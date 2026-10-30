import hashlib

password = input("Enter your password: ")

hashed_password = hashlib.sha256(password.encode()).hexdigest()

print("Hashed password:")
print(hashed_password)