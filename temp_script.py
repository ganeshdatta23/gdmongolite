import asyncio
from gdmongolite.schema import db

async def main():
    print("Executing database commands...")
    await db.User.insert({"name":"Alice","email":"a@b.com","age":28})
    print("Inserted user: Alice")
    
    users_cursor = db.User.find(age__gte=18)
    users = await users_cursor.to_list(length=100)
    print("Found users (age >= 18):")
    print(users)

if __name__ == "__main__":
    asyncio.run(main())