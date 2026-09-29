# Graph Report - .  (2026-08-26)

## Corpus Check
- 17 files · ~12,000 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 60 nodes · 64 edges · 8 communities detected
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 6 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## God Nodes (most connected - your core abstractions)
1. `Flask Application Core (app.py)` - 6 edges
2. `User` - 5 edges
3. `SQLAlchemy Models (models.py)` - 4 edges
4. `contains_image_content()` - 3 edges
5. `sanitize_message()` - 3 edges
6. `load_conditions()` - 3 edges
7. `handle_forum_message()` - 3 edges
8. `handle_private_message()` - 3 edges
9. `Real-Time Engine (Flask-SocketIO)` - 3 edges
10. `User Model (User)` - 3 edges

## Surprising Connections (you probably didn't know these)
- `Flask Application Core (app.py)` --reads--> `10 Clinical Conditions JSON`  [EXTRACTED]
  app.py → static/data/conditions.json
- `Profile Customizer View (profile.html)` --edits--> `User Model (User)`  [EXTRACTED]
  templates/profile.html → models.py
- `User Search View (search.html)` --queries--> `User Model (User)`  [EXTRACTED]
  templates/search.html → models.py
- `Forum & Room Chat View (forum.html)` --includes--> `SocketIO Client Coordinator (chat.js)`  [EXTRACTED]
  templates/forum.html → static/js/chat.js
- `1:1 Private Chat View (private_chat.html)` --includes--> `SocketIO Client Coordinator (chat.js)`  [EXTRACTED]
  templates/private_chat.html → static/js/chat.js

## Communities

### Community 0 - "Flask Backend & WebSockets"
Cohesion: 0.11
Nodes (0): 

### Community 1 - "SQLAlchemy Data Layer"
Cohesion: 0.15
Nodes (5): ForumMessage, ForumRoom, PrivateMessage, User, UserMixin

### Community 2 - "Clinical Knowledge & Chatbot"
Cohesion: 0.18
Nodes (12): Authentication & Session (Flask-Login), Chatbot Logic & Topics (chatbot.py), Chatbot Client Delay & Typing (chatbot.js), SocketIO Client Coordinator (chat.js), 10 Clinical Conditions JSON, Flask Application Core (app.py), Anti-Image Filter Security, Real-Time Engine (Flask-SocketIO) (+4 more)

### Community 3 - "Frontend Views & Design System"
Cohesion: 0.33
Nodes (6): SQLAlchemy Models (models.py), Forum Models (ForumRoom, ForumMessage), Private Message Model (PrivateMessage), User Model (User), Profile Customizer View (profile.html), User Search View (search.html)

### Community 4 - "Community 4"
Cohesion: 0.67
Nodes (4): contains_image_content(), handle_forum_message(), handle_private_message(), sanitize_message()

### Community 5 - "Community 5"
Cohesion: 0.67
Nodes (3): condition_detail(), index(), load_conditions()

### Community 6 - "Community 6"
Cohesion: 1.0
Nodes (0): 

### Community 7 - "Community 7"
Cohesion: 1.0
Nodes (1): Editorial Design System CSS (style.css)

## Knowledge Gaps
- **10 isolated node(s):** `Authentication & Session (Flask-Login)`, `Forum Models (ForumRoom, ForumMessage)`, `Private Message Model (PrivateMessage)`, `Conditions Catalog View (index.html)`, `Forum & Room Chat View (forum.html)` (+5 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 6`** (2 nodes): `chatbot.py`, `get_response()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 7`** (1 nodes): `Editorial Design System CSS (style.css)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Flask Application Core (app.py)` connect `Clinical Knowledge & Chatbot` to `Frontend Views & Design System`?**
  _High betweenness centrality (0.063) - this node is a cross-community bridge._
- **Why does `SQLAlchemy Models (models.py)` connect `Frontend Views & Design System` to `Clinical Knowledge & Chatbot`?**
  _High betweenness centrality (0.039) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `contains_image_content()` (e.g. with `handle_forum_message()` and `handle_private_message()`) actually correct?**
  _`contains_image_content()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `sanitize_message()` (e.g. with `handle_forum_message()` and `handle_private_message()`) actually correct?**
  _`sanitize_message()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Authentication & Session (Flask-Login)`, `Forum Models (ForumRoom, ForumMessage)`, `Private Message Model (PrivateMessage)` to the rest of the system?**
  _10 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Flask Backend & WebSockets` be split into smaller, more focused modules?**
  _Cohesion score 0.11 - nodes in this community are weakly interconnected._