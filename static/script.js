document.addEventListener("DOMContentLoaded", function() {
    appendBotMessage("How can I assist you?");
});

const chatIcon = document.querySelector(".chat-icon");
const chatBox = document.querySelector(".chat-box");
const userInputElement = document.getElementById("user-input");
const sendButton = document.getElementById("send-btn");
const chatMessagesContainer = document.getElementById("chat-messages");
const closeBtn = document.getElementById("close-btn");
const refreshButton = document.querySelector(".refresh-button");

chatIcon.addEventListener("click", function () {
    chatBox.style.display = "block";
    chatIcon.style.display = "none";
});

closeBtn.addEventListener("click", function () {
    chatBox.style.display = "none";
    chatIcon.style.display = "block";
});

refreshButton.addEventListener("click", function () {
    // Clear previous messages
    chatMessagesContainer.innerHTML = "";

    // Restart the conversation
    appendBotMessage("Hello! How can I assist you?");

    chatBox.style.display = "block";
    chatIcon.style.display = "none";
});

userInputElement.addEventListener("keydown", function (event) {
    if (event.key === "Enter") {
        event.preventDefault();
        sendMessage();
    }
});

sendButton.addEventListener("click", sendMessage);

function sendMessage() {
    const userInput = userInputElement.value;
    if (userInput.trim() !== "") {
        appendUserMessage(userInput);
        userInputElement.value = "";

        // Send the user input to your Flask backend and get the bot's response
        fetch('/get_response', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ input: userInput })
        })
        .then(response => response.json())
        .then(data => {
            appendBotMessage(data.response);
        })
        .catch(error => {
            console.error('Error:', error);
        }); 
    }
}

function appendUserMessage(message) {
    const userMessageElement = document.createElement("div");
    userMessageElement.className = "user-message";
    userMessageElement.textContent = message;
    chatMessagesContainer.appendChild(userMessageElement);
    chatMessagesContainer.scrollTop = chatMessagesContainer.scrollHeight;
}

function appendBotMessage(message) {
    const botMessageElement = document.createElement("div");
    botMessageElement.className = "bot-message";
    botMessageElement.textContent = message;
    chatMessagesContainer.appendChild(botMessageElement);
    chatMessagesContainer.scrollTop = chatMessagesContainer.scrollHeight;
}
