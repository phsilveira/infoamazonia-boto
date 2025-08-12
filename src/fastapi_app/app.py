import logging
import os
import pathlib
import json
import time
from datetime import datetime
import pkg_resources  # Add this import for getting installed packages

# Conditionally import Azure Monitor
try:
    from azure.monitor.opentelemetry import configure_azure_monitor
    has_azure_monitor = True
except ImportError:
    has_azure_monitor = False

from fastapi import Depends, FastAPI, Form, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.sql import func
from sqlmodel import Session, select
import sqlalchemy

from .models import Restaurant, Review, engine, redis_client
from .redis_utils import cache_get, cache_set

# Setup logger and Azure Monitor:
logger = logging.getLogger("app")
logger.setLevel(logging.INFO)
if os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING") and has_azure_monitor:
    configure_azure_monitor()
    logger.info("Azure Monitor configured")
else:
    logger.info("Azure Monitor not available or not configured")

# Setup FastAPI app:
app = FastAPI()
parent_path = pathlib.Path(__file__).parent.parent
app.mount("/mount", StaticFiles(directory=parent_path / "static"), name="static")
templates = Jinja2Templates(directory=parent_path / "templates")
templates.env.globals["prod"] = os.environ.get("RUNNING_IN_PRODUCTION", False)
# Use relative path for url_for, so that it works behind a proxy like Codespaces
templates.env.globals["url_for"] = app.url_path_for


# Dependency to get the database session
def get_db_session():
    with Session(engine) as session:
        yield session


@app.get("/health", response_class=JSONResponse)
async def health():
    """
    Health check endpoint to verify if the application, database and Redis are working.
    Returns a JSON response with status information.
    """
    health_status = {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "app": {"status": "healthy"},
            "database": {"status": "unknown"},
            "redis": {"status": "unknown"},
        },
        # "dependencies": {},  # Add a new field for dependencies
        # "environment": {}    # Add environment variables information
    }
    
    # # Add installed packages information
    # try:
    #     installed_packages = pkg_resources.working_set
    #     health_status["dependencies"] = {pkg.key: pkg.version for pkg in installed_packages}
    # except Exception as e:
    #     health_status["dependencies"] = {"error": f"Failed to retrieve packages: {str(e)}"}
    
    # # Add environment variables (without exposing sensitive values)
    # sensitive_prefixes = ['KEY', 'SECRET', 'TOKEN', 'PASSWORD', 'PASS', 'AUTH', 'CREDENTIAL']
    # for key in os.environ:
    #     # Skip internal Python environment variables
    #     if key.startswith(('PYTHON', '_')) or 'VSCODE' in key:
    #         continue
            
    #     # Check if this is a sensitive variable
    #     is_sensitive = any(sensitive in key.upper() for sensitive in sensitive_prefixes)
        
    #     if is_sensitive:
    #         # For sensitive values, just indicate they exist but don't show the value
    #         health_status["environment"][key] = "[REDACTED]"
    #     else:
    #         # For non-sensitive values, show the actual value
    #         health_status["environment"][key] = os.environ[key]
    
    # Check database connection
    try:
        # Use a simple query to check database connection
        with Session(engine) as session:
            session.exec(select(func.now())).first()
        health_status["services"]["database"] = {
            "status": "healthy",
            "message": "Database connection successful"
        }
    except sqlalchemy.exc.SQLAlchemyError as e:
        health_status["status"] = "unhealthy"
        health_status["services"]["database"] = {
            "status": "unhealthy",
            "message": f"Database connection failed: {str(e)}"
        }
        logger.error(f"Database health check failed: {str(e)}")

    # Check Redis connection
    if redis_client:
        try:
            # Set a test value with a short timeout
            test_key = f"health_check_{int(time.time())}"
            if redis_client.set(test_key, "ok", ex=10):
                health_status["services"]["redis"] = {
                    "status": "healthy",
                    "message": "Redis connection successful"
                }
            else:
                raise Exception("Failed to set test key")
        except Exception as e:
            health_status["status"] = "unhealthy"
            health_status["services"]["redis"] = {
                "status": "unhealthy",
                "message": f"Redis connection failed: {str(e)}"
            }
            logger.error(f"Redis health check failed: {str(e)}")
    else:
        health_status["services"]["redis"] = {
            "status": "not_configured",
            "message": "Redis client not initialized"
        }
    
    status_code = 200 if health_status["status"] == "healthy" else 503
    return JSONResponse(content=health_status, status_code=status_code)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request, session: Session = Depends(get_db_session)):
    logger.info("root called")
    
    # Try to get data from Redis cache
    cached_data = None
    if redis_client:
        cached_data = cache_get(redis_client, "restaurants_list")
        if cached_data:
            logger.info("Using cached restaurant data from Redis")
            restaurants = json.loads(cached_data)
            return templates.TemplateResponse("index.html", {"request": request, "restaurants": restaurants})
    
    # If not in cache, query the database
    statement = (
        select(Restaurant, func.avg(Review.rating).label("avg_rating"), func.count(Review.id).label("review_count"))
        .outerjoin(Review, Review.restaurant == Restaurant.id)
        .group_by(Restaurant.id)
    )
    results = session.exec(statement).all()

    restaurants = []
    for restaurant, avg_rating, review_count in results:
        restaurant_dict = restaurant.dict()
        restaurant_dict["avg_rating"] = avg_rating
        restaurant_dict["review_count"] = review_count
        restaurant_dict["stars_percent"] = round((float(avg_rating) / 5.0) * 100) if review_count > 0 else 0
        restaurants.append(restaurant_dict)

    # Store in Redis cache
    if redis_client:
        cache_set(redis_client, "restaurants_list", json.dumps(restaurants), 300)  # Cache for 5 minutes

    return templates.TemplateResponse("index.html", {"request": request, "restaurants": restaurants})


@app.get("/create", response_class=HTMLResponse)
async def create_restaurant(request: Request):
    logger.info("Request for add restaurant page received")
    return templates.TemplateResponse("create_restaurant.html", {"request": request})


@app.post("/add", response_class=RedirectResponse)
async def add_restaurant(
    request: Request, restaurant_name: str = Form(...), street_address: str = Form(...), description: str = Form(...),
    session: Session = Depends(get_db_session)
):
    logger.info("name: %s address: %s description: %s", restaurant_name, street_address, description)
    restaurant = Restaurant()
    restaurant.name = restaurant_name
    restaurant.street_address = street_address
    restaurant.description = description
    session.add(restaurant)
    session.commit()
    session.refresh(restaurant)
    
    # Invalidate Redis cache after adding a new restaurant
    if redis_client:
        redis_client.delete("restaurants_list")
        logger.info("Redis cache for restaurants list invalidated")

    return RedirectResponse(url=app.url_path_for("details", id=restaurant.id), status_code=status.HTTP_303_SEE_OTHER)


@app.get("/details/{id}", response_class=HTMLResponse)
async def details(request: Request, id: int, session: Session = Depends(get_db_session)):
    # Try to get from Redis cache
    cache_key = f"restaurant_details:{id}"
    if redis_client:
        cached_data = cache_get(redis_client, cache_key)
        if cached_data:
            logger.info(f"Using cached data for restaurant {id}")
            data = json.loads(cached_data)
            return templates.TemplateResponse("details.html", {
                "request": request, 
                "restaurant": data["restaurant"], 
                "reviews": data["reviews"]
            })

    restaurant = session.exec(select(Restaurant).where(Restaurant.id == id)).first()
    reviews = session.exec(select(Review).where(Review.restaurant == id)).all()

    review_count = len(reviews)
    avg_rating = 0
    if review_count > 0:
        avg_rating = sum(review.rating for review in reviews if review.rating is not None) / review_count

    restaurant_dict = restaurant.dict()
    restaurant_dict["avg_rating"] = avg_rating
    restaurant_dict["review_count"] = review_count
    restaurant_dict["stars_percent"] = round((float(avg_rating) / 5.0) * 100) if review_count > 0 else 0
    
    # Convert reviews for JSON serialization
    reviews_list = []
    for review in reviews:
        review_dict = review.dict()
        review_dict["review_date"] = review_dict["review_date"].isoformat()
        reviews_list.append(review_dict)
    
    # Store in Redis cache
    if redis_client:
        cache_data = {
            "restaurant": restaurant_dict,
            "reviews": reviews_list
        }
        cache_set(redis_client, cache_key, json.dumps(cache_data), 300)  # Cache for 5 minutes

    return templates.TemplateResponse(
        "details.html", {"request": request, "restaurant": restaurant_dict, "reviews": reviews}
    )


@app.post("/review/{id}", response_class=RedirectResponse)
async def add_review(
    request: Request,
    id: int,
    user_name: str = Form(...),
    rating: str = Form(...),
    review_text: str = Form(...),
    session: Session = Depends(get_db_session),
):
    review = Review()
    review.restaurant = id
    review.review_date = datetime.now()
    review.user_name = user_name
    review.rating = int(rating)
    review.review_text = review_text
    session.add(review)
    session.commit()
    
    # Invalidate related caches
    if redis_client:
        redis_client.delete(f"restaurant_details:{id}")
        redis_client.delete("restaurants_list")
        logger.info(f"Redis cache for restaurant {id} invalidated")

    return RedirectResponse(url=app.url_path_for("details", id=id), status_code=status.HTTP_303_SEE_OTHER)
