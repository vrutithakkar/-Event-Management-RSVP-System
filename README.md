# Event Management & RSVP System

A simple Django-based event management application where users can:
- register and log in
- create events
- view event details
- RSVP to events
- cancel RSVPs
- search and filter events by title or location

## Features
- User authentication
- Event creation, update, and deletion
- RSVP system with confirmation messages
- Event dashboard with search and location filters
- Basic email confirmation support via Django console backend

## Project Structure
- `events/` - main app containing models, views, forms, templates, and tests
- `event_management/` - Django project settings and URL routing

## Requirements
- Python 3.10+
- Django 4.2+

## Installation
1. Clone the repository
2. Navigate to the project folder:
   ```bash
   cd event_management
   ```
3. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows use: venv\Scripts\activate
   ```
4. Install dependencies:
   ```bash
   pip install django
   ```

## Run the Project
1. Apply migrations:
   ```bash
   python manage.py migrate
   ```
2. Start the development server:
   ```bash
   python manage.py runserver
   ```
3. Open your browser at:
   ```text
   http://127.0.0.1:8000/
   ```

## Run Tests
```bash
python manage.py test
```

