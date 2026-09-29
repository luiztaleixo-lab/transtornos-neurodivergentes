---
type: community
cohesion: 0.18
members: 12
---

# Clinical Knowledge & Chatbot

**Cohesion:** 0.18 - loosely connected
**Members:** 12 nodes

## Members
- [[10 Clinical Conditions JSON]] - document - static/data/conditions.json
- [[11 Private Chat View (private_chat.html)]] - document - templates/private_chat.html
- [[Anti-Image Filter Security]] - code - app.py
- [[Authentication & Session (Flask-Login)]] - code - app.py
- [[Chatbot Client Delay & Typing (chatbot.js)]] - code - static/js/chatbot.js
- [[Chatbot Logic & Topics (chatbot.py)]] - code - chatbot.py
- [[Conditions Catalog View (index.html)]] - document - templates/index.html
- [[Flask Application Core (app.py)]] - code - app.py
- [[Forum & Room Chat View (forum.html)]] - document - templates/forum.html
- [[Interactive Chatbot View (chatbot.html)]] - document - templates/chatbot.html
- [[Real-Time Engine (Flask-SocketIO)]] - code - app.py
- [[SocketIO Client Coordinator (chat.js)]] - code - static/js/chat.js

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Clinical_Knowledge_&_Chatbot
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_Frontend Views & Design System]]

## Top bridge nodes
- [[Flask Application Core (app.py)]] - degree 6, connects to 1 community