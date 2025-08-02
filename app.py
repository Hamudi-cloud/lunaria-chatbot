import os
import logging
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from chatbot import ChatbotService
import uuid

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")

# Enable CORS for frontend integration
CORS(app)

# Initialize chatbot service
chatbot_service = ChatbotService()

# In-memory storage for chat sessions
chat_sessions = {}

@app.route('/')
def index():
    """Serve the main chat interface"""
    return render_template('index.html')

@app.route('/api/chat/start', methods=['POST'])
def start_chat():
    """Start a new chat session"""
    try:
        session_id = str(uuid.uuid4())
        chat_sessions[session_id] = {
            'messages': [],
            'created_at': None
        }
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'message': 'Chat session started successfully'
        }), 200
        
    except Exception as e:
        logging.error(f"Error starting chat session: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to start chat session'
        }), 500

@app.route('/api/chat/message', methods=['POST'])
def send_message():
    """Send a message and get AI response"""
    try:
        data = request.get_json()
        
        # Validate request
        if not data or 'message' not in data or 'session_id' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing required fields: message and session_id'
            }), 400
        
        session_id = data['session_id']
        user_message = data['message'].strip()
        
        if not user_message:
            return jsonify({
                'success': False,
                'error': 'Message cannot be empty'
            }), 400
        
        # Check if session exists
        if session_id not in chat_sessions:
            return jsonify({
                'success': False,
                'error': 'Invalid session ID. Please start a new chat session.'
            }), 404
        
        # Get conversation history
        conversation_history = chat_sessions[session_id]['messages']
        
        # Add user message to history
        conversation_history.append({
            'role': 'user',
            'content': user_message
        })
        
        # Get AI response
        ai_response = chatbot_service.get_response(conversation_history)
        
        # Add AI response to history
        conversation_history.append({
            'role': 'assistant',
            'content': ai_response
        })
        
        # Update session
        chat_sessions[session_id]['messages'] = conversation_history
        
        return jsonify({
            'success': True,
            'response': ai_response,
            'session_id': session_id
        }), 200
        
    except Exception as e:
        logging.error(f"Error processing message: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to process message. Please try again.'
        }), 500

@app.route('/api/chat/history/<session_id>', methods=['GET'])
def get_chat_history(session_id):
    """Get conversation history for a session"""
    try:
        if session_id not in chat_sessions:
            return jsonify({
                'success': False,
                'error': 'Session not found'
            }), 404
        
        return jsonify({
            'success': True,
            'messages': chat_sessions[session_id]['messages']
        }), 200
        
    except Exception as e:
        logging.error(f"Error retrieving chat history: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to retrieve chat history'
        }), 500

@app.route('/api/chat/clear/<session_id>', methods=['DELETE'])
def clear_chat_history(session_id):
    """Clear conversation history for a session"""
    try:
        if session_id not in chat_sessions:
            return jsonify({
                'success': False,
                'error': 'Session not found'
            }), 404
        
        chat_sessions[session_id]['messages'] = []
        
        return jsonify({
            'success': True,
            'message': 'Chat history cleared successfully'
        }), 200
        
    except Exception as e:
        logging.error(f"Error clearing chat history: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to clear chat history'
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'AI Chatbot Backend',
        'active_sessions': len(chat_sessions)
    }), 200

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
