# gdmongolite v1.0.0 - Complete Feature Guide & PyPI Publication

## Installation
```bash
pip install gdmongolite
```

## 1. Basic Setup & Connection

### Simple Connection
```python
from gdmongolite import DB, Schema, Email, FieldTypes

# Auto-connects to localhost:27017
db = DB()

# Custom connection
db = DB(uri="mongodb://localhost:27017", database="myapp")

# Production connection
db = DB(uri="mongodb+srv://user:pass@cluster.mongodb.net/", database="production")
```

### Environment Variables
```bash
# .env file
MONGO_URI=mongodb://localhost:27017
MONGO_DB=myapp
MONGO_MAX_POOL=50
MONGO_MIN_POOL=5
MONGO_TIMEOUT_MS=30000
```

## 2. Schema Definition & Field Types

### Basic Schema
```python
class User(Schema):
    name: FieldTypes.Name              # 1-100 chars
    email: Email                       # Email validation
    age: FieldTypes.Age               # 0-150 range
    role: str = "user"                # Default value
    is_active: bool = True            # Boolean field
    tags: list[str] = []              # List field
    created_at: datetime = datetime.now()  # DateTime field

# Register schema
db.register_schema(User)
```

### All Field Types
```python
class CompleteSchema(Schema):
    # String fields
    name: FieldTypes.Name              # 1-100 chars
    username: FieldTypes.Username     # 3-30 chars, alphanumeric
    password: FieldTypes.Password     # 8-128 chars
    title: FieldTypes.Title           # 1-200 chars
    description: FieldTypes.Description  # Max 1000 chars
    content: FieldTypes.Content       # Max 10000 chars
    
    # Numeric fields
    age: FieldTypes.Age               # 0-150
    price: FieldTypes.Price           # Non-negative float
    rating: FieldTypes.Rating         # 0-5 range
    
    # Special fields
    email: Email                      # Email validation
    url: FieldTypes.URL              # URL validation
    phone: FieldTypes.Phone          # Phone validation
    
    # MongoDB types
    object_id: ObjectId              # MongoDB ObjectId
    created_at: DateTime             # DateTime field
```

## 3. CRUD Operations

### Create (Insert)
```python
# Single document
user = await db.User.insert({
    "name": "John Doe",
    "email": "john@example.com",
    "age": 30,
    "role": "admin"
})
print(f"Inserted: {user.message}")

# Multiple documents
users = await db.User.insert([
    {"name": "Alice", "email": "alice@example.com", "age": 25},
    {"name": "Bob", "email": "bob@example.com", "age": 35}
])
print(f"Inserted {users.count} users")

# Using schema objects
user_obj = User(name="Carol", email="carol@example.com", age=28)
result = await db.User.insert(user_obj)

# Sync version
user_sync = db.User.insert_sync({"name": "Dave", "email": "dave@example.com", "age": 32})
```

### Read (Find/Query)
```python
# Find all
all_users = await db.User.find().to_list()

# Find with filters
adults = await db.User.find(age__gte=18).to_list()
admins = await db.User.find(role="admin").to_list()
active_users = await db.User.find(is_active=True).to_list()

# Complex filters
complex_query = await db.User.find(
    age__gte=18,
    age__lt=65,
    is_active=True,
    role__in=["user", "admin", "moderator"]
).to_list()

# Find one document
user = await db.User.find(email="john@example.com").first()
if user:
    print(f"Found user: {user['name']}")

# Pagination
page1 = await db.User.find().skip(0).limit(10).to_list()
page2 = await db.User.find().skip(10).limit(10).to_list()

# Sorting
newest_users = await db.User.find().sort("-created_at").to_list()
oldest_users = await db.User.find().sort("created_at").to_list()
alphabetical = await db.User.find().sort("name").to_list()

# Count documents
total_users = await db.User.find().count()
adult_count = await db.User.find(age__gte=18).count()
admin_count = await db.User.find(role="admin").count()

# Sync versions
users_sync = db.User.find(age__gte=18).to_list_sync()
count_sync = db.User.find().count_sync()
```

### Update
```python
# Update many documents
result = await db.User.update(
    {"role": "user"},                    # Filter
    {"$set": {"role": "member"}}         # Update
)
print(f"Updated {result.count} documents")

# Update with MongoDB operators
await db.User.update(
    {"_id": user_id},
    {
        "$set": {"last_login": datetime.now()},
        "$inc": {"login_count": 1},
        "$push": {"tags": "active"},
        "$pull": {"tags": "inactive"}
    }
)

# Upsert (insert if not exists)
await db.User.update(
    {"email": "new@example.com"},
    {"$set": {"name": "New User", "age": 25}},
    upsert=True
)

# Sync version
result_sync = db.User.update_sync(
    {"role": "guest"}, 
    {"$set": {"role": "user"}}
)
```

### Delete
```python
# Delete documents
result = await db.User.delete(role="inactive")
print(f"Deleted {result.count} inactive users")

# Delete by multiple criteria
await db.User.delete(age__lt=13, is_active=False)

# Delete by ID
await db.User.delete(_id=user_id)

# Sync version
result_sync = db.User.delete_sync(role="spam")
```

## 4. Advanced Queries & Aggregations

### Basic Aggregations
```python
# Group by role
role_stats = await db.User.aggregate().group(
    "$role", 
    count={"$sum": 1},
    avg_age={"$avg": "$age"}
).execute()

# Statistical analysis
user_stats = await db.User.aggregate().group(
    None,
    total_users={"$sum": 1},
    avg_age={"$avg": "$age"},
    min_age={"$min": "$age"},
    max_age={"$max": "$age"},
    std_dev_age={"$stdDevPop": "$age"}
).execute()

# Date-based grouping
monthly_signups = await db.User.aggregate().group(
    {"$dateToString": {"format": "%Y-%m", "date": "$created_at"}},
    count={"$sum": 1}
).sort(_id=1).execute()
```

### Complex Aggregations
```python
# Multi-collection aggregation
order_analysis = await (
    db.Order.aggregate()
    .match(status="completed")
    .lookup("users", "user_id", "_id", "user_info")
    .unwind("user_info")
    .lookup("products", "product_ids", "_id", "product_info")
    .group(
        "$user_info.role",
        total_orders={"$sum": 1},
        total_revenue={"$sum": "$total"},
        avg_order_value={"$avg": "$total"},
        unique_customers={"$addToSet": "$user_id"}
    )
    .sort(total_revenue=-1)
    .execute()
)

# Text search
search_results = await db.User.aggregate().match(
    {"$text": {"$search": "john admin"}}
).execute()

# Geospatial queries
nearby_users = await db.User.aggregate().match({
    "location": {
        "$near": {
            "$geometry": {"type": "Point", "coordinates": [-73.9857, 40.7484]},
            "$maxDistance": 1000
        }
    }
}).execute()
```

## 5. FastAPI Integration

### Auto-Generated REST API
```python
from gdmongolite import create_fastapi_app

# Create complete REST API
app = create_fastapi_app(
    db,
    schemas=[User, Product, Order],
    title="My Powerful API",
    version="1.0.0",
    description="Auto-generated MongoDB API",
    enable_docs=True,
    enable_cors=True
)

# Automatically creates these endpoints:
# GET    /users/              - List users (with pagination, filtering, sorting)
# POST   /users/              - Create user
# GET    /users/{id}          - Get user by ID
# PUT    /users/{id}          - Update user
# DELETE /users/{id}          - Delete user
# POST   /users/search        - Advanced search
# GET    /users/count         - Count users
# GET    /users/aggregate     - Run aggregations
```

### Custom Endpoints
```python
@app.get("/analytics/dashboard")
async def analytics_dashboard():
    return {
        "total_users": await db.User.find().count(),
        "active_users": await db.User.find(is_active=True).count(),
        "total_orders": await db.Order.find().count(),
        "revenue": await db.Order.aggregate().group(
            None, total={"$sum": "$total"}
        ).execute(),
        "top_products": await db.Product.find().sort("-rating").limit(5).to_list()
    }

@app.get("/users/stats")
async def user_statistics():
    stats = await db.User.aggregate().group(
        None,
        total={"$sum": 1},
        avg_age={"$avg": "$age"},
        roles={"$addToSet": "$role"}
    ).execute()
    return stats[0] if stats else {}

# Run server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
```

## 6. Data Import/Export

### Export Data
```python
from gdmongolite import DataExporter

exporter = DataExporter(db)

# Export to JSON
await exporter.export_to_json(db.User, "users.json")
await exporter.export_to_json(
    db.User.find(role="admin"), 
    "admin_users.json"
)

# Export to CSV
await exporter.export_to_csv(db.User, "users.csv")
await exporter.export_to_csv(
    db.User.find(is_active=True),
    "active_users.csv",
    fields=["name", "email", "age", "role"]
)

# Export with custom query
await exporter.export_to_json(
    db.User.find(age__gte=18, role__in=["admin", "moderator"]),
    "staff_users.json"
)
```

### Import Data
```python
from gdmongolite import DataImporter

importer = DataImporter(db)

# Import from JSON
await importer.import_from_json("users.json", User)

# Import from CSV with field mapping
await importer.import_from_csv(
    "users.csv", 
    User,
    field_mapping={
        "full_name": "name",
        "email_address": "email",
        "user_age": "age",
        "user_role": "role"
    }
)

# Batch import for large datasets
await importer.batch_import(
    data_source="large_dataset.json",
    schema=User,
    batch_size=1000,
    validate=True,
    skip_errors=False
)

# Import with transformation
def transform_user(data):
    data["name"] = data["name"].title()
    data["email"] = data["email"].lower()
    return data

await importer.import_from_json(
    "users.json", 
    User, 
    transform_func=transform_user
)
```

## 7. Real-time Features

### WebSocket Integration
```python
from gdmongolite import WebSocketManager
from fastapi import WebSocket

@app.websocket("/ws/users")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    # Watch for changes in User collection
    async def on_user_change(change):
        await websocket.send_json({
            "type": "user_update",
            "operation": change["operationType"],
            "document_id": str(change["documentKey"]["_id"]),
            "data": change.get("fullDocument", {}),
            "timestamp": datetime.now().isoformat()
        })
    
    # Subscribe to real-time changes
    await db.User.watch_changes(on_user_change)

# Live queries
@app.websocket("/ws/live-query")
async def live_query_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    live_query = db.User.live_query(is_active=True)
    await live_query.subscribe(websocket)
```

### Change Streams
```python
# Monitor all changes
async def monitor_changes():
    async def handle_change(change):
        print(f"Change detected: {change['operationType']}")
        print(f"Collection: {change['ns']['coll']}")
        if change.get("fullDocument"):
            print(f"Document: {change['fullDocument']}")
    
    await db.User.watch_changes(handle_change)

# Monitor specific operations
async def monitor_inserts():
    async def handle_insert(change):
        if change["operationType"] == "insert":
            user = change["fullDocument"]
            print(f"New user registered: {user['name']} ({user['email']})")
    
    await db.User.watch_changes(handle_insert, operation_types=["insert"])
```

## 8. Security Features

### Password Management
```python
from gdmongolite import PasswordManager

password_manager = PasswordManager()

# Hash passwords
hashed = password_manager.hash_password("user_password123")
print(f"Hashed password: {hashed}")

# Verify passwords
is_valid = password_manager.verify_password("user_password123", hashed)
print(f"Password valid: {is_valid}")

# Generate secure passwords
secure_password = password_manager.generate_password(length=16)
print(f"Generated password: {secure_password}")
```

### JWT Authentication
```python
from gdmongolite import JWTManager
from fastapi import Depends, HTTPException

jwt_manager = JWTManager(secret_key="your-super-secret-key")

@app.post("/auth/login")
async def login(email: str, password: str):
    user = await db.User.find(email=email).first()
    if not user:
        raise HTTPException(404, "User not found")
    
    if not password_manager.verify_password(password, user["password_hash"]):
        raise HTTPException(401, "Invalid password")
    
    token = jwt_manager.create_token({
        "user_id": str(user["_id"]),
        "email": user["email"],
        "role": user["role"]
    })
    
    return {"access_token": token, "token_type": "bearer"}

@app.get("/auth/profile")
async def get_profile(current_user=Depends(jwt_manager.get_current_user)):
    return {
        "user_id": current_user["user_id"],
        "email": current_user["email"],
        "role": current_user["role"]
    }

@app.get("/admin/users")
async def admin_only(current_user=Depends(jwt_manager.require_role("admin"))):
    return await db.User.find().to_list()
```

## 9. Caching System

### Enable Caching
```python
from gdmongolite import add_caching_to_db

# Enable caching with default settings
cached_db = add_caching_to_db(db)

# Cached queries (automatic)
users = await cached_db.User.find(role="admin").to_list()  # Database query
users = await cached_db.User.find(role="admin").to_list()  # From cache

# Manual caching
@cached_db.cached(ttl=300)  # Cache for 5 minutes
async def expensive_operation():
    return await db.Order.aggregate().match(
        status="completed"
    ).group(
        "$user_id", 
        total_spent={"$sum": "$total"}
    ).sort(total_spent=-1).limit(10).execute()

result = await expensive_operation()  # Database query
result = await expensive_operation()  # From cache
```

### Cache Management
```python
# Cache statistics
cache_stats = cached_db.get_cache_stats()
print(f"Cache hit rate: {cache_stats['hit_rate']:.2%}")
print(f"Total queries: {cache_stats['total_queries']}")
print(f"Cache hits: {cache_stats['cache_hits']}")

# Clear cache
cached_db.clear_cache()
cached_db.clear_cache_pattern("user:*")

# Cache warming
await cached_db.warm_cache([
    ("popular_users", db.User.find(is_active=True).sort("-login_count").limit(100)),
    ("recent_orders", db.Order.find().sort("-created_at").limit(50))
])
```

## 10. Monitoring & Performance

### Enable Monitoring
```python
from gdmongolite import add_monitoring_to_db

monitored_db = add_monitoring_to_db(db)

# Get performance metrics
stats = monitored_db.get_performance_stats()
print(f"Average query time: {stats['avg_query_time']:.2f}ms")
print(f"Slow queries: {len(stats['slow_queries'])}")
print(f"Total queries: {stats['total_queries']}")

# Health check
health = monitored_db.health_check()
print(f"Database status: {health['status']}")
print(f"Connection pool: {health['connection_pool']}")
print(f"Memory usage: {health['memory_usage']}")

# Query profiling
profiler = monitored_db.get_profiler()
with profiler.profile("user_search"):
    users = await db.User.find(name__contains="john").to_list()

profile_results = profiler.get_results("user_search")
print(f"Query took: {profile_results['duration']:.2f}ms")
```

### Monitoring Dashboard
```python
@app.get("/monitoring/dashboard")
async def monitoring_dashboard():
    return {
        "performance": monitored_db.get_performance_stats(),
        "health": monitored_db.health_check(),
        "cache": monitored_db.get_cache_stats() if hasattr(monitored_db, 'get_cache_stats') else {},
        "system": {
            "cpu_usage": monitored_db.get_cpu_usage(),
            "memory_usage": monitored_db.get_memory_usage(),
            "disk_usage": monitored_db.get_disk_usage()
        }
    }

@app.get("/monitoring/slow-queries")
async def slow_queries():
    return monitored_db.get_slow_queries(limit=20)
```

## 11. Production Setup

### Production Configuration
```python
from gdmongolite import production_setup

# Production-ready database with all features
db = production_setup(
    uri="mongodb+srv://user:pass@cluster.mongodb.net/",
    database="production",
    enable_monitoring=True,
    enable_caching=True,
    enable_security=True,
    pool_size=100,
    timeout_ms=5000
)

# Production FastAPI app
app = create_fastapi_app(
    db,
    schemas=[User, Product, Order],
    title="Production API",
    version="1.0.0",
    enable_monitoring=True,
    enable_caching=True,
    enable_security=True,
    cors_origins=["https://myapp.com", "https://admin.myapp.com"],
    rate_limiting=True,
    request_logging=True
)
```

### Docker Deployment
```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

```yaml
# docker-compose.yml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - MONGO_URI=mongodb://mongo:27017
      - MONGO_DB=production
    depends_on:
      - mongo
  
  mongo:
    image: mongo:7
    ports:
      - "27017:27017"
    volumes:
      - mongo_data:/data/db

volumes:
  mongo_data:
```

## 12. Complete E-commerce Example

```python
from gdmongolite import DB, Schema, Email, FieldTypes, create_fastapi_app
from datetime import datetime
from typing import List
from fastapi import HTTPException

# Define all schemas
class User(Schema):
    name: FieldTypes.Name
    email: Email
    password_hash: str
    role: str = "customer"
    address: dict = {}
    phone: FieldTypes.Phone = None
    created_at: datetime = datetime.now()

class Category(Schema):
    name: FieldTypes.Title
    description: FieldTypes.Description
    parent_id: str = None
    is_active: bool = True

class Product(Schema):
    name: FieldTypes.Title
    description: FieldTypes.Description
    price: FieldTypes.Price
    category_id: str
    stock: int = 0
    images: List[str] = []
    rating: FieldTypes.Rating = 0.0
    reviews_count: int = 0
    is_active: bool = True
    created_at: datetime = datetime.now()

class Order(Schema):
    user_id: str
    items: List[dict]  # [{"product_id": str, "quantity": int, "price": float}]
    total: FieldTypes.Price
    status: str = "pending"  # pending, confirmed, shipped, delivered, cancelled
    shipping_address: dict
    payment_method: str
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

class Review(Schema):
    user_id: str
    product_id: str
    rating: FieldTypes.Rating
    comment: FieldTypes.Description
    created_at: datetime = datetime.now()

# Setup database
db = DB()
for schema in [User, Category, Product, Order, Review]:
    db.register_schema(schema)

# Create FastAPI app
app = create_fastapi_app(
    db, 
    [User, Category, Product, Order, Review],
    title="E-commerce API",
    version="1.0.0"
)

# Custom business logic endpoints
@app.post("/orders/create")
async def create_order(order_data: dict):
    # Validate stock availability
    for item in order_data["items"]:
        product = await db.Product.find(_id=item["product_id"]).first()
        if not product:
            raise HTTPException(404, f"Product {item['product_id']} not found")
        if product["stock"] < item["quantity"]:
            raise HTTPException(400, f"Insufficient stock for {product['name']}")
    
    # Calculate total
    total = 0
    for item in order_data["items"]:
        product = await db.Product.find(_id=item["product_id"]).first()
        item["price"] = product["price"]
        total += product["price"] * item["quantity"]
    
    order_data["total"] = total
    
    # Create order
    order = await db.Order.insert(order_data)
    
    # Update stock
    for item in order_data["items"]:
        await db.Product.update(
            {"_id": item["product_id"]},
            {"$inc": {"stock": -item["quantity"]}}
        )
    
    return order

@app.get("/products/search")
async def search_products(
    query: str = None,
    category_id: str = None,
    min_price: float = None,
    max_price: float = None,
    min_rating: float = None,
    page: int = 1,
    limit: int = 20
):
    filters = {"is_active": True}
    
    if query:
        filters["$text"] = {"$search": query}
    if category_id:
        filters["category_id"] = category_id
    if min_price is not None:
        filters["price"] = {"$gte": min_price}
    if max_price is not None:
        filters.setdefault("price", {})["$lte"] = max_price
    if min_rating is not None:
        filters["rating"] = {"$gte": min_rating}
    
    products = await db.Product.find(**filters).skip((page-1)*limit).limit(limit).to_list()
    total = await db.Product.find(**filters).count()
    
    return {
        "products": products,
        "total": total,
        "page": page,
        "pages": (total + limit - 1) // limit
    }

@app.get("/analytics/dashboard")
async def analytics_dashboard():
    # Sales analytics
    total_revenue = await db.Order.aggregate().match(
        status__in=["delivered", "shipped"]
    ).group(None, total={"$sum": "$total"}).execute()
    
    # Product analytics
    top_products = await db.Order.aggregate().match(
        status__in=["delivered", "shipped"]
    ).unwind("items").group(
        "$items.product_id",
        total_sold={"$sum": "$items.quantity"},
        revenue={"$sum": {"$multiply": ["$items.quantity", "$items.price"]}}
    ).sort(total_sold=-1).limit(10).execute()
    
    # User analytics
    user_stats = await db.User.aggregate().group(
        None,
        total_users={"$sum": 1},
        customers={"$sum": {"$cond": [{"$eq": ["$role", "customer"]}, 1, 0]}},
        admins={"$sum": {"$cond": [{"$eq": ["$role", "admin"]}, 1, 0]}}
    ).execute()
    
    return {
        "revenue": total_revenue[0]["total"] if total_revenue else 0,
        "top_products": top_products,
        "user_stats": user_stats[0] if user_stats else {},
        "total_orders": await db.Order.find().count(),
        "pending_orders": await db.Order.find(status="pending").count()
    }

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
```

## 13. Migration System

### Database Migrations
```python
from gdmongolite import MigrationManager

# Initialize migration manager
migration_manager = MigrationManager(db)

# Create migration
@migration_manager.migration("001_add_user_fields")
async def add_user_fields():
    # Add new fields to existing users
    await db.User.update(
        {"phone": {"$exists": False}},
        {"$set": {"phone": None, "last_login": None}}
    )
    print("Added phone and last_login fields to users")

# Run migrations
await migration_manager.run_migrations()

# Check migration status
status = migration_manager.get_migration_status()
print(f"Applied migrations: {status['applied']}")
print(f"Pending migrations: {status['pending']}")
```

### Index Management
```python
# Create indexes
await db.User.create_index("email", unique=True)
await db.User.create_index([("name", 1), ("age", -1)])
await db.Product.create_index("category_id")

# Text search index
await db.Product.create_index([("name", "text"), ("description", "text")])

# Geospatial index
await db.User.create_index("location", index_type="2dsphere")

# List indexes
indexes = await db.User.list_indexes()
for index in indexes:
    print(f"Index: {index['name']} - {index['key']}")
```

## 14. CLI Tools

### Command Line Interface
```bash
# Initialize new project
gdmongolite init my-project
cd my-project

# Generate schema from existing collection
gdmongolite generate-schema users > models/user.py

# Run migrations
gdmongolite migrate

# Start development server
gdmongolite serve --reload

# Export data
gdmongolite export users users.json
gdmongolite export products products.csv

# Import data
gdmongolite import users.json User

# Database shell
gdmongolite shell
```

### Interactive Shell
```python
# Start interactive shell
# gdmongolite shell

# Available in shell:
db = DB()  # Pre-configured database
User, Product, Order = load_schemas()  # Auto-loaded schemas

# Interactive queries
users = await db.User.find(age__gte=18).to_list()
print(f"Found {len(users)} adult users")

# Quick stats
stats = await db.get_collection_stats()
for collection, stat in stats.items():
    print(f"{collection}: {stat['count']} documents")
```

## 15. Testing Utilities

### Test Database Setup
```python
from gdmongolite import TestDB
import pytest

@pytest.fixture
async def test_db():
    # Creates isolated test database
    db = TestDB()
    db.register_schema(User)
    yield db
    await db.cleanup()  # Automatically cleans up

@pytest.mark.asyncio
async def test_user_creation(test_db):
    user = await test_db.User.insert({
        "name": "Test User",
        "email": "test@example.com",
        "age": 25
    })
    assert user.success
    assert user.count == 1
    
    # Verify user exists
    found_user = await test_db.User.find(email="test@example.com").first()
    assert found_user["name"] == "Test User"
```

### Mock Data Generation
```python
from gdmongolite import MockDataGenerator

# Generate test data
mock_gen = MockDataGenerator()

# Generate users
users = mock_gen.generate_users(count=100)
for user in users:
    await db.User.insert(user)

# Generate products
products = mock_gen.generate_products(count=50)
for product in products:
    await db.Product.insert(product)

# Generate orders with relationships
orders = mock_gen.generate_orders(
    user_ids=[u["_id"] for u in users[:20]],
    product_ids=[p["_id"] for p in products],
    count=200
)
for order in orders:
    await db.Order.insert(order)
```

## 16. Performance Optimization

### Query Optimization
```python
# Use projections to limit fields
users = await db.User.find().project("name", "email").to_list()

# Use explain to analyze queries
explain_result = await db.User.find(age__gte=18).explain()
print(f"Execution time: {explain_result['executionTimeMillis']}ms")
print(f"Documents examined: {explain_result['totalDocsExamined']}")

# Batch operations for better performance
batch_operations = [
    {"insertOne": {"document": {"name": "User1", "email": "user1@example.com"}}},
    {"insertOne": {"document": {"name": "User2", "email": "user2@example.com"}}},
    {"updateOne": {"filter": {"name": "User1"}, "update": {"$set": {"age": 25}}}}
]
result = await db.User.bulk_write(batch_operations)
print(f"Inserted: {result.inserted_count}, Modified: {result.modified_count}")
```

### Connection Pooling
```python
# Configure connection pool
db = DB(
    uri="mongodb://localhost:27017",
    database="myapp",
    max_pool_size=100,
    min_pool_size=10,
    max_idle_time_ms=30000,
    wait_queue_timeout_ms=5000
)

# Monitor connection pool
pool_stats = db.get_pool_stats()
print(f"Active connections: {pool_stats['active']}")
print(f"Available connections: {pool_stats['available']}")
print(f"Total connections: {pool_stats['total']}")
```

## 17. Error Handling & Logging

### Custom Error Handling
```python
from gdmongolite import GDMongoError, ValidationError, ConnectionError

try:
    user = await db.User.insert({
        "name": "John",
        "email": "invalid-email",  # Will cause validation error
        "age": 200  # Will cause validation error
    })
except ValidationError as e:
    print(f"Validation failed: {e.details}")
    for field, error in e.field_errors.items():
        print(f"  {field}: {error}")
except ConnectionError as e:
    print(f"Database connection failed: {e}")
except GDMongoError as e:
    print(f"General database error: {e}")
```

### Logging Configuration
```python
import logging
from gdmongolite import configure_logging

# Configure logging
configure_logging(
    level=logging.INFO,
    log_queries=True,
    log_slow_queries=True,
    slow_query_threshold=100,  # ms
    log_file="gdmongolite.log"
)

# Custom logger
logger = logging.getLogger("gdmongolite")
logger.info("Application started")

# Query logging will automatically log:
# - All database operations
# - Slow queries (>100ms)
# - Connection events
# - Error details
```

## 18. Advanced Configuration

### Environment Configuration
```bash
# .env file - Complete configuration
MONGO_URI=mongodb://localhost:27017
MONGO_DB=myapp
MONGO_MAX_POOL=100
MONGO_MIN_POOL=10
MONGO_TIMEOUT_MS=30000
MONGO_MAX_IDLE_TIME_MS=30000
MONGO_WAIT_QUEUE_TIMEOUT_MS=5000

# Caching configuration
GDMONGO_CACHE_ENABLED=true
GDMONGO_CACHE_TTL=3600
GDMONGO_CACHE_MAX_SIZE=1000
REDIS_URL=redis://localhost:6379

# Monitoring configuration
GDMONGO_MONITORING_ENABLED=true
GDMONGO_LOG_SLOW_QUERIES=true
GDMONGO_SLOW_QUERY_THRESHOLD=500
GDMONGO_PROFILING_ENABLED=true

# Security configuration
GDMONGO_SECURITY_ENABLED=true
JWT_SECRET_KEY=your-super-secret-key
JWT_EXPIRATION_HOURS=24
PASSWORD_MIN_LENGTH=8

# Development settings
GDMONGO_DEBUG=true
GDMONGO_AUTO_RELOAD=true
GDMONGO_SUPPRESS_STARTUP=false
```

### Configuration Class
```python
from gdmongolite import ConfigManager

# Load configuration
config = ConfigManager()

# Access configuration
print(f"Database URI: {config.mongo_uri}")
print(f"Cache enabled: {config.cache_enabled}")
print(f"Debug mode: {config.debug}")

# Override configuration
config.override({
    "mongo_db": "test_database",
    "cache_ttl": 1800,
    "debug": True
})

# Validate configuration
if not config.validate():
    print("Configuration validation failed:")
    for error in config.validation_errors:
        print(f"  - {error}")
```

## 19. Microservices Integration

### Service Discovery
```python
from gdmongolite import ServiceRegistry

# Register service
registry = ServiceRegistry(db)
await registry.register_service(
    name="user-service",
    host="localhost",
    port=8001,
    health_check_url="/health",
    metadata={"version": "1.0.0", "environment": "production"}
)

# Discover services
services = await registry.discover_services("user-service")
for service in services:
    print(f"Service: {service['name']} at {service['host']}:{service['port']}")

# Health monitoring
health_status = await registry.check_service_health("user-service")
print(f"Service health: {health_status['status']}")
```

### Event Sourcing
```python
from gdmongolite import EventStore

# Event store for microservices
event_store = EventStore(db)

# Store events
await event_store.store_event(
    aggregate_id="user-123",
    event_type="UserCreated",
    event_data={
        "name": "John Doe",
        "email": "john@example.com",
        "timestamp": datetime.now()
    },
    version=1
)

# Replay events
events = await event_store.get_events("user-123")
for event in events:
    print(f"Event: {event['event_type']} at {event['timestamp']}")

# Event projections
@event_store.projection("user_summary")
async def user_summary_projection(event):
    if event["event_type"] == "UserCreated":
        await db.UserSummary.insert({
            "user_id": event["aggregate_id"],
            "name": event["event_data"]["name"],
            "created_at": event["event_data"]["timestamp"]
        })
```

## 20. Deployment Strategies

### Kubernetes Deployment
```yaml
# k8s-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: gdmongolite-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: gdmongolite-app
  template:
    metadata:
      labels:
        app: gdmongolite-app
    spec:
      containers:
      - name: app
        image: myapp:latest
        ports:
        - containerPort: 8000
        env:
        - name: MONGO_URI
          valueFrom:
            secretKeyRef:
              name: mongo-secret
              key: uri
        - name: MONGO_DB
          value: "production"
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
---
apiVersion: v1
kind: Service
metadata:
  name: gdmongolite-service
spec:
  selector:
    app: gdmongolite-app
  ports:
  - port: 80
    targetPort: 8000
  type: LoadBalancer
```

### AWS Lambda Deployment
```python
# lambda_handler.py
from gdmongolite import DB, Schema, create_fastapi_app
from mangum import Mangum

# Initialize database
db = DB(
    uri=os.environ["MONGO_URI"],
    database=os.environ["MONGO_DB"]
)

# Register schemas
db.register_schema(User)

# Create FastAPI app
app = create_fastapi_app(db, [User])

# Lambda handler
handler = Mangum(app)

def lambda_handler(event, context):
    return handler(event, context)
```

## 21. Missing Features - Complete Coverage

### Quick Setup Functions
```python
from gdmongolite import quick_setup, production_setup, development_setup

# Quick setup with all features enabled
db = quick_setup(
    uri="mongodb://localhost:27017",
    database="myapp"
)

# Production setup with monitoring, caching, and security
db = production_setup(
    uri="mongodb+srv://user:pass@cluster.mongodb.net/",
    database="production"
)

# Development setup with debugging and hot reload
db = development_setup(
    uri="mongodb://localhost:27017",
    database="development"
)
# Automatically sets GDMONGO_DEBUG=true
```

### Role-Based Access Control (RBAC)
```python
from gdmongolite import RoleBasedAccessControl

# Setup RBAC
rbac = RoleBasedAccessControl(db)

# Define roles and permissions
await rbac.create_role("admin", [
    "users:read", "users:write", "users:delete",
    "products:read", "products:write", "products:delete",
    "orders:read", "orders:write", "orders:delete"
])

await rbac.create_role("manager", [
    "users:read", "users:write",
    "products:read", "products:write",
    "orders:read", "orders:write"
])

await rbac.create_role("user", [
    "users:read",
    "products:read",
    "orders:read"
])

# Assign roles to users
await rbac.assign_role(user_id="user123", role="manager")
await rbac.assign_role(user_id="user456", role="user")

# Check permissions
has_permission = await rbac.check_permission(
    user_id="user123", 
    permission="products:write"
)
print(f"User can write products: {has_permission}")

# Middleware for FastAPI
@app.get("/admin/users")
async def admin_users(current_user=Depends(rbac.require_permission("users:read"))):
    return await db.User.find().to_list()
```

### Data Encryption
```python
from gdmongolite import DataEncryption

# Setup field-level encryption
encryption = DataEncryption(secret_key="your-encryption-key")

# Encrypt sensitive fields
class User(Schema):
    name: FieldTypes.Name
    email: Email
    ssn: str = encryption.encrypted_field()  # Automatically encrypted
    credit_card: str = encryption.encrypted_field()
    salary: float = encryption.encrypted_field()

# Data is automatically encrypted on insert
user = await db.User.insert({
    "name": "John Doe",
    "email": "john@example.com",
    "ssn": "123-45-6789",  # Encrypted in database
    "credit_card": "4111-1111-1111-1111",  # Encrypted in database
    "salary": 75000.0  # Encrypted in database
})

# Data is automatically decrypted on retrieval
user = await db.User.find(email="john@example.com").first()
print(f"SSN: {user['ssn']}")  # Automatically decrypted

# Manual encryption/decryption
encrypted_data = encryption.encrypt("sensitive data")
decrypted_data = encryption.decrypt(encrypted_data)
```

### Audit Logging
```python
from gdmongolite import AuditLog

# Setup audit logging
audit = AuditLog(db)

# Enable automatic audit logging
@audit.track_changes
class User(Schema):
    name: FieldTypes.Name
    email: Email
    role: str = "user"

# All changes are automatically logged
user = await db.User.insert({"name": "John", "email": "john@example.com"})
# Audit log: {"action": "insert", "collection": "user", "document_id": "...", "user_id": "...", "timestamp": "..."}

await db.User.update({"_id": user.data}, {"$set": {"role": "admin"}})
# Audit log: {"action": "update", "collection": "user", "document_id": "...", "changes": {"role": {"old": "user", "new": "admin"}}, ...}

# Query audit logs
audit_logs = await audit.get_logs(
    collection="user",
    action="update",
    start_date=datetime.now() - timedelta(days=7)
)

for log in audit_logs:
    print(f"User {log['user_id']} {log['action']} document {log['document_id']} at {log['timestamp']}")

# Manual audit logging
await audit.log_action(
    action="custom_action",
    collection="user",
    document_id="user123",
    user_id="admin456",
    metadata={"reason": "Manual verification", "ip_address": "192.168.1.1"}
)
```

### Security Configuration
```python
from gdmongolite import SecurityConfig

# Comprehensive security setup
security_config = SecurityConfig(
    # Password policies
    password_min_length=12,
    password_require_uppercase=True,
    password_require_lowercase=True,
    password_require_numbers=True,
    password_require_symbols=True,
    password_max_age_days=90,
    
    # Session management
    session_timeout_minutes=30,
    max_concurrent_sessions=3,
    
    # Rate limiting
    rate_limit_requests=100,
    rate_limit_window_minutes=15,
    
    # IP restrictions
    allowed_ips=["192.168.1.0/24", "10.0.0.0/8"],
    blocked_ips=["192.168.1.100"],
    
    # Encryption
    encrypt_sensitive_fields=True,
    encryption_algorithm="AES-256-GCM",
    
    # Audit settings
    audit_all_operations=True,
    audit_retention_days=365
)

# Apply security configuration
db.apply_security_config(security_config)

# Validate password against policy
is_valid, errors = security_config.validate_password("MySecureP@ssw0rd123")
if not is_valid:
    for error in errors:
        print(f"Password error: {error}")
```

### Web Server Integration
```python
from gdmongolite import WebServer, quick_serve, dev_serve, prod_serve

# Quick development server
quick_serve(
    db=db,
    schemas=[User, Product, Order],
    port=8000,
    reload=True
)

# Development server with hot reload
dev_serve(
    db=db,
    schemas=[User, Product, Order],
    port=8000,
    debug=True,
    auto_reload=True,
    cors_origins=["http://localhost:3000"]
)

# Production server
prod_serve(
    db=db,
    schemas=[User, Product, Order],
    host="0.0.0.0",
    port=8000,
    workers=4,
    enable_ssl=True,
    ssl_cert="/path/to/cert.pem",
    ssl_key="/path/to/key.pem"
)

# Custom web server
server = WebServer(
    db=db,
    schemas=[User, Product, Order],
    middleware=[
        "cors",
        "gzip",
        "rate_limiting",
        "security_headers"
    ],
    static_files={"/static": "./static"},
    templates_dir="./templates"
)

# Add custom routes
@server.app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now()}

# Start server
server.run(host="0.0.0.0", port=8000)
```

### Query Analyzer
```python
from gdmongolite import QueryAnalyzer

# Analyze query performance
analyzer = QueryAnalyzer(db)

# Analyze a specific query
analysis = await analyzer.analyze_query(
    collection="user",
    query={"age": {"$gte": 18}, "is_active": True},
    projection={"name": 1, "email": 1}
)

print(f"Execution time: {analysis['execution_time_ms']}ms")
print(f"Documents examined: {analysis['docs_examined']}")
print(f"Documents returned: {analysis['docs_returned']}")
print(f"Index used: {analysis['index_used']}")

if analysis['suggestions']:
    print("Optimization suggestions:")
    for suggestion in analysis['suggestions']:
        print(f"  - {suggestion}")

# Analyze all slow queries
slow_queries = await analyzer.get_slow_queries(threshold_ms=100)
for query in slow_queries:
    print(f"Slow query: {query['query']} took {query['duration_ms']}ms")

# Index recommendations
recommendations = await analyzer.recommend_indexes()
for rec in recommendations:
    print(f"Recommended index for {rec['collection']}: {rec['index']}")
    print(f"  Reason: {rec['reason']}")
    print(f"  Expected improvement: {rec['improvement']}")
```

### Common Aggregations
```python
from gdmongolite import CommonAggregations

# Pre-built common aggregation patterns
agg = CommonAggregations(db)

# Time-based analytics
daily_stats = await agg.daily_stats(
    collection="order",
    date_field="created_at",
    value_field="total",
    start_date=datetime.now() - timedelta(days=30)
)

monthly_revenue = await agg.monthly_revenue(
    collection="order",
    amount_field="total",
    status_filter={"status": "completed"}
)

# User behavior analytics
user_activity = await agg.user_activity_summary(
    user_collection="user",
    activity_collection="order",
    user_id_field="user_id",
    activity_date_field="created_at"
)

# Product analytics
top_products = await agg.top_selling_products(
    order_collection="order",
    product_collection="product",
    limit=10
)

# Geographic analytics
sales_by_region = await agg.sales_by_region(
    collection="order",
    region_field="shipping_address.region",
    amount_field="total"
)

# Cohort analysis
cohort_data = await agg.cohort_analysis(
    user_collection="user",
    activity_collection="order",
    signup_date_field="created_at",
    activity_date_field="created_at"
)
```

### Notification System
```python
from gdmongolite import NotificationSystem

# Setup notifications
notifications = NotificationSystem(db)

# Configure notification channels
await notifications.add_channel("email", {
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "username": "your-email@gmail.com",
    "password": "your-app-password"
})

await notifications.add_channel("slack", {
    "webhook_url": "https://hooks.slack.com/services/...",
    "channel": "#alerts"
})

await notifications.add_channel("sms", {
    "provider": "twilio",
    "account_sid": "your-account-sid",
    "auth_token": "your-auth-token",
    "from_number": "+1234567890"
})

# Setup notification rules
@notifications.on_event("user_registered")
async def welcome_email(event_data):
    await notifications.send(
        channel="email",
        to=event_data["email"],
        subject="Welcome to our platform!",
        template="welcome_email",
        data=event_data
    )

@notifications.on_event("order_placed")
async def order_confirmation(event_data):
    # Send email to customer
    await notifications.send(
        channel="email",
        to=event_data["customer_email"],
        subject="Order Confirmation",
        template="order_confirmation",
        data=event_data
    )
    
    # Notify admin via Slack
    await notifications.send(
        channel="slack",
        message=f"New order #{event_data['order_id']} for ${event_data['total']}"
    )

# Trigger notifications
await notifications.trigger_event("user_registered", {
    "user_id": "user123",
    "name": "John Doe",
    "email": "john@example.com"
})

# Bulk notifications
users = await db.User.find(is_active=True).to_list()
await notifications.send_bulk(
    channel="email",
    recipients=[user["email"] for user in users],
    subject="Monthly Newsletter",
    template="newsletter",
    data={"month": "December", "year": 2024}
)
```

## 22. Telemetry & Analytics

### Usage Telemetry
```python
from gdmongolite import TelemetryCollector

# Setup telemetry (optional, privacy-focused)
telemetry = TelemetryCollector(
    enabled=True,
    anonymous=True,  # No personal data collected
    endpoint="https://telemetry.gdmongolite.com/api/v1/events"
)

# Automatic usage tracking
db = DB(telemetry=telemetry)

# Custom events
telemetry.track_event("feature_used", {
    "feature": "advanced_aggregation",
    "complexity": "high",
    "performance_ms": 150
})

# Performance metrics
telemetry.track_performance("query_execution", {
    "collection": "user",
    "operation": "find",
    "duration_ms": 45,
    "documents_returned": 100
})

# Error tracking
telemetry.track_error("validation_error", {
    "error_type": "field_validation",
    "field": "email",
    "schema": "User"
})

# Get insights
insights = await telemetry.get_insights()
print(f"Most used features: {insights['popular_features']}")
print(f"Average query time: {insights['avg_query_time']}ms")
print(f"Error rate: {insights['error_rate']:.2%}")
```

### Application Analytics
```python
# Built-in analytics for your application
analytics = telemetry.get_app_analytics()

# User behavior analytics
user_analytics = await analytics.user_behavior(
    user_collection="user",
    activity_collections=["order", "review", "login"]
)

# Feature usage analytics
feature_usage = await analytics.feature_usage(
    events_collection="app_events",
    time_range=timedelta(days=30)
)

# Performance analytics
performance_data = await analytics.performance_metrics(
    metrics_collection="performance_logs",
    aggregation_level="daily"
)

# Custom dashboards
dashboard_data = await analytics.create_dashboard([
    {"type": "line_chart", "metric": "daily_active_users", "period": "30d"},
    {"type": "bar_chart", "metric": "feature_usage", "period": "7d"},
    {"type": "pie_chart", "metric": "user_segments", "period": "current"}
])
```

## 23. Utility Functions

### Data Validation Utilities
```python
from gdmongolite import ValidationUtils

# Email validation
is_valid_email = ValidationUtils.validate_email("user@example.com")
print(f"Email valid: {is_valid_email}")  # True

# Phone number validation
is_valid_phone = ValidationUtils.validate_phone("+1-555-123-4567")
print(f"Phone valid: {is_valid_phone}")  # True

# URL validation
is_valid_url = ValidationUtils.validate_url("https://example.com")
print(f"URL valid: {is_valid_url}")  # True

# Credit card validation
is_valid_card = ValidationUtils.validate_credit_card("4111-1111-1111-1111")
print(f"Credit card valid: {is_valid_card}")  # True

# Custom validation
def validate_username(username):
    return ValidationUtils.validate_pattern(
        username, 
        r'^[a-zA-Z0-9_]{3,20}$',
        "Username must be 3-20 characters, alphanumeric and underscores only"
    )

result = validate_username("john_doe123")
print(f"Username valid: {result.is_valid}")  # True
```

### Data Transformation Utilities
```python
from gdmongolite import DataUtils

# Convert data formats
data = {
    "user_name": "John Doe",
    "user_email": "john@example.com",
    "user_age": "30"
}

# Snake case to camel case
camel_case_data = DataUtils.to_camel_case(data)
print(camel_case_data)  # {"userName": "John Doe", "userEmail": "john@example.com", "userAge": "30"}

# Camel case to snake case
snake_case_data = DataUtils.to_snake_case(camel_case_data)
print(snake_case_data)  # Original format

# Type conversion
typed_data = DataUtils.auto_convert_types(data)
print(typed_data)  # {"user_name": "John Doe", "user_email": "john@example.com", "user_age": 30}

# Clean data
cleaned_data = DataUtils.clean_data({
    "name": "  John Doe  ",
    "email": "JOHN@EXAMPLE.COM",
    "phone": "(555) 123-4567",
    "empty_field": "",
    "null_field": None
})
print(cleaned_data)  # {"name": "John Doe", "email": "john@example.com", "phone": "5551234567"}
```

### Date/Time Utilities
```python
from gdmongolite import DateUtils
from datetime import datetime, timedelta

# Parse various date formats
date1 = DateUtils.parse_date("2024-01-15")
date2 = DateUtils.parse_date("01/15/2024")
date3 = DateUtils.parse_date("January 15, 2024")
date4 = DateUtils.parse_date("2024-01-15T10:30:00Z")

# Format dates
formatted = DateUtils.format_date(datetime.now(), "YYYY-MM-DD HH:mm:ss")
print(f"Formatted date: {formatted}")

# Date calculations
start_of_month = DateUtils.start_of_month(datetime.now())
end_of_month = DateUtils.end_of_month(datetime.now())
days_ago_30 = DateUtils.days_ago(30)

# Time zone handling
utc_time = DateUtils.to_utc(datetime.now())
local_time = DateUtils.to_local(utc_time, "America/New_York")

# Business day calculations
business_days = DateUtils.business_days_between(
    start_date=datetime(2024, 1, 1),
    end_date=datetime(2024, 1, 31)
)
print(f"Business days in January: {business_days}")
```

### String Utilities
```python
from gdmongolite import StringUtils

# Generate secure random strings
random_id = StringUtils.generate_id(length=12)
print(f"Random ID: {random_id}")  # e.g., "aB3xY9mN2pQ7"

secure_token = StringUtils.generate_token(length=32)
print(f"Secure token: {secure_token}")

# Slug generation
slug = StringUtils.slugify("This is a Sample Title!")
print(f"Slug: {slug}")  # "this-is-a-sample-title"

# Text processing
truncated = StringUtils.truncate("This is a very long text that needs to be shortened", 20)
print(f"Truncated: {truncated}")  # "This is a very long..."

# Extract information
emails = StringUtils.extract_emails("Contact us at support@example.com or sales@example.com")
print(f"Emails found: {emails}")  # ["support@example.com", "sales@example.com"]

urls = StringUtils.extract_urls("Visit https://example.com or http://test.com")
print(f"URLs found: {urls}")  # ["https://example.com", "http://test.com"]

# Text similarity
similarity = StringUtils.similarity("hello world", "hello word")
print(f"Similarity: {similarity:.2f}")  # 0.91
```

### File Utilities
```python
from gdmongolite import FileUtils

# File operations
file_info = FileUtils.get_file_info("data.json")
print(f"File size: {file_info['size']} bytes")
print(f"Modified: {file_info['modified']}")

# Read files with encoding detection
content = FileUtils.read_file_smart("data.csv")
print(f"File encoding: {content['encoding']}")
print(f"Content preview: {content['content'][:100]}...")

# Batch file operations
files = FileUtils.find_files(
    directory="./data",
    pattern="*.json",
    recursive=True
)

for file_path in files:
    print(f"Found JSON file: {file_path}")

# File validation
is_valid_json = FileUtils.validate_json_file("data.json")
is_valid_csv = FileUtils.validate_csv_file("data.csv")

# Compress/decompress
FileUtils.compress_file("large_data.json", "large_data.json.gz")
FileUtils.decompress_file("large_data.json.gz", "restored_data.json")
```

### Hash Utilities
```python
from gdmongolite import HashUtils

# Generate hashes
md5_hash = HashUtils.md5("hello world")
sha256_hash = HashUtils.sha256("hello world")
sha512_hash = HashUtils.sha512("hello world")

print(f"MD5: {md5_hash}")
print(f"SHA256: {sha256_hash}")
print(f"SHA512: {sha512_hash}")

# File hashing
file_hash = HashUtils.hash_file("data.json", algorithm="sha256")
print(f"File hash: {file_hash}")

# Verify data integrity
is_valid = HashUtils.verify_hash("hello world", sha256_hash, "sha256")
print(f"Hash valid: {is_valid}")  # True

# Generate checksums
checksum = HashUtils.generate_checksum({
    "name": "John Doe",
    "email": "john@example.com",
    "age": 30
})
print(f"Data checksum: {checksum}")
```

### Network Utilities
```python
from gdmongolite import NetworkUtils

# IP address utilities
is_valid_ip = NetworkUtils.validate_ip("192.168.1.1")
print(f"IP valid: {is_valid_ip}")  # True

ip_info = NetworkUtils.get_ip_info("8.8.8.8")
print(f"IP location: {ip_info['country']}, {ip_info['city']}")

# URL utilities
url_parts = NetworkUtils.parse_url("https://api.example.com:8080/v1/users?page=1&limit=10")
print(f"Host: {url_parts['host']}")
print(f"Port: {url_parts['port']}")
print(f"Path: {url_parts['path']}")
print(f"Query: {url_parts['query']}")

# HTTP utilities
response = await NetworkUtils.http_request(
    method="GET",
    url="https://api.example.com/users",
    headers={"Authorization": "Bearer token"},
    timeout=30
)

if response.success:
    print(f"Response: {response.data}")
else:
    print(f"Error: {response.error}")

# Health check utilities
health = await NetworkUtils.check_service_health("https://api.example.com/health")
print(f"Service healthy: {health['is_healthy']}")
print(f"Response time: {health['response_time_ms']}ms")
```

## Author Information

**Ganesh Datta Padamata**
- Email: ganeshdattapadamata@gmail.com
- GitHub: [@ganeshdatta23](https://github.com/ganeshdatta23)
- LinkedIn: [Ganesh Datta Padamata](https://linkedin.com/in/ganeshdatta)
- Website: [ganeshdatta.dev](https://ganeshdatta.dev)

### About the Author
Ganesh Datta Padamata is a passionate software engineer and MongoDB expert with extensive experience in building scalable database solutions. He created gdmongolite to solve the common pain points developers face when working with MongoDB, making it accessible to beginners while providing powerful features for experts.

### Contact & Support
- **Technical Support**: ganeshdattapadamata@gmail.com
- **Feature Requests**: [GitHub Issues](https://github.com/ganeshdatta23/gdmongolite/issues)
- **Community**: [GitHub Discussions](https://github.com/ganeshdatta23/gdmongolite/discussions)
- **Documentation**: [ReadTheDocs](https://gdmongolite.readthedocs.io)

### Contributing
Contributions are welcome! Please read our [Contributing Guide](https://github.com/ganeshdatta23/gdmongolite/blob/main/CONTRIBUTING.md) and [Code of Conduct](https://github.com/ganeshdatta23/gdmongolite/blob/main/CODE_OF_CONDUCT.md).

### License
MIT License - see [LICENSE](https://github.com/ganeshdatta23/gdmongolite/blob/main/LICENSE) file.

### Acknowledgments
Special thanks to the MongoDB community, FastAPI team, and Pydantic developers for creating the amazing tools that make gdmongolite possible.


## Installation After Publication

```bash
pip install gdmongolite
```

## Quick Start After Installation

```python
from gdmongolite import DB, Schema, Email, FieldTypes

# Define your model
class User(Schema):
    name: FieldTypes.Name
    email: Email
    age: FieldTypes.Age

# Connect and use
db = DB()
db.register_schema(User)

# Insert with validation
user = await db.User.insert({
    "name": "Ganesh Datta",
    "email": "ganeshdattapadamata@gmail.com",
    "age": 28
})

print("Welcome to the future of MongoDB development with gdmongolite!")
print(f"Created by: Ganesh Datta Padamata")
print(f"Contact: ganeshdattapadamata@gmail.com")
```

## Installation After Publication

```bash
pip install gdmongolite
```

## First Program (30 seconds)

```python
from gdmongolite import DB, Schema, Email, FieldTypes

class User(Schema):
    name: FieldTypes.Name
    email: Email
    age: FieldTypes.Age

db = DB()
db.register_schema(User)

# Insert user
user = await db.User.insert({
    "name": "Alice Johnson",
    "email": "alice@example.com", 
    "age": 28
})

print("Welcome to the future of MongoDB development!")
```
