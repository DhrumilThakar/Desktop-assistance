document.addEventListener('DOMContentLoaded', () => {
    const startBtn = document.getElementById('startBtn');
    const stopBtn = document.getElementById('stopBtn');
    const currentCommand = document.getElementById('currentCommand');
    const commandHistory = document.getElementById('commandHistory');
    const featureCards = document.querySelectorAll('.feature-card');
    const statusIndicator = document.querySelector('.status-indicator');
    const statusText = document.querySelector('.status-text');

    let isListening = false;
    let ws = null;

    // Initialize WebSocket connection
    function initializeWebSocket() {
        ws = new WebSocket('ws://localhost:8765');

        ws.onopen = () => {
            console.log('Connected to server');
            updateStatus(true);
            startBtn.disabled = false;
            stopBtn.disabled = true;
        };

        ws.onclose = () => {
            console.log('Disconnected from server');
            updateStatus(false);
            startBtn.disabled = false;
            stopBtn.disabled = true;
        };

        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            handleServerMessage(data);
        };

        ws.onerror = (error) => {
            console.error('WebSocket error:', error);
            updateStatus(false);
        };
    }

    // Update status indicator
    function updateStatus(active) {
        statusIndicator.style.backgroundColor = active ? '#00B894' : '#FF7675';
        statusText.textContent = active ? 'Active' : 'Inactive';
        statusText.style.color = active ? '#00B894' : '#FF7675';
    }

    // Handle server messages
    function handleServerMessage(data) {
        switch (data.type) {
            case 'command':
                addToHistory(`You: ${data.text}`, 'command');
                break;
            case 'response':
                addToHistory(`Assistant: ${data.text}`, 'response');
                break;
            case 'error':
                addToHistory(`Error: ${data.text}`, 'error');
                break;
        }
    }

    // Add message to command history
    function addToHistory(text, type = 'command') {
        const messageDiv = document.createElement('div');
        messageDiv.className = `history-message ${type}`;
        messageDiv.textContent = text;
        commandHistory.appendChild(messageDiv);
        commandHistory.scrollTop = commandHistory.scrollHeight;
    }

    // Start listening
    startBtn.addEventListener('click', () => {
        if (!isListening && ws && ws.readyState === WebSocket.OPEN) {
            isListening = true;
            currentCommand.textContent = 'Listening...';
            startBtn.disabled = true;
            stopBtn.disabled = false;
            
            // Send start command to server
            ws.send(JSON.stringify({ type: 'start' }));
        }
    });

    // Stop listening
    stopBtn.addEventListener('click', () => {
        if (isListening && ws && ws.readyState === WebSocket.OPEN) {
            isListening = false;
            currentCommand.textContent = 'Stopped';
            startBtn.disabled = false;
            stopBtn.disabled = true;
            
            // Send stop command to server
            ws.send(JSON.stringify({ type: 'stop' }));
        }
    });

    // Feature card click handlers
    featureCards.forEach(card => {
        card.addEventListener('click', () => {
            const feature = card.dataset.feature;
            if (ws && ws.readyState === WebSocket.OPEN) {
                ws.send(JSON.stringify({
                    type: 'feature',
                    feature: feature
                }));
            }
        });
    });

    // Initialize WebSocket connection
    initializeWebSocket();

    // Handle window close
    window.addEventListener('beforeunload', () => {
        if (ws) {
            ws.close();
        }
    });
}); 