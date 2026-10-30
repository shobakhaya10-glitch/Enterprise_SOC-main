import sqlite3


DATABASE = "database/soc.db"


def show_dashboard():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    # ==============================
    # SECURITY SUMMARY
    # ==============================

    cursor.execute("SELECT COUNT(*) FROM security_events")
    total_events = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM security_events
        WHERE status = 'SUCCESS'
    """)
    successful_logins = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM security_events
        WHERE status = 'FAILED'
    """)
    failed_logins = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM security_events
        WHERE username LIKE 'NETWORK:%'
    """)
    network_events = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM security_events
        WHERE username LIKE 'PORT:%'
    """)
    port_events = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM security_alerts
        WHERE severity = 'HIGH'
    """)
    high_alerts = cursor.fetchone()[0]

    # ==============================
    # RECENT EVENTS
    # ==============================

    cursor.execute("""
        SELECT timestamp, username, status
        FROM security_events
        ORDER BY id DESC
        LIMIT 10
    """)
    recent_events = cursor.fetchall()

    # ==============================
    # RECENT ALERTS
    # ==============================

    cursor.execute("""
        SELECT timestamp, username, alert_type, severity, details
        FROM security_alerts
        ORDER BY id DESC
        LIMIT 10
    """)
    recent_alerts = cursor.fetchall()

    connection.close()

    # ==============================
    # DISPLAY DASHBOARD
    # ==============================

    print()
    print("========================================")
    print("       ENTERPRISE SOC MONITOR")
    print("========================================")

    print()
    print("SECURITY SUMMARY")
    print("----------------------------------------")
    print(f"Total Events          : {total_events}")
    print(f"Successful Logins     : {successful_logins}")
    print(f"Failed Logins         : {failed_logins}")
    print(f"Network Events        : {network_events}")
    print(f"Port Events           : {port_events}")
    print(f"HIGH Alerts           : {high_alerts}")

    print()
    print("RECENT SECURITY EVENTS")
    print("----------------------------------------")

    for event in recent_events:
        timestamp, username, status = event

        if username.startswith("NETWORK:"):
            event_type = "NETWORK"
            event_name = username.replace("NETWORK:", "")

        elif username.startswith("PORT:"):
            event_type = "PORT"
            event_name = username.replace("PORT:", "")

        else:
            event_type = "LOGIN"
            event_name = username

        print(
            f"{timestamp} | "
            f"{event_type:<7} | "
            f"{event_name:<15} | "
            f"{status}"
        )

    print()
    print("RECENT SECURITY ALERTS")
    print("----------------------------------------")

    if recent_alerts:

        for alert in recent_alerts:

            timestamp, username, alert_type, severity, details = alert

            print(f"{timestamp} | {username} | {severity}")
            print(f"Alert  : {alert_type}")
            print(f"Details: {details}")
            print("----------------------------------------")

    else:
        print("No security alerts found.")

    print("========================================")


if __name__ == "__main__":
    show_dashboard()
