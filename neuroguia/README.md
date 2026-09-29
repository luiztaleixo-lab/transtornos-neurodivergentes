# NeuroGuia - Portal de Neurodesenvolvimento e Condições Relacionadas

Plataforma web desenvolvida em **Python (Flask)** com foco educativo e comunitário sobre transtornos do neurodesenvolvimento e condições correlatas.

---

## Recursos e Funcionalidades

- **Guia Clínico das 10 Condições**: Apresentação detalhada em aba única (O que é, Sintomas e Características, Critérios e Diagnóstico, Abordagens e Apoio, Mitos e Fatos) com âncoras internas.
- **Fórum Comunitário em Tempo Real**: Salas temáticas criadas pela comunidade com WebSocket bidirecional via `Flask-SocketIO`.
- **Chat Privado 1:1**: Conversas privadas em tempo real entre membros cadastrados utilizando a mesma infraestrutura de WebSockets.
- **Segurança Rigorosa no Backend**: Bloqueio ativo de qualquer envio de imagens ou links de imagens no chat (regex no backend).
- **Assistente Interativo (Chatbot)**: 13 tópicos clínicos com delay de espera/digitação humanizado e busca livre por palavras-chave.
- **Sistema de Usuários e Perfis**: Cadastro, login seguro com hash criptográfico (`werkzeug.security`), biografia e personalização da cor do avatar.
- **Busca de Membros**: Localização rápida de usuários para envio de mensagens privadas.
- **Design System Editorial & Redação Sem Emojis**: Paleta sóbria e elegante inspirada em publicações científicas com tipografia *Fraunces* e *Plus Jakarta Sans*. Totalmente livre de emojis.
- **Grafo de Conhecimento**: Documentação arquitetural gerada com o `Graphify` na pasta `graphify-out/`.

---

## Estrutura do Projeto

```text
neuroguia/
├── app.py                      # Servidor Flask, rotas, segurança e eventos SocketIO
├── models.py                   # Modelos de banco de dados (User, ForumRoom, ForumMessage, PrivateMessage)
├── chatbot.py                  # Base de conhecimento e lógica do Chatbot (13 tópicos)
├── requirements.txt            # Dependências Python
├── static/
│   ├── css/
│   │   └── style.css           # Folha de estilos editorial (sem emojis)
│   ├── js/
│   │   ├── chat.js             # Comunicação SocketIO do fórum e chat privado
│   │   ├── chatbot.js          # Controle interativo com delay de digitação
│   │   └── main.js             # Filtro dinâmico do catálogo clínico
│   └── data/
│       └── conditions.json     # Base clínica das 10 condições
├── templates/
│   ├── base.html               # Layout base com aviso educativo fixo
│   ├── index.html              # Catálogo clínico
│   ├── forum.html              # Fórum de discussões
│   ├── private_chat.html       # Janela de chat privado 1:1
│   ├── search.html             # Busca de usuários
│   ├── profile.html            # Edição de perfil
│   ├── user_profile.html       # Visualização pública de perfis
│   ├── auth.html               # Login e cadastro
│   └── chatbot.html            # Interface do assistente interativo
└── graphify-out/               # Grafo de conhecimento gerado pelo Graphify
    ├── graph.json              # Grafo em formato JSON
    ├── graph.html              # Visualizador interativo do grafo
    ├── GRAPH_REPORT.md         # Relatório analítico de arquitetura
    └── obsidian/               # Notas integradas para Obsidian
```

---

## Como Instalar e Rodar

### 1. Criar o Ambiente Virtual (opcional, mas recomendado)
```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

### 2. Instalar as Dependências
```powershell
pip install -r requirements.txt
```

### 3. Iniciar o Servidor
```powershell
python app.py
```

O portal estará disponível em: **`http://127.0.0.1:5000`**
