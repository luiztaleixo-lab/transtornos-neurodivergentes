---
type: community
cohesion: 0.15
members: 13
---

# SQLAlchemy Data Layer

**Cohesion:** 0.15 - loosely connected
**Members:** 13 nodes

## Members
- [[.check_password()]] - code - models.py
- [[.set_password()]] - code - models.py
- [[.to_dict()_2]] - code - models.py
- [[.to_dict()_1]] - code - models.py
- [[.to_dict()_3]] - code - models.py
- [[.to_dict()]] - code - models.py
- [[ForumMessage]] - code - models.py
- [[ForumRoom]] - code - models.py
- [[PrivateMessage]] - code - models.py
- [[User]] - code - models.py
- [[UserMixin]] - code
- [[models.py]] - code - models.py
- [[utc_now()]] - code - models.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/SQLAlchemy_Data_Layer
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_Flask Backend & WebSockets]]

## Top bridge nodes
- [[models.py]] - degree 6, connects to 1 community