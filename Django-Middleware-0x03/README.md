# Django Middleware Project

This project implements various custom middleware components for a Django chat application.

## Middleware Implemented

### 1. RequestLoggingMiddleware
Logs each user's requests to a file (`requests.log`) with timestamp, username, and request path.

### 2. RestrictAccessByTimeMiddleware
Restricts access to chat functionality between 9 PM and 6 AM, returning a 403 Forbidden error.

### 3. OffensiveLanguageMiddleware
- Detects offensive language in messages using a predefined word list
- Implements rate limiting (5 messages per minute per IP address)
- Returns appropriate error responses for violations

### 4. RolePermissionMiddleware
Enforces role-based access control for the admin panel, allowing only admin or moderator users.

## Setup Instructions

1. Clone the repository
2. Create virtual environment: `python -m venv venv`
3. Activate virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix/MacOS: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Apply migrations: `python manage.py migrate`
6. Create superuser: `python manage.py createsuperuser`
7. Run server: `python manage.py runserver`

## Testing the Middleware

Use tools like Postman or curl to test:

1. **Request Logging**: Check `requests.log` file after making requests
2. **Time Restriction**: Try accessing `/chats/messages/` between 9 PM and 6 AM
3. **Rate Limiting**: Send multiple POST requests to `/chats/messages/` within a minute
4. **Role Permission**: Try accessing `/chats/admin-panel/` with different user roles

## API Endpoints

- `GET /chats/messages/` - Get all chat messages
- `POST /chats/messages/` - Create new message (requires authentication)
- `GET /chats/admin-panel/` - Admin dashboard (requires admin role)