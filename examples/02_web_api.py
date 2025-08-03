"""
WEB API WITH FASTAPI - From Zero to Hero!
=========================================

Learn how to create a professional REST API in just 5 minutes!
No web development experience needed - gdmongolite does everything!

What you'll learn:
- Create REST API with one line of code
- Auto-generated API documentation
- Handle user authentication
- Deploy to production
"""

from gdmongolite import DB, Schema, Email, FieldTypes, create_fastapi_app, quick_serve

# Step 1: Define your data models
db = DB()

class User(Schema):
    name: FieldTypes.Name
    email: Email
    age: FieldTypes.Age
    role: str = "user"  # user, admin, moderator
    is_active: bool = True

class Product(Schema):
    name: FieldTypes.Title
    description: FieldTypes.Description
    price: FieldTypes.Price
    category: str
    in_stock: bool = True

class Order(Schema):
    user_id: str
    product_ids: list[str]
    total_amount: FieldTypes.Price
    status: str = "pending"  # pending, confirmed, shipped, delivered

# Register schemas
for schema in [User, Product, Order]:
    db.register_schema(schema)

# Step 2: Create FastAPI app (ONE LINE!)
app = create_fastapi_app(
    db,
    schemas=[User, Product, Order],
    title="My Amazing API",
    description="Built with gdmongolite - World's Easiest MongoDB Toolkit",
    version="1.0.0"
)

# Step 3: Add custom endpoints
@app.get("/")
async def welcome():
    """Welcome message"""
    return {
        "message": "Welcome to your gdmongolite API!",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/users/stats")
async def user_stats():
    """Get user statistics"""
    total = await db.User.find().count()
    active = await db.User.find(is_active=True).count()
    admins = await db.User.find(role="admin").count()
    
    return {
        "total_users": total,
        "active_users": active,
        "admin_users": admins,
        "inactive_users": total - active
    }

@app.get("/products/categories")
async def product_categories():
    """Get all product categories"""
    categories = await db.Product.find().distinct("category")
    return {"categories": categories}

@app.post("/orders/calculate")
async def calculate_order(product_ids: list[str]):
    """Calculate order total"""
    total = 0
    products = []
    
    for product_id in product_ids:
        from bson import ObjectId
        product = await db.Product.find(_id=ObjectId(product_id)).first()
        if product:
            total += product["price"]
            products.append(product["name"])
    
    return {
        "products": products,
        "total_amount": total,
        "currency": "USD"
    }

# Step 4: Run the server
if __name__ == "__main__":
    print("Starting your amazing API server...")
    print("API Documentation: http://localhost:8000/docs")
    print("Health Check: http://localhost:8000/health")
    print("User Stats: http://localhost:8000/users/stats")
    
    # This starts the server - visit http://localhost:8000/docs
    quick_serve(db, [User, Product, Order], port=8000)