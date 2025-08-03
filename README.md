# gdmongolite Documentation
gdmongolite is a zero-boilerplate, schema-first, multi-driver MongoDB toolkit that unifies sync and async drivers, Pydantic validation, migrations, telemetry hooks, and a CLI into one package.

## Table of Contents
1. Installation
2. Configuration
3. Defining Schemas
4. Connecting to MongoDB
5. CRUD Operations
6. Advanced Querying
7. Migrations
8. Transactions
9. Change Streams
10. Interactive Shell
11. Model Generation
12. Telemetry Hooks
13. CLI Reference
14. Testing
15. Project Layout
16. Best Practices
17. FAQ

## 1. Installation
Install from PyPI:
```bash
pip install gdmongolite
```
For development tools:
```bash
pip install gdmongolite[dev]
```

## 2. Configuration
Create a `.env` file in your project root:
```
MONGO_URI="mongodb://localhost:27017"
MONGO_DB="myapp"
MONGO_MAX_POOL=50
MONGO_MIN_POOL=5
MONGO_TIMEOUT_MS=30000
```
gdmongolite reads these automatically via Pydantic `BaseSettings`. You can also override via environment variables:
```bash
export MONGO_URI="mongodb://remotehost:27017"
```

## 3. Defining Schemas
All schemas inherit from `Schema`. Collection names are inferred:
```python
# src/gdmongolite/schema/__init__.py
from gdmongolite import DB, Schema, Email, Positive

db = DB()  # Uses .env

class User(Schema):
    name: str
    email: Email          # Validates format
    age: Positive       # Must be >0
    tags: list[str] = []  # Default empty list
```
Now you can use `db.User` for operations.

## 4. Connecting to MongoDB
Instantiate the singleton `DB` facade:
```python
from gdmongolite import DB

# Async context (default)
db = DB()

# Explicit sync mode
db_sync = DB(mode="sync")

# Or specify URI directly
db2 = DB("mongodb://localhost:27017", database="myapp")
```
Close connections when done:
```python
await db.close()
db_sync.close_sync()
```

## 5. CRUD Operations
| Operation      | Async                                        | Sync                                          |
|----------------|----------------------------------------------|-----------------------------------------------|
| Insert one     | `await db.User.insert(data)`                 | `db.User.insert_sync(data)`                   |
| Find many      | `await db.User.find(**filters).to_list()`    | `db.User.find(**filters).to_list_sync()`      |
| Update one     | `await db.User.update(filter, update)`       | `db.User.update_sync(filter, update)`         |
| Delete many    | `await db.User.delete(**filters)`            | `db.User.delete_sync(**filters)`              |
Returned value is a standardized `QueryResponse`:
```python
{
  "success": True,
  "data": [...],
  "count": 3,
  "message": "Found 3 documents"
}
```

## 6. Advanced Querying
Filter operators:
- `__gt`, `__gte`, `__lt`, `__lte`
- `__in`, `__nin`
- `__regex`
Logical operators:
```python
from gdmongolite import OR, AND

query = OR(age__lt=18, AND(tags__in=["vip"], is_active=True))
results = await db.User.find(query).to_list()
```
Pagination:
```python
await db.User.find(age__gte=18).limit(10).skip(20).to_list()
```
Aggregation:
```python
pipeline = [
  {"$"match": {"age": {"$"gte": 18}}},
  {"$"group": {"_id": None, "avg_age": {"$"avg": "$age"}}}
]
stats = await db.User.aggregate(pipeline).to_list()
```

## 7. Migrations
Generate migration scripts when schemas change:
```bash
gdmongolite migrate
```
- Creates timestamped scripts under `migrations/`
- Compare current models to database collections
- Apply on startup:
```python
await db.migrate_all()
```

## 8. Transactions
Support for ACID transactions:
```python
async with db.transaction():
    await db.Order.insert({...})
    await db.Inventory.update(...)
# Sync:
with db.transaction_sync():
    db.Order.insert_sync({...})
    db.Inventory.update_sync(...)
```

## 9. Change Streams
Listen to real-time changes:
```python
async for change in db.User.watch(pipeline=[]):
    print("Change detected:", change)
```

## 10. Interactive Shell
Launch REPL with `db` preloaded:
```bash
gdmongolite shell
```
Inside the shell:
```python
await db.User.insert({"name":"Bob", "email":"bob@x.com", "age":25})
users = await db.User.find().to_list()
```

## 11. Model Generation
Scaffold schemas from existing collections:
```bash
gdmongolite gen-model --collection products --out src/models/product.py
```
- Samples documents
- Infers field names and types

## 12. Telemetry Hooks
Register hooks on query events:
```python
from gdmongolite import DB

@DB.on("pre_query")
def before(collection, filt, opts):
    print(f"About to query {collection}: {filt}")

@DB.on("post_query")
def after(collection, result):
    print(f"{collection} returned {result.count} docs in {result.duration}ms")
```

## 13. CLI Reference
```bash
gdmongolite --help
# Commands:
# migrate     Generate and apply migration scripts
# shell       Launch interactive REPL
# gen-model   Scaffold a schema from an existing collection
# test        Run test suite
```

## 14. Testing
```bash
pip install gdmongolite[dev]
pytest --maxfail=1 --disable-warnings -q
```
- Coverage ≥ 95%
- Uses `pytest-asyncio` for async tests

## 15. Project Layout
```
gdmongolite/
├── src/gdmongolite/
│   ├── __init__.py
│   ├── core.py
│   ├── schema.py
│   ├── query.py
│   ├── migrate.py
│   ├── telemetry.py
│   ├── cli.py
│   ├── config.py
│   └── utils.py
├── migrations/      # Auto-generated scripts
├── tests/
├── README.md
├── LICENSE
├── pyproject.toml
└── .env
```

## 16. Best Practices
- Keep schemas small and focused
- Version your migrations and commit them
- Use telemetry hooks to capture performance metrics
- Run CI on every PR, testing multiple Python and dependency versions
- Document any custom extensions or plugins

## 17. FAQ
**Q: Can I override default index creation?**
A: Yes — define `class Meta: indexes = [...]` inside your `Schema` subclass.
**Q: How do I handle large result sets?**
A: Use cursors with `batch_size` and `to_list(batch_size=100)`.
**Q: Can I use gdmongolite with FastAPI?**
A: Absolutely—instantiate `db` at startup and import your schemas into your routers.

**gdmongolite** empowers you with a single, coherent API for all MongoDB needs—schema definition, validation, querying, migrations, transactions, change streams, telemetry, and CLI tooling—ensuring you never touch low-level driver code again.