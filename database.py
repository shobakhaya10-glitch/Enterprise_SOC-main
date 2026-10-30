import sqlite3


DATABASE = "database/soc.db"


def create_database():
    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS security_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            username TEXT NOT NULL,
            status TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def save_event(timestamp, username, status):
    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO security_events (timestamp, username, status)
        VALUES (?, ?, ?)
    """, (timestamp, username, status))

    connection.commit()
    connection.close()


if __name__ == "__main__":
    create_database()
    print("SOC database initialized successfully.")
