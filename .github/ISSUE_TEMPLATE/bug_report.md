---
name: Bug report
about: Create a report to help us improve gdmongolite
title: '[BUG] '
labels: 'bug'
assignees: 'ganeshdatta23'

---

**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Import gdmongolite with '...'
2. Define schema '....'
3. Execute operation '....'
4. See error

**Expected behavior**
A clear and concise description of what you expected to happen.

**Code Example**
```python
from gdmongolite import DB, Schema, FieldTypes

# Your code that reproduces the issue
class User(Schema):
    name: FieldTypes.Name
    
db = DB()
# ... rest of your code
```

**Error Message**
```
Paste the full error message here
```

**Environment (please complete the following information):**
- OS: [e.g. Windows 11, macOS 13, Ubuntu 22.04]
- Python version: [e.g. 3.11.0]
- gdmongolite version: [e.g. 1.0.1]
- MongoDB version: [e.g. 7.0]

**Additional context**
Add any other context about the problem here.