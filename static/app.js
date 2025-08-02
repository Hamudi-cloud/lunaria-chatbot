class ChatApp {
    constructor() {
        this.sessionId = null;
        this.isConnected = false;
        this.messageForm = document.getElementById('messageForm');
        this.messageInput = document.getElementById('messageInput');
        this.sendBtn = document.getElementById('sendBtn');
        this.clearBtn = document.getElementById('clearBtn');
        this.messagesContainer = document.getElementById('messagesContainer');
        this.loadingIndicator = document.getElementById('loadingIndicator');
        this.statusBadge = document.getElementById('statusBadge');
        this.charCount = document.getElementById('charCount');
        this.errorModal = new bootstrap.Modal(document.getElementById('errorModal'));
        
        this.initializeEventListeners();
        this.initializeChat();
    }

    initializeEventListeners() {
        // Message form submission
        this.messageForm.addEventListener('submit', (e) => {
            e.preventDefault();
            this.sendMessage();
        });

        // Clear chat button
        this.clearBtn.addEventListener('click', () => {
            this.clearChat();
        });

        // Character counter
        this.messageInput.addEventListener('input', () => {
            const length = this.messageInput.value.length;
            this.charCount.textContent = length;
            
            if (length > 900) {
                this.charCount.classList.add('text-warning');
            } else {
                this.charCount.classList.remove('text-warning');
            }
        });

        // Enter key to send message
        this.messageInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
    }

    async initializeChat() {
        try {
            this.updateStatus('connecting', 'Connecting...');
            
            const response = await fetch('/api/chat/start', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            const data = await response.json();

            if (data.success) {
                this.sessionId = data.session_id;
                this.isConnected = true;
                this.enableInput();
                this.updateStatus('connected', 'Connected');
                console.log('Chat session started:', this.sessionId);
            } else {
                throw new Error(data.error || 'Failed to start chat session');
            }
        } catch (error) {
            console.error('Failed to initialize chat:', error);
            this.updateStatus('error', 'Connection Failed');
            this.showError('Failed to connect to the chat service. Please refresh the page and try again.');
        }
    }

    async sendMessage() {
        const message = this.messageInput.value.trim();
        
        if (!message || !this.isConnected) {
            return;
        }

        // Clear input and disable while processing
        this.messageInput.value = '';
        this.charCount.textContent = '0';
        this.disableInput();

        // Add user message to chat
        this.addMessage('user', message);

        // Show loading indicator
        this.showLoading();

        try {
            const response = await fetch('/api/chat/message', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    message: message,
                    session_id: this.sessionId
                })
            });

            const data = await response.json();

            if (data.success) {
                this.addMessage('assistant', data.response);
            } else {
                throw new Error(data.error || 'Failed to get response');
            }
        } catch (error) {
            console.error('Failed to send message:', error);
            this.addMessage('assistant', 'Sorry, I encountered an error processing your message. Please try again.');
            this.showError('Failed to send message. Please try again.');
        } finally {
            this.hideLoading();
            this.enableInput();
            this.messageInput.focus();
        }
    }

    async clearChat() {
        if (!this.isConnected) {
            return;
        }

        try {
            const response = await fetch(`/api/chat/clear/${this.sessionId}`, {
                method: 'DELETE'
            });

            const data = await response.json();

            if (data.success) {
                // Clear messages except welcome message
                this.messagesContainer.innerHTML = `
                    <div class="message-group mb-4">
                        <div class="d-flex">
                            <div class="avatar-container me-3">
                                <div class="avatar bg-primary">
                                    <i class="bi bi-robot"></i>
                                </div>
                            </div>
                            <div class="message-content">
                                <div class="message bg-light p-3 rounded">
                                    <p class="mb-0">Hello! I'm your AI assistant. How can I help you today?</p>
                                </div>
                                <small class="text-muted mt-1 d-block">Just now</small>
                            </div>
                        </div>
                    </div>
                `;
                this.scrollToBottom();
            } else {
                throw new Error(data.error || 'Failed to clear chat');
            }
        } catch (error) {
            console.error('Failed to clear chat:', error);
            this.showError('Failed to clear chat. Please try again.');
        }
    }

    addMessage(role, content) {
        const messageGroup = document.createElement('div');
        messageGroup.className = 'message-group mb-4';

        const isUser = role === 'user';
        const timestamp = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

        messageGroup.innerHTML = `
            <div class="d-flex ${isUser ? 'flex-row-reverse' : ''}">
                <div class="avatar-container ${isUser ? 'ms-3' : 'me-3'}">
                    <div class="avatar ${isUser ? 'bg-success' : 'bg-primary'}">
                        <i class="bi ${isUser ? 'bi-person' : 'bi-robot'}"></i>
                    </div>
                </div>
                <div class="message-content">
                    <div class="message ${isUser ? 'bg-success text-white' : 'bg-light'} p-3 rounded">
                        <p class="mb-0">${this.escapeHtml(content)}</p>
                    </div>
                    <small class="text-muted mt-1 d-block ${isUser ? 'text-end' : ''}">${timestamp}</small>
                </div>
            </div>
        `;

        this.messagesContainer.appendChild(messageGroup);
        this.scrollToBottom();
    }

    showLoading() {
        this.loadingIndicator.style.display = 'block';
        this.scrollToBottom();
    }

    hideLoading() {
        this.loadingIndicator.style.display = 'none';
    }

    enableInput() {
        this.messageInput.disabled = false;
        this.sendBtn.disabled = false;
    }

    disableInput() {
        this.messageInput.disabled = true;
        this.sendBtn.disabled = true;
    }

    updateStatus(status, text) {
        const badge = this.statusBadge;
        badge.className = 'badge';
        
        switch (status) {
            case 'connected':
                badge.classList.add('bg-success');
                break;
            case 'connecting':
                badge.classList.add('bg-warning');
                break;
            case 'error':
                badge.classList.add('bg-danger');
                break;
            default:
                badge.classList.add('bg-secondary');
        }

        badge.innerHTML = `<i class="bi bi-circle-fill me-1"></i>${text}`;
    }

    showError(message) {
        document.getElementById('errorMessage').textContent = message;
        this.errorModal.show();
    }

    scrollToBottom() {
        const chatContainer = document.getElementById('chatContainer');
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Initialize the chat app when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new ChatApp();
});
