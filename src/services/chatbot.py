from transitions import Machine
from sqlalchemy.orm import Session
import models
import logging
from utils.message_loader import message_loader
import redis.asyncio as redis
from typing import Optional

logger = logging.getLogger(__name__)

class ChatBot:
    states = ['start', 'register', 'menu_state', 'get_user_location', 'get_user_subject', 
              'get_user_schedule', 'about', 'get_term_info', 'get_article_summary', 
              'get_news_suggestion', 'feedback_state', 'unsubscribe_state', 'monthly_news_response']

    def __init__(self, db: Session, redis_client: Optional[redis.Redis] = None):
        self.db = db
        self.redis_client = redis_client
        self.machine = Machine(
            model=self,
            states=ChatBot.states,
            initial='start',
            auto_transitions=False
        )

        # Define transitions with proper triggers
        self.machine.add_transition(
            trigger='verify_user',
            source='start',
            dest='register',
            conditions=['is_new_user']
        )
        self.machine.add_transition(
            trigger='show_menu',
            source=['start', 'register', 'get_user_location', 'get_user_subject', 'get_user_schedule', 'unsubscribe_state', 'monthly_news_response'],
            dest='menu_state'
        )
        self.machine.add_transition(
            trigger='select_subscribe',
            source=['menu_state', 'get_user_location'],
            dest='get_user_location'
        )
        self.machine.add_transition(
            trigger='proceed_to_subjects',
            source='get_user_location',
            dest='get_user_subject'
        )
        self.machine.add_transition(
            trigger='proceed_to_schedule',
            source='get_user_subject',
            dest='get_user_schedule'
        )
        self.machine.add_transition(
            trigger='select_about',
            source='menu_state',
            dest='about'
        )
        self.machine.add_transition(
            trigger='select_term_info',
            source='menu_state',
            dest='get_term_info'
        )
        self.machine.add_transition(
            trigger='select_article_summary',
            source=['menu_state', 'monthly_news_response'],
            dest='get_article_summary'
        )
        self.machine.add_transition(
            trigger='select_news_suggestion',
            source='menu_state',
            dest='get_news_suggestion'
        )
        self.machine.add_transition(
            trigger='get_feedback',
            source=['get_term_info','get_article_summary', 'monthly_news_response'],
            dest='feedback_state'
        )
        self.machine.add_transition(
            trigger='select_unsubscribe',
            source='menu_state',
            dest='unsubscribe_state'
        )
        self.machine.add_transition(
            trigger='start_monthly_news_response',
            source='start',
            dest='monthly_news_response'
        )
        self.machine.add_transition(
            trigger='end_conversation',
            source=['register', 'get_user_schedule', 'about', 'feedback_state', 
                   'get_news_suggestion', 'get_article_summary', 'get_term_info', 
                   'unsubscribe_state', 'monthly_news_response'],
            dest='start'
        )

    def set_state(self, state):
        """Set the state explicitly"""
        if state in self.states:
            self.state = state
        else:
            self.state = 'start'

    def is_new_user(self, phone_number):
        """Check if a user with the given phone number exists"""
        try:
            user = self.db.query(models.User).filter_by(phone_number=phone_number).first()
            return user is None
        except Exception as e:
            logger.error(f"Error checking user: {e}")
            return True

    def register_user(self, phone_number: str):
        """Register a new user with the given phone number and name"""
        try:
            new_user = models.User(phone_number=phone_number)
            self.db.add(new_user)
            self.db.commit()
            return new_user
        except Exception as e:
            self.db.rollback()
            raise e

    def get_user(self, phone_number: str):
        """Get an existing user by phone number"""
        return self.db.query(models.User).filter_by(phone_number=phone_number).first()

    def save_location(self, user_id: int, location_name: str):
        """Save a new location for the user"""
        try:
            new_location = models.Location(location_name=location_name, user_id=user_id)
            self.db.add(new_location)
            self.db.commit()
            return new_location
        except Exception as e:
            self.db.rollback()
            raise e

    def save_subject(self, user_id: int, subject_name: str):
        """Save a new subject for the user"""
        try:
            new_subject = models.Subject(subject_name=subject_name, user_id=user_id)
            self.db.add(new_subject)
            self.db.commit()
            return new_subject
        except Exception as e:
            self.db.rollback()
            raise e

    def save_schedule(self, user_id: int, schedule: str):
        """Save the user's preferred schedule"""
        try:
            user = self.db.query(models.User).get(user_id)
            if user:
                user.schedule = schedule
                self.db.commit()
                return user
            raise Exception("User not found")
        except Exception as e:
            self.db.rollback()
            raise e

    async def set_current_interaction_id(self, interaction_id: int, phone_number: str):
        """Set the current interaction ID in Redis"""
        if self.redis_client:
            try:
                # Use the phone number as part of the key to make it unique per user
                redis_key = f"interaction:{phone_number}"
                await self.redis_client.set(redis_key, str(interaction_id))
                logger.info(f"Saved interaction ID {interaction_id} for phone {phone_number} in Redis")
                return True
            except Exception as e:
                logger.error(f"Failed to save interaction ID in Redis: {e}")
                # Fallback to instance variable if Redis fails
                self.current_interaction_id = interaction_id
                return False
        else:
            # Fallback to instance variable if Redis is not available
            logger.warning("Redis client not available, using instance variable for interaction ID")
            self.current_interaction_id = interaction_id
            return False

    async def get_current_interaction_id(self, phone_number: str) -> Optional[int]:
        """Get the current interaction ID from Redis"""
        if self.redis_client:
            try:
                redis_key = f"interaction:{phone_number}"
                interaction_id = await self.redis_client.get(redis_key)
                if interaction_id:
                    return int(interaction_id)
                logger.warning(f"No interaction ID found in Redis for phone {phone_number}")
                return None
            except Exception as e:
                logger.error(f"Failed to get interaction ID from Redis: {e}")
                # Fallback to instance variable if Redis fails
                return self.current_interaction_id
        else:
            # Fallback to instance variable if Redis is not available
            logger.warning("Redis client not available, using instance variable for interaction ID")
            return self.current_interaction_id