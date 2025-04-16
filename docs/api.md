# InfoAmazonia Boto API Documentation

This document provides a comprehensive list of all API endpoints in the InfoAmazonia Boto application, categorized by their functionality.

## Authentication Endpoints

### `/login` (GET)
- **Description**: Renders the login page
- **Response**: HTML login page
- **Authentication**: None required

### `/token` (POST)
- **Description**: Authenticates admin users and creates access token
- **Parameters**: 
  - `username`: Admin username
  - `password`: Admin password
- **Response**: Redirects to homepage with authentication cookie
- **Authentication**: None required

### `/logout` (GET)
- **Description**: Logs out the current user by removing authentication cookie
- **Response**: Redirects to login page
- **Authentication**: None required

## Dashboard Endpoints

### `/` (GET)
- **Description**: Main dashboard page
- **Response**: HTML dashboard page
- **Authentication**: Admin required

### `/health` (GET)
- **Description**: Health check endpoint for monitoring application status
- **Response**: JSON with system health information
- **Authentication**: None required

### `/api/dashboard/stats` (GET)
- **Description**: Provides general dashboard statistics
- **Response**: JSON with user counts, message stats, and click rates
- **Authentication**: Admin required

### `/api/dashboard/recent-users` (GET)
- **Description**: Lists recently registered users
- **Response**: JSON with recent user information
- **Authentication**: Admin required

### `/api/dashboard/news-sources` (GET)
- **Description**: Lists news sources
- **Response**: JSON with news sources information
- **Authentication**: Admin required

### `/api/dashboard/user-stats` (GET)
- **Description**: Provides weekly user statistics over time
- **Response**: JSON with user growth metrics
- **Authentication**: Admin required

### `/api/dashboard/message-stats` (GET) 
- **Description**: Provides weekly message statistics over time
- **Response**: JSON with message count metrics
- **Authentication**: Admin required

### `/api/dashboard/status-stats` (GET)
- **Description**: Provides message status metrics over time
- **Response**: JSON with message status counts
- **Authentication**: Admin required

### `/api/v1/analytics/ctr-stats` (GET)
- **Description**: Gets click-through rate statistics from external API
- **Response**: JSON with CTR metrics
- **Authentication**: Admin required

### `/api/scheduler/runs` (GET)
- **Description**: Lists recent scheduler job executions
- **Response**: JSON with scheduler run details
- **Authentication**: Admin required

## Admin User Management Endpoints

### `/admin/users` (GET)
- **Description**: List all users with filtering options
- **Parameters**:
  - `phone_number` (optional): Filter by phone number
  - `status` (optional): Filter by active/inactive status
  - `sort` (optional): Sort by creation date
  - `skip` (optional): Pagination offset
  - `limit` (optional): Page size
- **Response**: HTML page with users list
- **Authentication**: Admin required

### `/admin/users/create` (POST)
- **Description**: Creates a new user
- **Parameters**:
  - `phone_number`: User's phone number
  - `status`: Active or inactive
  - `schedule`: Message frequency preference
- **Response**: Redirects to user detail page
- **Authentication**: Admin required

### `/admin/users/{user_id}` (GET)
- **Description**: Shows detailed information about a specific user
- **Parameters**:
  - `user_id`: User ID
- **Response**: HTML page with user details
- **Authentication**: Admin required

### `/admin/users/{user_id}/status` (POST)
- **Description**: Updates a user's active status
- **Parameters**:
  - `user_id`: User ID
  - `status`: Active or inactive
- **Response**: Redirects to user detail page
- **Authentication**: Admin required

### `/admin/users/{user_id}/schedule` (POST)
- **Description**: Updates a user's message schedule preference
- **Parameters**:
  - `user_id`: User ID
  - `schedule`: Message frequency preference
- **Response**: Redirects to user detail page
- **Authentication**: Admin required

## Location Management Endpoints

### `/admin/users/{user_id}/location` (POST)
- **Description**: Adds location information to a user's profile
- **Parameters**:
  - `user_id`: User ID
  - `location_name`: Name of the location
- **Response**: Redirects to user detail page
- **Authentication**: Admin required

### `/admin/users/{user_id}/locations/{location_id}/delete` (POST)
- **Description**: Deletes a location from a user's profile
- **Parameters**:
  - `user_id`: User ID
  - `location_id`: Location ID to delete
- **Response**: Redirects to user detail page
- **Authentication**: Admin required

## Subject Management Endpoints

### `/admin/users/{user_id}/subjects` (POST)
- **Description**: Adds a subject of interest to a user's profile
- **Parameters**:
  - `user_id`: User ID
  - `subject_name`: Subject name
- **Response**: Redirects to user detail page
- **Authentication**: Admin required

### `/admin/users/{user_id}/subjects/{subject_id}/delete` (POST)
- **Description**: Deletes a subject from a user's profile
- **Parameters**:
  - `user_id`: User ID
  - `subject_id`: Subject ID to delete
- **Response**: Redirects to user detail page
- **Authentication**: Admin required

## Message Management Endpoints

### `/admin/messages` (GET)
- **Description**: Lists all messages with filtering options
- **Parameters**:
  - `page` (optional): Page number for pagination
  - `page_size` (optional): Page size for pagination
  - `message_type` (optional): Filter by message type
  - `status` (optional): Filter by status
  - `phone_number` (optional): Filter by phone number
- **Response**: HTML page with messages list
- **Authentication**: Admin required

### `/admin/messages/template` (POST)
- **Description**: Creates a new message template
- **Parameters**:
  - `name`: Template name
  - `content`: Template content
  - `variables`: JSON string of template variables
- **Response**: Redirects to messages page
- **Authentication**: Admin required

### `/admin/messages/schedule` (POST)
- **Description**: Schedules a message for delivery
- **Parameters**:
  - `template_id`: Message template ID
  - `schedule_type`: Immediate or scheduled
  - `scheduled_date` (optional): Date for scheduled messages
  - `target_group`: User group to target
- **Response**: Redirects to messages page
- **Authentication**: Admin required

### `/admin/messages/send-template` (POST)
- **Description**: Sends a template message to a specific user
- **Parameters**:
  - `template_name`: Name of the template
  - `language_code`: Language code for the template
  - `phone_number`: Recipient phone number
- **Response**: Redirects to messages page
- **Authentication**: Admin required

## Interaction Analysis Endpoints

### `/admin/interactions` (GET)
- **Description**: Lists user interactions with the system
- **Parameters**:
  - `skip` (optional): Pagination offset
  - `limit` (optional): Page size
- **Response**: HTML page with interactions list
- **Authentication**: Admin required

### `/admin/interactions/summaries/{category}` (GET)
- **Description**: Provides AI-generated summaries of user interactions by category
- **Parameters**:
  - `category`: Interaction category to summarize
- **Response**: JSON with summary text
- **Authentication**: Admin required

## News Sources Management

### `/admin/news-sources` (GET)
- **Description**: Lists all news sources
- **Parameters**:
  - `skip` (optional): Pagination offset
  - `limit` (optional): Page size
- **Response**: HTML page with news sources list
- **Authentication**: Admin required

## Analytics and Metrics Endpoints

### `/admin/metrics` (GET)
- **Description**: Shows system metrics data
- **Response**: HTML page with metrics visualization
- **Authentication**: Admin required

### `/admin/scheduler` (GET)
- **Description**: Lists scheduler run history
- **Parameters**:
  - `skip` (optional): Pagination offset
  - `limit` (optional): Page size
- **Response**: HTML page with scheduler runs
- **Authentication**: Admin required

### `/admin/ctr-stats` (GET)
- **Description**: Shows click-through rate statistics
- **Response**: HTML page with CTR statistics
- **Authentication**: Admin required
