"""
ABSOLUTE BEGINNER'S GUIDE TO gdmongolite
========================================

This is your first step into the world's easiest MongoDB toolkit!
No prior MongoDB knowledge required - we'll teach you everything!

What you'll learn:
- How to connect to MongoDB (super easy!)
- How to create data models (like Excel columns but smarter!)
- How to save, find, update, and delete data
- How to become a MongoDB pro in 10 minutes!
"""

# Step 1: Import gdmongolite (this is ALL you need!)
from gdmongolite import DB, Schema, Email, FieldTypes

print("Welcome to gdmongolite - The World's Easiest MongoDB Toolkit!")
print("Let's learn MongoDB the easy way...")

# Step 2: Connect to database (automatic - no configuration needed!)
# gdmongolite automatically connects to MongoDB on your computer
db = DB()
print("Connected to MongoDB automatically!")

# Step 3: Define your data structure (like creating a table in Excel)
# Think of Schema as defining what columns your data will have
class User(Schema):
    """
    This defines what a User looks like in our database
    Think of it like an Excel sheet with these columns:
    - name: Person's name (must be 1-100 characters)
    - email: Email address (automatically validated!)
    - age: Person's age (must be positive number)
    - hobbies: List of things they like (optional)
    """
    name: FieldTypes.Name        # Smart field that validates names
    email: Email                 # Smart field that validates emails
    age: FieldTypes.Age         # Smart field that validates age (0-150)
    hobbies: list[str] = []     # List of hobbies (starts empty)

# Step 4: Register your model with the database
db.register_schema(User)
print("User model registered! Now we can save users to database.")

# Step 5: Let's save some users! (CREATE operation)
print("\nSAVING USERS TO DATABASE...")

async def save_users():
    """Save some example users"""
    
    # Save one user
    response = await db.User.insert({
        "name": "Alice Johnson",
        "email": "alice@example.com", 
        "age": 28,
        "hobbies": ["reading", "coding", "hiking"]
    })
    
    if response.success:
        print(f"Saved Alice! Message: {response.message}")
    else:
        print(f"Error: {response.error}")
    
    # Save multiple users at once
    users_to_save = [
        {
            "name": "Bob Smith",
            "email": "bob@example.com",
            "age": 35,
            "hobbies": ["gaming", "cooking"]
        },
        {
            "name": "Carol Davis", 
            "email": "carol@example.com",
            "age": 42,
            "hobbies": ["painting", "yoga", "traveling"]
        },
        {
            "name": "David Wilson",
            "email": "david@example.com", 
            "age": 29,
            "hobbies": ["music", "photography"]
        }
    ]
    
    response = await db.User.insert(users_to_save)
    if response.success:
        print(f"Saved {response.count} users in one go!")

# Step 6: Find users in the database (READ operation)
print("\nFINDING USERS IN DATABASE...")

async def find_users():
    """Find users with different methods"""
    
    # Find ALL users
    all_users = await db.User.find().to_list()
    print(f"Total users in database: {len(all_users)}")
    
    # Find users by age (older than 30)
    adults = await db.User.find(age__gte=30).to_list()
    print(f"Users 30 or older: {len(adults)}")
    
    # Find users by email domain
    gmail_users = await db.User.find(email__contains="example.com").to_list()
    print(f"Users with example.com email: {len(gmail_users)}")
    
    # Find one specific user
    alice = await db.User.find(name="Alice Johnson").first()
    if alice:
        print(f"Found Alice! She likes: {', '.join(alice['hobbies'])}")
    
    # Find users with specific hobbies
    coders = await db.User.find(hobbies__contains="coding").to_list()
    print(f"Users who like coding: {len(coders)}")

# Step 7: Update users (UPDATE operation)
print("\nUPDATING USERS...")

async def update_users():
    """Update user information"""
    
    # Update one user - add a new hobby to Alice
    response = await db.User.update(
        {"name": "Alice Johnson"},  # Find Alice
        {"$push": {"hobbies": "swimming"}}  # Add swimming to her hobbies
    )
    
    if response.success:
        print("Updated Alice's hobbies!")
    
    # Update multiple users - make everyone a year older
    response = await db.User.update(
        {},  # Empty filter = all users
        {"$inc": {"age": 1}}  # Increase age by 1
    )
    
    if response.success:
        print(f"Made {response.count} users one year older!")

# Step 8: Delete users (DELETE operation)
print("\nDELETING USERS...")

async def delete_users():
    """Delete users (be careful with this!)"""
    
    # Delete users over 50 (none in our example, so safe)
    response = await db.User.delete(age__gt=50)
    print(f"Deleted {response.count} users over 50")
    
    # Count remaining users
    remaining = await db.User.find().count()
    print(f"Users remaining: {remaining}")

# Step 9: Advanced queries (you're becoming a pro!)
print("\nADVANCED QUERIES (You're getting good at this!)...")

async def advanced_queries():
    """More complex database queries"""
    
    # Find users between ages 25-35 who like coding
    tech_users = await db.User.find(
        age__gte=25,
        age__lte=35, 
        hobbies__contains="coding"
    ).to_list()
    print(f"Tech users (25-35): {len(tech_users)}")
    
    # Get users sorted by age (youngest first)
    sorted_users = await db.User.find().sort("age").to_list()
    print("Users by age (youngest first):")
    for user in sorted_users:
        print(f"  - {user['name']}: {user['age']} years old")
    
    # Get only names and emails (not all data)
    names_emails = await db.User.find().project("name", "email").to_list()
    print("Names and emails only:")
    for user in names_emails:
        print(f"  - {user['name']}: {user['email']}")
    
    # Pagination - get first 2 users
    first_page = await db.User.find().limit(2).to_list()
    print(f"First page (2 users): {len(first_page)} users")
    
    # Get next 2 users
    second_page = await db.User.find().skip(2).limit(2).to_list()
    print(f"Second page (next 2 users): {len(second_page)} users")

# Step 10: Error handling (what happens when things go wrong)
print("\nERROR HANDLING...")

async def handle_errors():
    """Learn how gdmongolite handles errors"""
    
    # Try to save invalid data
    response = await db.User.insert({
        "name": "",  # Empty name (invalid!)
        "email": "not-an-email",  # Invalid email!
        "age": -5  # Negative age (invalid!)
    })
    
    if not response.success:
        print(f"Validation caught the error: {response.error}")
        print("gdmongolite protected your database from bad data!")
    
    # Try to find non-existent user
    missing_user = await db.User.find(name="Non Existent").first()
    if missing_user is None:
        print("User not found - gdmongolite returns None (not an error)")

# Step 11: Run everything!
async def main():
    """Run all our examples"""
    print("\n" + "="*50)
    print("RUNNING ALL EXAMPLES...")
    print("="*50)
    
    await save_users()
    await find_users()
    await update_users()
    await advanced_queries()
    await handle_errors()
    await delete_users()
    
    print("\n" + "="*50)
    print("CONGRATULATIONS!")
    print("You just learned MongoDB with gdmongolite!")
    print("You can now:")
    print("- Save data to MongoDB")
    print("- Find data with complex queries")
    print("- Update data safely")
    print("- Delete data when needed")
    print("- Handle errors gracefully")
    print("\nYou're now a MongoDB pro!")
    print("="*50)

# For sync users (if you prefer non-async code)
def sync_example():
    """Same operations but synchronous (no async/await)"""
    print("\nSYNC VERSION (no async/await needed)...")
    
    # Save user (sync version)
    response = db.User.insert_sync({
        "name": "Sync User",
        "email": "sync@example.com",
        "age": 25
    })
    print(f"Sync save: {response.message}")
    
    # Find users (sync version)
    users = db.User.find(age__gte=20).to_list_sync()
    print(f"Found {len(users)} users (sync)")
    
    # Update user (sync version)
    response = db.User.update_sync(
        {"name": "Sync User"},
        {"age": 26}
    )
    print(f"Sync update: {response.message}")
    
    # Delete user (sync version)
    response = db.User.delete_sync(name="Sync User")
    print(f"Sync delete: {response.message}")

if __name__ == "__main__":
    # Run the async version
    import asyncio
    asyncio.run(main())
    
    # Run the sync version
    sync_example()
    
    print("\nNEXT STEPS:")
    print("1. Try examples/02_web_api.py to create a web API")
    print("2. Try examples/03_data_import_export.py to work with files")
    print("3. Read the full documentation in README.md")
    print("4. Build something amazing!")