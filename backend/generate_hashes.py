from utils.security import hash_password

# Test users and their passwords
test_users = [
    {"username": "kenny.admin", "password": "admin123"},
    {"username": "isaac.manager", "password": "gerente123"},
    {"username": "valeria.jefe", "password": "bodega123"},
    {"username": "ana.vendedor", "password": "ventas123"}
]

print("Generated bcrypt hashes for test users:")
print("-" * 50)
for user in test_users:
    hashed = hash_password(user["password"])
    print(f"Username: {user['username']}")
    print(f"Password: {user['password']}")
    print(f"Bcrypt Hash: {hashed}")
    print("-" * 50)

# Print SQL update statements
print("\nSQL UPDATE statements for datos_ejemplo.sql:")
print("-" * 50)
for user in test_users:
    hashed = hash_password(user["password"])
    print(f"UPDATE USUARIO SET clave_hash = '{hashed}' WHERE usuario_login = '{user['username']}';")
