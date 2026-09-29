// main.js - Comportamentos gerais da interface e filtro de condicoes

document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('conditionSearchInput');
    const conditionLinks = document.querySelectorAll('.condition-item-link');

    if (searchInput && conditionLinks.length > 0) {
        searchInput.addEventListener('input', (e) => {
            const term = e.target.value.toLowerCase().trim();

            conditionLinks.forEach(link => {
                const name = link.getAttribute('data-name') || '';
                const sigla = link.getAttribute('data-sigla') || '';

                if (name.includes(term) || sigla.includes(term)) {
                    link.style.display = 'flex';
                } else {
                    link.style.display = 'none';
                }
            });
        });
    }
});
