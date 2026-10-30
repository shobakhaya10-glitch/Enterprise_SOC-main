import socket
import subprocess
from datetime import datetime
from database import save_event


def get_network_information():
    hostname = socket.gethostname()

    try:
        result = subprocess.run(
            ["ip", "-4", "addr", "show", "enp0s3"],
            capture_output=True,
            text=True
        )

        ip_address = "Unable to determine IP address"

        for line in result.stdout.splitlines():
            line = line.strip()

            if line.startswith("inet "):
                ip_address = line.split()[1].split("/")[0]
                break

    except Exception:
        ip_address = "Unable to determine IP address"

    print("========================================")
    print("       NETWORK MONITOR")
    print("========================================")
    print(f"Hostname          : {hostname}")
    print(f"Network Interface : enp0s3")
    print(f"IP Address        : {ip_address}")
    print("========================================")


def check_connectivity(host):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        result = subprocess.run(
            ["ping", "-c", "1", "-W", "2", host],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        if result.returncode == 0:
            print(f"Host {host} is reachable.")

            save_event(
                timestamp,
                f"NETWORK:{host}",
                "REACHABLE"
            )

            return True

        else:
            print(f"Host {host} is unreachable.")

            save_event(
                timestamp,
                f"NETWORK:{host}",
                "UNREACHABLE"
            )

            return False

    except Exception:
        print("Unable to perform connectivity test.")

        save_event(
            timestamp,
            f"NETWORK:{host}",
            "ERROR"
        )

        return False


def check_port(host, port):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)

    try:
        result = sock.connect_ex((host, port))

        if result == 0:
            print(f"Port {port:<5}: OPEN")

            save_event(
                timestamp,
                f"PORT:{host}:{port}",
                "OPEN"
            )

        else:
            print(f"Port {port:<5}: CLOSED")

            save_event(
                timestamp,
                f"PORT:{host}:{port}",
                "CLOSED"
            )

    except Exception:
        print(f"Port {port:<5}: ERROR")

        save_event(
            timestamp,
            f"PORT:{host}:{port}",
            "ERROR"
        )

    finally:
        sock.close()


def check_common_ports(host):
    print()
    print("PORT MONITOR")
    print("----------------------------------------")

    ports = [22, 80, 443]

    for port in ports:
        check_port(host, port)


if __name__ == "__main__":
    get_network_information()

    host = input("Enter host to test: ")

    check_connectivity(host)
    check_common_ports(host)
