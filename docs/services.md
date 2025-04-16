# Services Documentation

This document provides detailed information about the various services used in the InfoAmazonia Boto application.

## Table of Contents

- [Search Service](#search-service)
- [News Service](#news-service)
- [Article Ingestion Service](#article-ingestion-service)
- [ChatGPT Service](#chatgpt-service)
- [ChatBot Service](#chatbot-service)
- [Message Handlers](#message-handlers)

## Search Service

The Search Service provides functionality for searching articles and retrieving information related to environmental terms and news from the Amazon region.

### Key Features

- Semantic vector search using embeddings
- Full-text search capabilities
- Article summarization and term explanations
- URL shortening and click-through rate tracking
- Caching mechanisms for improved performance

### Main Components

#### Search Endpoints

- `GET /` - Main search interface
- `GET /search-articles` - Article search interface
- `GET /ctr-stats` - Click-through rate statistics page
- `POST /api/search-articles` - API endpoint for article search
- `POST /api/search` - API endpoint for semantic search with summary generation
- `GET /api/article-stats` - Article statistics API
- `GET /api/ctr-stats` - Click-through rate statistics API
- `GET /r/<short_id>` - URL shortener redirection

#### Caching System

The service implements multiple caching mechanisms:
- `search_cache` - Caches search results (TTL: 5 minutes)
- `url_cache` - Maps shortened URL IDs to original URLs (TTL: 30 days)
- `url_impressions_cache` and `url_clicks_cache` - Track metrics for URLs

#### URL Shortening

The service creates shortened URLs for article links with:
- Unique identifier generation
- Click tracking
- UTM parameter addition for analytics

## News Service

The News Service fetches and processes news articles from various sources related to the Amazon region.

### Key Features

- API integration with WordPress-based news sources
- Multiple language support
- Location-based article filtering
- Topic categorization
- Duplicate detection

### Main Components

#### News Sources

The service connects to news sources through their API endpoints:
- InfoAmazonia in Portuguese
- Additional sources can be configured by extending the `api_sources` list

#### News Processing

For each fetched article, the service:
1. Extracts metadata (title, author, description, URL, etc.)
2. Processes location data
3. Categorizes articles into topics and subtopics
4. Checks for duplicates in the database

#### Topic Categorization

Articles are categorized into the following topics:
- `danos_ambientais` - Environmental damage
- `areas_protegidas` - Protected areas
- `povos` - Indigenous and local communities
- `mudanca_climatica` - Climate change
- `conservacao` - Conservation
- `politica_economia` - Politics and economy

## Article Ingestion Service

The Article Ingestion Service processes news items into searchable articles with AI-enhanced features.

### Key Features

- Automatic article summarization
- Vector embedding generation
- Retry mechanism for error handling
- Duplicate detection
- Batch processing

### Main Components

#### Article Processing

The `process_article` function:
1. Generates article summaries using AI
2. Creates vector embeddings for semantic search
3. Structures the article data for database storage
4. Includes retry logic for resilience

#### Batch Ingestion

The `ingest_articles` function:
1. Checks for database connectivity
2. Processes multiple articles in sequence
3. Performs duplicate detection
4. Handles individual article errors gracefully
5. Tracks ingestion statistics

## ChatGPT Service

The ChatGPT Service provides an abstraction layer for interacting with OpenAI's GPT models, with compatibility for both standard OpenAI API and Azure OpenAI Service.

### Key Features

- Multi-provider support (OpenAI and Azure OpenAI)
- Text embeddings generation
- Text completion and summarization
- Location and subject validation
- Image processing capabilities
- Streaming responses support

### Main Components

#### Initialization

The service automatically detects and configures the appropriate client:
- Azure OpenAI client when `USE_AZURE_OPENAI=True`
- Standard OpenAI client otherwise

#### Core Functions

- `generate_embedding` - Creates vector embeddings for semantic search
- `generate_completion` - Generates AI completions for queries
- `generate_term_summary` and `generate_article_summary` - Creates concise summaries
- `validate_location` and `validate_subject` - Validates user input
- `validate_schedule` - Validates and normalizes schedule preferences
- `process_image` - Analyzes images using vision capabilities
- `generate_streaming_completion` - Provides streaming responses

## ChatBot Service

The ChatBot Service manages conversational state and user interactions through a state machine.

### Key Features

- State management via transitions framework
- User registration and data persistence
- Interaction tracking
- Redis integration for distributed state storage
- Flexible conversation flow

### Main Components

#### State Machine

The ChatBot uses a state machine with the following states:
- `start` - Initial state
- `register` - User registration
- `menu_state` - Main menu
- `get_user_location` - Location collection
- `get_user_subject` - Subject interest collection
- `get_user_schedule` - Notification schedule selection
- `about` - Information about the service
- `get_term_info` - Term explanation
- `get_article_summary` - Article summarization
- `get_news_suggestion` - News suggestion collection
- `feedback_state` - Feedback collection
- `unsubscribe_state` - Unsubscription process
- `monthly_news_response` - Monthly news interaction

#### User Management

Functions for managing user data:
- `register_user` - Creates new user accounts
- `get_user` - Retrieves user information
- `save_location`, `save_subject`, `save_schedule` - Updates user preferences

#### State Persistence

The service can use Redis for distributed state storage:
- `set_current_interaction_id` - Stores current interaction in Redis or fallback storage
- `get_current_interaction_id` - Retrieves interaction data

## Message Handlers

The message handlers service manages the processing of user messages based on their current state in the conversation.

### Key Features

- State-specific message processing
- Interactive UI components generation
- Integration with external services
- Error handling with user-friendly messages
- User confirmation processing

### Main Components

#### State Handlers

Individual handler functions for different conversational states:

- `handle_start_state` - Initiates conversation
- `handle_register_state` - Processes registration
- `handle_menu_state` - Manages menu interactions with button UI
- `handle_location_state` - Processes location inputs
- `handle_subject_state` - Processes subject interest inputs
- `handle_schedule_state` - Manages notification schedule preferences
- `handle_about_state` - Provides information
- `handle_term_info_state` - Processes term queries
- `handle_feedback_state` - Collects user feedback
- `handle_article_summary_state` - Processes article lookup
- `handle_news_suggestion_state` - Collects news suggestions
- `handle_unsubscribe_state` - Manages unsubscription with confirmation
- `handle_monthly_news_response` - Processes responses to monthly news

#### Interactive UI

The service generates WhatsApp-compatible interactive components:
- Menu buttons
- Confirmation buttons
- Navigation options
