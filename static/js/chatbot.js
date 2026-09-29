// chatbot.js - Gerenciador interativo com tempo de espera / digitacao

document.addEventListener('DOMContentLoaded', () => {
    const topicButtons = document.querySelectorAll('.btn-topic-selector');
    const queryForm = document.getElementById('chatbotQueryForm');
    const queryInput = document.getElementById('chatbotQueryInput');
    const responseTag = document.getElementById('responseTopicTag');
    const responseText = document.getElementById('chatbotResponseText');
    const statusIndicator = document.getElementById('responseStatusIndicator');

    let currentTimeout = null;

    function simulateTypingAndFetch(payload, topicTitle) {
        if (currentTimeout) clearTimeout(currentTimeout);

        if (statusIndicator) statusIndicator.style.display = 'inline-flex';
        if (responseTag) responseTag.textContent = topicTitle || 'Consultando...';
        if (responseText) {
            responseText.style.opacity = '0.5';
            responseText.textContent = 'Buscando orientacao tecnica sobre o tema solicitado...';
        }

        // Tempo de espera deliberado entre a pergunta e a resposta (850ms)
        const delayMs = 850;

        currentTimeout = setTimeout(async () => {
            try {
                const res = await fetch('/api/chatbot', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                const data = await res.json();

                if (statusIndicator) statusIndicator.style.display = 'none';
                if (responseTag) responseTag.textContent = data.title || 'Orientacao';
                if (responseText) {
                    responseText.style.opacity = '1';
                    responseText.textContent = data.response;
                }
            } catch (err) {
                if (statusIndicator) statusIndicator.style.display = 'none';
                if (responseText) {
                    responseText.style.opacity = '1';
                    responseText.textContent = 'Nao foi possivel carregar a resposta no momento. Tente novamente.';
                }
            }
        }, delayMs);
    }

    topicButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            topicButtons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            const topicKey = btn.getAttribute('data-topic');
            const topicTitle = btn.textContent.trim();

            simulateTypingAndFetch({ topic: topicKey }, topicTitle);
        });
    });

    if (queryForm) {
        queryForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const text = queryInput.value.trim();
            if (!text) return;

            topicButtons.forEach(b => b.classList.remove('active'));
            simulateTypingAndFetch({ query: text }, 'Busca: ' + text);
        });
    }
});
