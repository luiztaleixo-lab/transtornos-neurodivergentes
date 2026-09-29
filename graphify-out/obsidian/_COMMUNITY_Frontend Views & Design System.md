---
type: community
cohesion: 0.33
members: 6
---

# Frontend Views & Design System

**Cohesion:** 0.33 - loosely connected
**Members:** 6 nodes

## Members
- [[Forum Models (ForumRoom, ForumMessage)]] - code - models.py
- [[Private Message Model (PrivateMessage)]] - code - models.py
- [[Profile Customizer View (profile.html)]] - document - templates/profile.html
- [[SQLAlchemy Models (models.py)]] - code - models.py
- [[User Model (User)]] - code - models.py
- [[User Search View (search.html)]] - document - templates/search.html

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Frontend_Views_&_Design_System
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_Clinical Knowledge & Chatbot]]

## Top bridge nodes
- [[SQLAlchemy Models (models.py)]] - degree 4, connects to 1 community