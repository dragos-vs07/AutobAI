let currentConversationId = null;

function display_conversation(conversation_id, otherUsername)
{
    const messagesArea = document.getElementById("messages_area");
    messagesArea.innerHTML = '';
    currentConversationId = conversation_id;

    socket.emit("join", { conversation_id: conversation_id });

    fetch(`/API/messages/${conversation_id}`).then(response => response.json())
    .then( data => {
        if (data.length)
            for (m of data)
            {
            const message = document.createElement("p");
            message.textContent = m.content;

            if(m.user_id == userId) // means this is a message from the current user
                message.classList.add("current_user");
            else
                message.classList.add("other_user");
            
             message.classList.add("message");

            messagesArea.appendChild(message);
            document.getElementById("top_username").textContent = otherUsername;

            }
        else
        {
            const message = document.createElement("p");
            message.textContent = "No messages yet";
            messagesArea.appendChild(message);
        }
    })
}

document.getElementById("message_form").addEventListener("submit",function(e){
    e.preventDefault();

    const input = document.getElementById("message_input");
    const content = input.value.trim();


    if (!content || !currentConversationId) return;

    const message = document.createElement("p");
    message.textContent = content;

   
    message.classList.add("current_user");     
    message.classList.add("message");
             
    document.getElementById("messages_area").appendChild(message);

    socket.emit("send_message", {
        conversation_id: currentConversationId,
        content: content
    });

    
    input.value = "";
});

socket.on("new_message", function(data) {
    if(data.conversation_id == currentConversationId)
    {
        const message = document.createElement("div");
        const username = document.createElement("p");
        const content = document.createElement("p");

        username.textContent = data.sender_username;
        content.textContent = data.content;

        message.appendChild(username);
        message.appendChild(content);

        document.getElementById("messages_area").appendChild(message);
    }
    document.getElementById(`last_message_${data.conversation_id}`).textContent = data.content;
});