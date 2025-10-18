document.addEventListener('DOMContentLoaded', function() {
    const chatContainer = document.getElementById('chat-container');
    const adminQuestionContainer = document.getElementById('admin-question-container');
    const adminQuestionText = document.getElementById('admin-question-text');
    const dismissQuestionBtn = document.getElementById('dismiss-question-btn');

    function fetchMessages() {
        fetch('/chat/messages')
            .then(response => response.json())
            .then(messages => {
                chatContainer.innerHTML = '';
                let lastQuestion = null;

                messages.forEach(msg => {
                    const msgElement = document.createElement('div');
                    msgElement.classList.add('chat-message', 'p-2', 'rounded', 'mb-2');

                    if (msg.type === 'message') {
                        msgElement.textContent = msg.content;
                        msgElement.style.backgroundColor = '#4a4a4a';
                    } else if (msg.type === 'question') {
                        // Keep track of the last question
                        lastQuestion = msg.content;
                    }
                    chatContainer.appendChild(msgElement);
                });

                // Display the last question received
                if (lastQuestion) {
                    adminQuestionText.textContent = lastQuestion;
                    adminQuestionContainer.style.display = 'block';
                } else {
                    adminQuestionContainer.style.display = 'none';
                }

                chatContainer.scrollTop = chatContainer.scrollHeight;
            })
            .catch(error => console.error('Error fetching chat messages:', error));
    }

    dismissQuestionBtn.addEventListener('click', function() {
        adminQuestionContainer.style.display = 'none';
    });

    // Fetch messages every 3 seconds
    setInterval(fetchMessages, 3000);
    fetchMessages(); // Initial fetch
});
