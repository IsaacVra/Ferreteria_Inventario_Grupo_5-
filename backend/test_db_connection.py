import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database configuration
config = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'database': os.getenv('DB_NAME', 'ferreteria_db'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'port': int(os.getenv('DB_PORT', '3307'))
}

print(f"Attempting to connect to MySQL with:")
print(f"Host: {config['host']}")
print(f"Port: {config['port']}")
print(f"User: {config['user']}")
print(f"Database: {config['database']}")
print(f"Password: {'*' * len(config['password']) if config['password'] else '(empty)'}")

try:
    # Try connecting without specifying database first
    connection = mysql.connector.connect(
        host=config['host'],
        user=config['user'],
        password=config['password'],
        port=config['port']
    )
    print("✓ Successfully connected to MySQL server!")
    
    # Check if database exists
    cursor = connection.cursor()
    cursor.execute("SHOW DATABASES")
    databases = cursor.fetchall()
    print(f"Available databases: {[db[0] for db in databases]}")
    
    # Try to connect to the specific database
    if config['database'] in [db[0] for db in databases]:
        print(f"✓ Database '{config['database']}' exists!")
    else:
        print(f"⚠ Database '{config['database']}' does not exist. Creating it...")
        cursor.execute(f"CREATE DATABASE {config['database']}")
        print(f"✓ Database '{config['database']}' created successfully!")
    
    cursor.close()
    connection.close()
    
except mysql.connector.Error as err:
    print(f"✗ MySQL Error: {err}")
    print(f"Error Code: {err.errno}")
    
    # Common issues and solutions
    if err.errno == 1045:
        print("\nPossible solutions:")
        print("1. Check if MySQL server is running")
        print("2. Verify the password is correct")
        print("3. Try connecting with: mysql -u root -p")
        print("4. Check if user 'root'@'localhost' has the correct privileges")
    elif err.errno == 2003:
        print("\nPossible solutions:")
        print("1. Check if MySQL server is running on the specified port")
        print(f"2. Verify port {config['port']} is correct")
        print("3. Check firewall settings")
        
except Exception as e:
    print(f"✗ Unexpected error: {e}")
