"""
🌐 WEB API TUTORIAL - From Zero to Hero!
========================================

Learn how to create a professional web API in just 5 minutes!
No web development experience needed - we'll teach you everything!

What you'll learn:
- How to create REST APIs instantly
- How to handle web requests
- How to serve your API to the world
- How to create interactive documentation
- How to become a web API expert!
"""

from gdmongolite import (
    DB, Schema, Email, FieldTypes,
    create_fastapi_app, quick_serve,
    FastAPIIntegration
)
from typing import List, Optional
from datetime import datetime

print("🌐 Welcome to Web API Tutorial!")
print("📚 Let's create professional APIs the easy way...")

# Step 1: Create your data models (same as before, but for web!)
db = DB()

class User(Schema):
    """User model for our API"""
    name: FieldTypes.Name
    email: Email
    age: FieldTypes.Age
    bio: FieldTypes.Description = ""
    is_active: bool = True
    created_at: datetime = None

class Post(Schema):
    """Blog post model"""
    title: FieldTypes.Title
    content: FieldTypes.Content
    author_email: Email
    tags: List[str] = []
    published: bool = False
    created_at: datetime = None

class Comment(Schema):
    """Comment model"""
    post_id: str
    author_email: Email
    content: str
    created_at: datetime = None

# Register all models
for model in [User, Post, Comment]:
    db.register_schema(model)

print("✅ Models registered! Ready to create API...")

# Step 2: Create API with ONE LINE! (Yes, really!)
print("\n🚀 CREATING API WITH ONE LINE...")

def create_instant_api():
    """Create a complete REST API instantly"""
    
    # This ONE line creates a complete API with:
    # - User management endpoints
    # - Post management endpoints  
    # - Comment management endpoints
    # - Interactive documentation
    # - Error handling
    # - Data validation
    # - And much more!
    
    app = create_fastapi_app(
        db,
        schemas=[User, Post, Comment],
        title="My Amazing Blog API",
        description="Created with gdmongolite - The World's Easiest MongoDB Toolkit!",
        version="1.0.0"
    )
    
    print("✅ API created! Here's what you get automatically:")
    print("📋 AUTOMATIC ENDPOINTS:")
    print("   Users:")
    print("   - GET    /users/           (List all users)")
    print("   - POST   /users/           (Create new user)")
    print("   - GET    /users/{id}       (Get specific user)")
    print("   - PUT    /users/{id}       (Update user)")
    print("   - DELETE /users/{id}       (Delete user)")
    print("   - POST   /users/search     (Advanced search)")
    print("   - POST   /users/bulk       (Create multiple users)")
    print("")
    print("   Posts:")
    print("   - GET    /posts/           (List all posts)")
    print("   - POST   /posts/           (Create new post)")
    print("   - GET    /posts/{id}       (Get specific post)")
    print("   - PUT    /posts/{id}       (Update post)")
    print("   - DELETE /posts/{id}       (Delete post)")
    print("   - POST   /posts/search     (Advanced search)")
    print("")
    print("   Comments:")
    print("   - GET    /comments/        (List all comments)")
    print("   - POST   /comments/        (Create new comment)")
    print("   - GET    /comments/{id}    (Get specific comment)")
    print("   - PUT    /comments/{id}    (Update comment)")
    print("   - DELETE /comments/{id}    (Delete comment)")
    print("")
    print("   Utility:")
    print("   - GET    /health           (Health check)")
    print("   - GET    /schemas          (API schema info)")
    print("   - GET    /stats            (Database statistics)")
    print("   - GET    /docs             (Interactive documentation)")
    
    return app

# Step 3: Add custom endpoints (make it your own!)
print("\n🎨 ADDING CUSTOM ENDPOINTS...")

def add_custom_endpoints(app):
    """Add your own custom API endpoints"""
    
    # Custom endpoint: Get user statistics
    @app.get("/api/user-stats")
    async def get_user_stats():
        """Get user statistics"""
        total_users = await db.User.find().count()
        active_users = await db.User.find(is_active=True).count()
        
        return {
            "total_users": total_users,
            "active_users": active_users,
            "inactive_users": total_users - active_users
        }
    
    # Custom endpoint: Get popular posts
    @app.get("/api/popular-posts")
    async def get_popular_posts(limit: int = 10):
        """Get most popular posts"""
        posts = await (db.Post
                      .find(published=True)
                      .sort("-created_at")
                      .limit(limit)
                      .to_list())
        
        return {
            "posts": posts,
            "count": len(posts)
        }
    
    # Custom endpoint: Search posts by tag
    @app.get("/api/posts/by-tag/{tag}")
    async def get_posts_by_tag(tag: str):
        """Get posts by specific tag"""
        posts = await db.Post.find(tags__contains=tag, published=True).to_list()
        
        return {
            "tag": tag,
            "posts": posts,
            "count": len(posts)
        }
    
    # Custom endpoint: User dashboard
    @app.get("/api/dashboard/{user_email}")
    async def get_user_dashboard(user_email: str):
        """Get user's dashboard data"""
        
        # Get user info
        user = await db.User.find(email=user_email).first()
        if not user:
            return {"error": "User not found"}
        
        # Get user's posts
        posts = await db.Post.find(author_email=user_email).to_list()
        
        # Get user's comments
        comments = await db.Comment.find(author_email=user_email).to_list()
        
        return {
            "user": user,
            "posts": {
                "total": len(posts),
                "published": len([p for p in posts if p["published"]]),
                "drafts": len([p for p in posts if not p["published"]])
            },
            "comments": {
                "total": len(comments)
            }
        }
    
    print("✅ Custom endpoints added!")
    print("🎨 Your custom endpoints:")
    print("   - GET /api/user-stats        (User statistics)")
    print("   - GET /api/popular-posts     (Popular posts)")
    print("   - GET /api/posts/by-tag/{tag} (Posts by tag)")
    print("   - GET /api/dashboard/{email}  (User dashboard)")

# Step 4: Advanced API features
print("\n🎓 ADVANCED API FEATURES...")

def create_advanced_api():
    """Create API with advanced features"""
    
    # Create FastAPI app manually for more control
    from fastapi import FastAPI, HTTPException, Query, Path
    from fastapi.middleware.cors import CORSMiddleware
    
    app = FastAPI(
        title="Advanced Blog API",
        description="Professional API with advanced features",
        version="2.0.0"
    )
    
    # Add CORS (allows web browsers to use your API)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, specify your domains
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Create integration
    integration = FastAPIIntegration(db, app)
    
    # Add CRUD routes
    integration.add_crud_routes(User)
    integration.add_crud_routes(Post)
    integration.add_crud_routes(Comment)
    
    # Add utility endpoints
    integration.add_health_check()
    integration.add_schema_info()
    integration.add_stats_endpoint()
    
    # Advanced endpoint with pagination and filtering
    @app.get("/api/advanced-search")
    async def advanced_search(
        model: str = Query(..., description="Model to search (user, post, comment)"),
        query: str = Query(None, description="Search query"),
        page: int = Query(1, ge=1, description="Page number"),
        per_page: int = Query(10, ge=1, le=100, description="Items per page"),
        sort_by: str = Query("created_at", description="Field to sort by"),
        sort_order: str = Query("desc", description="Sort order (asc/desc)")
    ):
        """Advanced search with pagination and sorting"""
        
        # Select model
        if model == "user":
            schema = db.User
        elif model == "post":
            schema = db.Post
        elif model == "comment":
            schema = db.Comment
        else:
            raise HTTPException(status_code=400, detail="Invalid model")
        
        # Build query
        filters = {}
        if query:
            # Search in multiple fields based on model
            if model == "user":
                filters = {"$or": [
                    {"name__contains": query},
                    {"email__contains": query},
                    {"bio__contains": query}
                ]}
            elif model == "post":
                filters = {"$or": [
                    {"title__contains": query},
                    {"content__contains": query},
                    {"tags__contains": query}
                ]}
            elif model == "comment":
                filters = {"content__contains": query}
        
        # Execute query
        cursor = schema.find(**filters)
        
        # Apply sorting
        sort_direction = -1 if sort_order == "desc" else 1
        cursor = cursor.sort(**{sort_by: sort_direction})
        
        # Get total count
        total = await cursor.count()
        
        # Apply pagination
        skip = (page - 1) * per_page
        results = await cursor.skip(skip).limit(per_page).to_list()
        
        return {
            "results": results,
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total": total,
                "pages": (total + per_page - 1) // per_page
            },
            "query": query,
            "sort": {"by": sort_by, "order": sort_order}
        }
    
    print("✅ Advanced API created with:")
    print("   🔍 Advanced search with pagination")
    print("   🌐 CORS enabled for web browsers")
    print("   📊 Detailed pagination info")
    print("   🔧 Flexible sorting options")
    
    return app

# Step 5: Serve your API to the world!
print("\n🌍 SERVING YOUR API...")

def serve_api():
    """Different ways to serve your API"""
    
    print("🚀 SERVING OPTIONS:")
    print("1. Quick serve (development):")
    print("   quick_serve(db, [User, Post, Comment])")
    print("")
    print("2. Development server with auto-reload:")
    print("   from gdmongolite import dev_serve")
    print("   dev_serve(db, [User, Post, Comment])")
    print("")
    print("3. Production server:")
    print("   from gdmongolite import prod_serve")
    print("   prod_serve(db, [User, Post, Comment], workers=4)")
    print("")
    print("4. Custom server:")
    print("   app = create_fastapi_app(db, [User, Post, Comment])")
    print("   uvicorn.run(app, host='0.0.0.0', port=8000)")

# Step 6: Test your API
print("\n🧪 TESTING YOUR API...")

def test_api_examples():
    """Examples of how to test your API"""
    
    print("🧪 API TESTING EXAMPLES:")
    print("")
    print("1. Using curl (command line):")
    print("   # Create a user")
    print('   curl -X POST "http://localhost:8000/users/" \\')
    print('        -H "Content-Type: application/json" \\')
    print('        -d \'{"name": "John Doe", "email": "john@example.com", "age": 30}\'')
    print("")
    print("   # Get all users")
    print('   curl "http://localhost:8000/users/"')
    print("")
    print("   # Search users")
    print('   curl "http://localhost:8000/users/?age__gte=25&limit=10"')
    print("")
    print("2. Using Python requests:")
    print("   import requests")
    print('   response = requests.post("http://localhost:8000/users/", json={')
    print('       "name": "Jane Doe",')
    print('       "email": "jane@example.com",')
    print('       "age": 28')
    print('   })')
    print('   print(response.json())')
    print("")
    print("3. Using JavaScript fetch:")
    print("   fetch('http://localhost:8000/users/', {")
    print("       method: 'POST',")
    print("       headers: {'Content-Type': 'application/json'},")
    print("       body: JSON.stringify({")
    print("           name: 'Bob Smith',")
    print("           email: 'bob@example.com',")
    print("           age: 35")
    print("       })")
    print("   }).then(response => response.json())")
    print("     .then(data => console.log(data));")
    print("")
    print("4. Interactive documentation:")
    print("   Open http://localhost:8000/docs in your browser")
    print("   Test all endpoints directly in the browser!")

# Step 7: Production deployment
print("\n🚀 PRODUCTION DEPLOYMENT...")

def deployment_guide():
    """Guide for deploying to production"""
    
    print("🚀 DEPLOYMENT OPTIONS:")
    print("")
    print("1. Deploy to Heroku:")
    print("   - Create Procfile: 'web: python app.py'")
    print("   - Set environment variables in Heroku dashboard")
    print("   - git push heroku main")
    print("")
    print("2. Deploy to Railway:")
    print("   - Connect your GitHub repo")
    print("   - Set MONGO_URI environment variable")
    print("   - Automatic deployment on git push")
    print("")
    print("3. Deploy to DigitalOcean App Platform:")
    print("   - Create app from GitHub repo")
    print("   - Configure environment variables")
    print("   - Automatic scaling and SSL")
    print("")
    print("4. Deploy with Docker:")
    print("   - Create Dockerfile")
    print("   - Build: docker build -t my-api .")
    print("   - Run: docker run -p 8000:8000 my-api")
    print("")
    print("📋 PRODUCTION CHECKLIST:")
    print("   ✅ Set secure MONGO_URI")
    print("   ✅ Configure CORS for your domain")
    print("   ✅ Enable HTTPS")
    print("   ✅ Set up monitoring")
    print("   ✅ Configure logging")
    print("   ✅ Set up backups")

# Step 8: Complete example
def complete_example():
    """Complete working example"""
    
    print("\n🎯 COMPLETE EXAMPLE:")
    print("Save this as 'my_api.py' and run it!")
    
    example_code = '''
from gdmongolite import DB, Schema, Email, FieldTypes, quick_serve

# Create database connection
db = DB()

# Define your models
class User(Schema):
    name: FieldTypes.Name
    email: Email
    age: FieldTypes.Age

class Post(Schema):
    title: FieldTypes.Title
    content: FieldTypes.Content
    author_email: Email

# Register models
db.register_schema(User)
db.register_schema(Post)

# Serve API (this starts the web server!)
if __name__ == "__main__":
    quick_serve(db, [User, Post], host="0.0.0.0", port=8000)
'''
    
    print(example_code)
    print("\nThen run: python my_api.py")
    print("Open: http://localhost:8000/docs")
    print("🎉 You have a professional API running!")

if __name__ == "__main__":
    # Run all examples
    app = create_instant_api()
    add_custom_endpoints(app)
    advanced_app = create_advanced_api()
    serve_api()
    test_api_examples()
    deployment_guide()
    complete_example()
    
    print("\n" + "="*60)
    print("🎉 CONGRATULATIONS!")
    print("You just learned how to create professional web APIs!")
    print("You can now:")
    print("✅ Create REST APIs instantly")
    print("✅ Add custom endpoints")
    print("✅ Handle web requests professionally")
    print("✅ Deploy to production")
    print("✅ Test your APIs")
    print("\nYou're now a Web API expert! 🌐")
    print("="*60)
    
    print("\n🎓 NEXT STEPS:")
    print("1. Try examples/03_data_import_export.py")
    print("2. Try examples/04_advanced_queries.py")
    print("3. Build your own API project!")
    print("4. Deploy to the cloud! 🚀")
    
    # Uncomment to actually start the server
    # quick_serve(db, [User, Post, Comment], host="0.0.0.0", port=8000)