// chat.js - Gerenciador SocketIO unificado para Forum e Chat Privado

document.addEventListener('DOMContentLoaded', () => {
    const socket = io();

    function escapeHTML(str) {
        const div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
    }

    function scrollToBottom(el) {
        if (el) {
            el.scrollTop = el.scrollHeight;
        }
    }

    socket.on('error_message', (data) => {
        if (data && data.error) {
            alert(data.error);
        }
    });

    // ----------------- CHAT DO FORUM -----------------
    const forumForm = document.getElementById('forumMessageForm');
    const forumInput = document.getElementById('forumMessageInput');
    const forumContainer = document.getElementById('forumMessagesContainer');

    if (forumForm && forumContainer) {
        const roomId = forumForm.getAttribute('data-room-id');
        scrollToBottom(forumContainer);

        socket.emit('join_forum', { room_id: roomId });

        forumForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const content = forumInput.value.trim();
            if (!content) return;

            const imgRegex = /\.(png|jpe?g|gif|webp|svg|bmp|tiff)(\?.*)?$/i;
            if (imgRegex.test(content) || /<img/i.test(content) || /data:image\//i.test(content)) {
                alert('O envio de imagens ou links de imagens e proibido no sistema.');
                return;
            }

            socket.emit('send_forum_message', {
                room_id: roomId,
                content: content
            });

            forumInput.value = '';
        });

        socket.on('new_forum_message', (msg) => {
            const emptyState = document.getElementById('emptyChatState');
            if (emptyState) emptyState.remove();

            const row = document.createElement('div');
            row.className = 'chat-message-row';

            row.innerHTML = `
                <span class="message-avatar" style="background-color: ${escapeHTML(msg.avatar_color || '#4a6b5d')};">
                    ${escapeHTML((msg.username || '?').substring(0, 2).toUpperCase())}
                </span>
                <div class="message-bubble">
                    <div class="message-meta">
                        <strong class="message-author">
                            <a href="/perfil/${msg.user_id}">${escapeHTML(msg.username)}</a>
                        </strong>
                        <time class="message-time">${escapeHTML(msg.created_at || '')}</time>
                    </div>
                    <div class="message-text">${escapeHTML(msg.content)}</div>
                </div>
            `;

            forumContainer.appendChild(row);
            scrollToBottom(forumContainer);
        });
    }

    const openModalBtn = document.getElementById('openCreateRoomBtn');
    const closeModalBtn = document.getElementById('closeCreateRoomBtn');
    const cancelModalBtn = document.getElementById('cancelCreateRoomBtn');
    const modal = document.getElementById('createRoomModal');

    if (openModalBtn && modal) {
        openModalBtn.addEventListener('click', () => modal.style.display = 'flex');
        if (closeModalBtn) closeModalBtn.addEventListener('click', () => modal.style.display = 'none');
        if (cancelModalBtn) cancelModalBtn.addEventListener('click', () => modal.style.display = 'none');
    }

    // ----------------- CHAT PRIVADO 1:1 -----------------
    const privateForm = document.getElementById('privateMessageForm');
    const privateInput = document.getElementById('privateMessageInput');
    const privateContainer = document.getElementById('privateMessagesContainer');

    if (privateForm && privateContainer) {
        const recipientId = privateForm.getAttribute('data-recipient-id');
        const roomName = privateForm.getAttribute('data-room-name');
        scrollToBottom(privateContainer);

        socket.emit('join_private', { room_name: roomName });

        privateForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const content = privateInput.value.trim();
            if (!content) return;

            const imgRegex = /\.(png|jpe?g|gif|webp|svg|bmp|tiff)(\?.*)?$/i;
            if (imgRegex.test(content) || /<img/i.test(content) || /data:image\//i.test(content)) {
                alert('O envio de imagens ou links de imagens e proibido no chat privado.');
                return;
            }

            socket.emit('send_private_message', {
                recipient_id: parseInt(recipientId),
                content: content
            });

            privateInput.value = '';
        });

        socket.on('new_private_message', (msg) => {
            const emptyState = document.getElementById('emptyPrivateChatState');
            if (emptyState) emptyState.remove();

            const row = document.createElement('div');
            row.className = 'chat-message-row';

            row.innerHTML = `
                <span class="message-avatar" style="background-color: ${escapeHTML(msg.sender_avatar_color || '#4a6b5d')};">
                    ${escapeHTML((msg.sender_username || '?').substring(0, 2).toUpperCase())}
                </span>
                <div class="message-bubble">
                    <div class="message-meta">
                        <strong class="message-author">${escapeHTML(msg.sender_username)}</strong>
                        <time class="message-time">${escapeHTML(msg.created_at || '')}</time>
                    </div>
                    <div class="message-text">${escapeHTML(msg.content)}</div>
                </div>
            `;

            privateContainer.appendChild(row);
            scrollToBottom(privateContainer);
        });
    }
});
