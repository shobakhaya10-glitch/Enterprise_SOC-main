def login():
    username = input("Enter username: ")
    password = input("Enetr password: ")

    if username == "admin" and password == "1234":
        print("Access Granted")
    else:
        print("Access Denied")

print("===== Enterprise SOC login System =====")
login()