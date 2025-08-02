# AI Chatbot Application

## Overview

This is a web-based AI chatbot application built with Flask and OpenAI's GPT-4o model. The application provides a modern, responsive chat interface where users can have conversations with an AI assistant. It features a clean Bootstrap-based UI with dark theme support and real-time messaging capabilities.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

The application follows a simple client-server architecture with the following layers:

1. **Frontend**: Static HTML/CSS/JavaScript served by Flask
2. **Backend**: Flask web application with REST API endpoints
3. **AI Service**: OpenAI GPT-4o integration via ChatbotService
4. **Session Management**: In-memory storage for chat sessions

The architecture prioritizes simplicity and rapid development over complex scalability patterns, making it ideal for prototype and small-scale deployments.

## Key Components

### Backend Components

- **Flask Application (`app.py`)**: Main web server handling HTTP requests and serving templates
- **ChatbotService (`chatbot.py`)**: Service layer for OpenAI API integration and conversation management
- **Main Entry Point (`main.py`)**: Application launcher with development server configuration

### Frontend Components

- **Chat Interface (`templates/index.html`)**: Bootstrap-based responsive UI with dark theme
- **JavaScript Logic (`static/app.js`)**: Client-side chat functionality and API communication
- **Styling (`static/style.css`)**: Custom CSS for enhanced user experience

### API Endpoints

- `GET /`: Serves the main chat interface
- `POST /api/chat/start`: Initializes new chat sessions with UUID-based identification

## Data Flow

1. **Session Initialization**: Client requests new chat session via `/api/chat/start`
2. **Message Processing**: User messages are processed through the ChatbotService
3. **AI Integration**: Conversation history is sent to OpenAI GPT-4o model
4. **Response Handling**: AI responses are formatted and returned to the client
5. **Session Management**: Chat history is maintained in server memory using session IDs

The system uses a conversation history approach, limiting recent messages to manage token usage while maintaining context.

## External Dependencies

### Required Services
- **OpenAI API**: Core AI functionality using GPT-4o model
- **Environment Variables**: `OPENAI_API_KEY` for API authentication, `SESSION_SECRET` for Flask sessions

### Frontend Libraries
- **Bootstrap 5**: UI framework with Replit agent dark theme
- **Bootstrap Icons**: Icon set for UI elements
- **Modern Web Standards**: ES6+ JavaScript, CSS3, HTML5

### Python Packages
- **Flask**: Web framework and template engine
- **Flask-CORS**: Cross-origin resource sharing support
- **OpenAI**: Official Python client for OpenAI API
- **UUID**: Session ID generation

## Deployment Strategy

The application is configured for development deployment with:

- **Development Server**: Flask's built-in server on host `0.0.0.0`, port `5000`
- **Debug Mode**: Enabled for development with hot reload
- **Environment Configuration**: Uses environment variables for sensitive data
- **CORS Support**: Enabled for frontend integration flexibility

### Production Considerations
- Replace in-memory session storage with persistent database
- Implement proper session cleanup and expiration
- Add rate limiting and authentication mechanisms
- Use production WSGI server instead of Flask development server
- Implement proper error handling and logging strategies

The current architecture supports easy migration to production environments by replacing the session storage mechanism and adding appropriate middleware for security and performance.