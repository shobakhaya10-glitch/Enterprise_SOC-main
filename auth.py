import json
from datetime import datetime
from hashing import hash_password
from database import save_event
from alerts import check_failed_logins


def log_login(username, status):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("logs/login.log", "a") as file:
        file.write(
            f"{timestamp} - Username: {username} - Status: {status}\n"
        )

    save_event(timestamp, username, status)


def login():

    with open("users.json", "r") as file:
        users = json.load(file)

    attempt = 1

    while attempt <= 3:

        username = input("Enter username: ")
        password = input("Enter password: ")

        entered_password_hash = hash_password(password)

        if username in users:

            stored_password_hash = users[username]["password"]

            if entered_password_hash == stored_password_hash:

                print("Access Granted")
                log_login(username, "SUCCESS")

                return True

        print("Access Denied")
        log_login(username, "FAILED")

        check_failed_logins(username)

        attempt += 1

    print("Too many failed login attempts.")

    return False


if __name__ == "__main__":
    print("===== Enterprise SOC Login System =====")
    login()
