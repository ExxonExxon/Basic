# Tradsiee: Video Lead Generation Engine

## Project Overview
Tradsiee is a specialized lead generation platform designed for tradespeople ("tradies"). It allows customers to quickly record or upload a video describing their problem (e.g., a plumbing leak), which is then sent as a lead to the tradie. The system handles video storage, SMS notifications, and provides a comprehensive dashboard for tradies to manage their leads.

### Main Technologies
- **Backend:** Python (FastAPI)
- **Database & Auth:** Supabase
- **Video Storage:** Cloudinary
- **SMS Notifications:** Twilio
- **Frontend:** Vanilla HTML/JS with Tailwind CSS, Chart.js for analytics.

## Architecture
The system follows a widget-based architecture:
1.  **Widget Injection:** Tradies embed a `<script>` tag pointing to the `/loader.js` endpoint.
2.  **Customer Interaction:** Customers enter their phone number, record a video, and provide a description.
3.  **Lead Processing:** The backend receives the lead, stores the video in Cloudinary, records metadata in Supabase, and notifies the tradie via Twilio SMS.
4.  **Tradie Portal:** A password-protected dashboard (`portal.html`) allows tradies to view lead details, watch videos, and manage their business performance.

## Getting Started

### Prerequisites
- Python 3.12+
- A `.env` file with credentials for Supabase, Cloudinary, and Twilio.
- A Supabase project with appropriate tables (businesses, leads).

### Building and Running
- **Backend:** 
  ```bash
  uvicorn main:app --reload
  ```
- **Frontend:** 
  The HTML files can be served using any static server (e.g., Live Server in VS Code or `python -m http.server 5500`).
  Note: The widget expects the backend to be running on `http://127.0.0.1:8000`.

### Core Components
- `main.py`: The FastAPI application, handling API routes, authentication dependencies, and external integrations.
- `index.html`: The core widget template.
- `portal.html`: The main tradie dashboard.
- `login.html` / `signup.html`: Authentication flow.
- `.env`: Environment configuration for third-party services.

## Development Conventions
- **API Styling:** Follows FastAPI best practices with Pydantic models for validation and `HTTPBearer` for Supabase JWT verification.
- **Frontend Styling:** Uses Tailwind CSS via CDN for rapid prototyping and styling.
- **Video Handling:** Direct uploads to Cloudinary from the client side using unsigned presets.
- **SMS:** Twilio Messaging Service is used for both tradie and customer notifications.

## TODO / Future Improvements
- [ ] Add unit and integration tests for FastAPI routes.
- [ ] Implement a more robust templating engine for the widget (currently using string replacement).
- [ ] Move frontend logic into a modern framework (React/Vue) for better state management in the portal.
- [ ] Implement error logging and monitoring (e.g., Sentry).
