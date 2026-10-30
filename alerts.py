import sqlite3
from datetime import datetime, timedelta


DATABASE = "database/soc.db"


def check_failed_logins(username):
    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    time_limit = datetime.now() - timedelta(minutes=5)

    cursor.execute("""
        SELECT COUNT(*)
        FROM security_events
        WHERE username = ?
        AND status = 'FAILED'
        AND timestamp >= ?
    """, (username, time_limit.strftime("%Y-%m-%d %H:%M:%S")))

    failed_attempts = cursor.fetchone()[0]

    if failed_attempts >= 3:

        cursor.execute("""
            SELECT COUNT(*)
            FROM security_alerts
            WHERE username = ?
            AND alert_type = 'Multiple Failed Login Attempts'
            AND timestamp >= ?
        """, (username, time_limit.strftime("%Y-%m-%d %H:%M:%S")))

        existing_alert = cursor.fetchone()[0]

        if existing_alert == 0:

            alert_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            cursor.execute("""
                INSERT INTO security_alerts
                (timestamp, username, alert_type, severity, details)
                VALUES (?, ?, ?, ?, ?)
            """, (
                alert_time,
                username,
                "Multiple Failed Login Attempts",
                "HIGH",
                f"{failed_attempts} failed login attempts within 5 minutes"
            ))

            connection.commit()

            print("===== SECURITY ALERT =====")
            print("Multiple failed login attempts detected.")
            print(f"Username: {username}")
            print(f"Failed attempts in the last 5 minutes: {failed_attempts}")
            print("Severity: HIGH")

            connection.close()
            return True

    connection.close()
    return False
