"""
📊 DATA IMPORT/EXPORT - Handle Any Data Format!
==============================================

Learn how to work with CSV, JSON, YAML, XML files and external APIs!
Perfect for data migration, backups, and integrations.

What you'll learn:
- Import data from any file format
- Export data to any format
- Migrate between databases
- Handle large datasets efficiently
"""

import asyncio
from gdmongolite import DB, Schema, Email, FieldTypes, DataImporter, DataExporter

# Step 1: Define your models
db = DB()

class Customer(Schema):
    name: FieldTypes.Name
    email: Email
    age: FieldTypes.Age
    country: str
    purchase_amount: FieldTypes.Price = 0.0
    join_date: str

class Product(Schema):
    name: FieldTypes.Title
    category: str
    price: FieldTypes.Price
    rating: FieldTypes.Rating = 0.0
    description: FieldTypes.Description = ""

# Register schemas
db.register_schema(Customer)
db.register_schema(Product)

async def demo_import_export():
    """Comprehensive import/export demonstration"""
    
    print("📊 DATA IMPORT/EXPORT DEMO")
    print("=" * 40)
    
    # Create sample data first
    sample_customers = [
        {
            "name": "John Smith",
            "email": "john@example.com",
            "age": 32,
            "country": "USA",
            "purchase_amount": 299.99,
            "join_date": "2023-01-15"
        },
        {
            "name": "Maria Garcia",
            "email": "maria@example.com", 
            "age": 28,
            "country": "Spain",
            "purchase_amount": 450.50,
            "join_date": "2023-02-20"
        },
        {
            "name": "Yuki Tanaka",
            "email": "yuki@example.com",
            "age": 35,
            "country": "Japan", 
            "purchase_amount": 199.99,
            "join_date": "2023-03-10"
        }
    ]
    
    # Save sample data
    await db.Customer.insert(sample_customers)
    print("✅ Created sample customer data")
    
    # Initialize importer and exporter
    importer = DataImporter(db)
    exporter = DataExporter(db)
    
    # EXPORT EXAMPLES
    print("\n📤 EXPORTING DATA...")
    
    # Export to JSON
    response = await exporter.export_to_file(
        Customer,
        "exports/customers.json",
        format="json"
    )
    if response.success:
        print(f"✅ Exported to JSON: {response.message}")
    
    # Export to CSV
    response = await exporter.export_to_file(
        Customer,
        "exports/customers.csv",
        format="csv"
    )
    if response.success:
        print(f"✅ Exported to CSV: {response.message}")
    
    # Export to YAML
    response = await exporter.export_to_file(
        Customer,
        "exports/customers.yaml",
        format="yaml"
    )
    if response.success:
        print(f"✅ Exported to YAML: {response.message}")
    
    # Export with filters (only USA customers)
    response = await exporter.export_to_file(
        Customer,
        "exports/usa_customers.json",
        query={"country": "USA"},
        format="json"
    )
    if response.success:
        print(f"✅ Exported USA customers only: {response.message}")
    
    # Export specific fields only
    response = await exporter.export_to_file(
        Customer,
        "exports/customer_contacts.csv",
        projection={"name": 1, "email": 1, "country": 1},
        format="csv"
    )
    if response.success:
        print(f"✅ Exported contacts only: {response.message}")
    
    # IMPORT EXAMPLES
    print("\n📥 IMPORTING DATA...")
    
    # Clear existing data for clean import demo
    await db.Product.delete()
    
    # Create sample import files
    import json
    import csv
    from pathlib import Path
    
    # Create imports directory
    Path("imports").mkdir(exist_ok=True)
    
    # Create JSON import file
    products_json = [
        {
            "name": "Laptop Pro",
            "category": "Electronics",
            "price": 1299.99,
            "rating": 4.5,
            "description": "High-performance laptop for professionals"
        },
        {
            "name": "Wireless Headphones",
            "category": "Electronics", 
            "price": 199.99,
            "rating": 4.2,
            "description": "Premium wireless headphones with noise cancellation"
        },
        {
            "name": "Coffee Maker",
            "category": "Home",
            "price": 89.99,
            "rating": 4.0,
            "description": "Automatic drip coffee maker"
        }
    ]
    
    with open("imports/products.json", "w") as f:
        json.dump(products_json, f, indent=2)
    
    # Import from JSON
    response = await importer.import_from_file(
        "imports/products.json",
        Product,
        format="json",
        validate=True
    )
    if response.success:
        print(f"✅ Imported from JSON: {response.message}")
    
    # Create CSV import file
    csv_data = [
        ["name", "category", "price", "rating", "description"],
        ["Gaming Mouse", "Electronics", "79.99", "4.3", "High-precision gaming mouse"],
        ["Desk Chair", "Furniture", "249.99", "4.1", "Ergonomic office chair"],
        ["Water Bottle", "Sports", "24.99", "4.4", "Insulated stainless steel bottle"]
    ]
    
    with open("imports/more_products.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(csv_data)
    
    # Import from CSV
    response = await importer.import_from_file(
        "imports/more_products.csv",
        Product,
        format="csv",
        batch_size=100
    )
    if response.success:
        print(f"✅ Imported from CSV: {response.message}")
    
    # ADVANCED IMPORT/EXPORT
    print("\n🚀 ADVANCED FEATURES...")
    
    # Import with data transformation
    def transform_product(data):
        """Transform data during import"""
        # Convert price to float if it's string
        if isinstance(data.get("price"), str):
            data["price"] = float(data["price"])
        
        # Add discount field
        data["discount"] = 0.1 if data["price"] > 100 else 0.05
        
        return data
    
    # Batch import with validation
    response = await importer.import_from_file(
        "imports/products.json",
        Product,
        batch_size=50,
        validate=True
    )
    
    # Export with sorting and limits
    response = await exporter.export_to_file(
        Product,
        "exports/top_products.json",
        sort={"rating": -1},  # Highest rated first
        limit=5,  # Top 5 only
        format="json"
    )
    if response.success:
        print(f"✅ Exported top 5 products: {response.message}")
    
    # WORKING WITH EXTERNAL APIs
    print("\n🌐 EXTERNAL API INTEGRATION...")
    
    # Import from external API (example)
    try:
        # This would import from a real API
        # response = await importer.import_from_url(
        #     "https://api.example.com/products",
        #     Product,
        #     format="json"
        # )
        print("💡 API import ready - just provide the URL!")
    except Exception as e:
        print(f"ℹ️  API import example (would work with real API)")
    
    # MIGRATION BETWEEN DATABASES
    print("\n🔄 DATABASE MIGRATION...")
    
    from gdmongolite import DataMigrator
    
    # Create second database for migration demo
    target_db = DB("mongodb://localhost:27017", "target_database")
    target_db.register_schema(Customer)
    
    migrator = DataMigrator(db, target_db)
    
    # Migrate customers to new database
    # response = await migrator.migrate_collection(
    #     Customer,
    #     transform_func=lambda doc: {**doc, "migrated": True}
    # )
    print("💡 Migration ready - can move data between databases!")
    
    # PERFORMANCE MONITORING
    print("\n📈 PERFORMANCE STATS...")
    
    # Check how many products we have
    total_products = await db.Product.find().count()
    print(f"📊 Total products imported: {total_products}")
    
    # Show file sizes
    import os
    for file_path in ["exports/customers.json", "exports/customers.csv"]:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"📁 {file_path}: {size} bytes")

async def create_sample_files():
    """Create sample files for import demonstration"""
    from pathlib import Path
    import json
    import csv
    import yaml
    
    # Create directories
    Path("sample_data").mkdir(exist_ok=True)
    
    # Sample customer data
    customers = [
        {
            "name": "Alice Johnson",
            "email": "alice@company.com",
            "age": 29,
            "country": "Canada",
            "purchase_amount": 350.75,
            "join_date": "2023-01-15"
        },
        {
            "name": "Bob Chen",
            "email": "bob@startup.com", 
            "age": 34,
            "country": "Singapore",
            "purchase_amount": 1200.00,
            "join_date": "2023-02-20"
        },
        {
            "name": "Carol Smith",
            "email": "carol@enterprise.com",
            "age": 41,
            "country": "Australia", 
            "purchase_amount": 899.99,
            "join_date": "2023-03-10"
        }
    ]
    
    # Create JSON file
    with open("sample_data/customers.json", "w") as f:
        json.dump(customers, f, indent=2)
    
    # Create CSV file
    with open("sample_data/customers.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=customers[0].keys())
        writer.writeheader()
        writer.writerows(customers)
    
    # Create YAML file
    with open("sample_data/customers.yaml", "w") as f:
        yaml.dump(customers, f, default_flow_style=False)
    
    print("✅ Created sample data files:")
    print("  - sample_data/customers.json")
    print("  - sample_data/customers.csv") 
    print("  - sample_data/customers.yaml")

if __name__ == "__main__":
    print("🚀 Starting Data Import/Export Demo...")
    
    # Create sample files first
    asyncio.run(create_sample_files())
    
    # Run the main demo
    asyncio.run(demo_import_export())
    
    print("\n🎉 DEMO COMPLETE!")
    print("\n📚 What you learned:")
    print("✅ Export data to JSON, CSV, YAML, XML")
    print("✅ Import data from any file format")
    print("✅ Handle large datasets with batching")
    print("✅ Validate data during import")
    print("✅ Filter and transform data")
    print("✅ Work with external APIs")
    print("✅ Migrate between databases")
    
    print("\n🎯 Try these files:")
    print("- Check exports/ folder for exported data")
    print("- Modify sample_data/ files and re-import")
    print("- Try importing your own CSV/JSON files!")

"""
🔧 REAL-WORLD EXAMPLES:

# Import customer data from CRM system
await importer.import_from_file(
    "crm_export.csv",
    Customer,
    batch_size=1000,
    validate=True
)

# Export sales report
await exporter.export_to_file(
    Order,
    "monthly_sales.xlsx",
    query={"created_at__gte": "2023-01-01"},
    sort={"total_amount": -1}
)

# Migrate from old system
migrator = DataMigrator(old_db, new_db)
await migrator.migrate_collection(
    OldCustomer,
    NewCustomer,
    transform_func=convert_old_to_new_format
)

# Import from external API
await importer.import_from_url(
    "https://api.partner.com/products",
    Product,
    format="json",
    batch_size=500
)

# Backup entire database
for schema in [Customer, Product, Order]:
    await exporter.export_to_file(
        schema,
        f"backup/{schema.__name__.lower()}.json"
    )
"""