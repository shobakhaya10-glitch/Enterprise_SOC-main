from auth import login
from monitor import show_dashboard
from network import get_network_information, check_connectivity, check_common_ports


def main():

    print("===== ENTERPRISE SOC SYSTEM =====")

    # Initial authentication
    login()

    while True:

        print()
        print("========================================")
        print("       ENTERPRISE SOC SYSTEM")
        print("========================================")
        print("1. Login")
        print("2. Security Dashboard")
        print("3. Network Information")
        print("4. Network & Port Security Scan")
        print("5. Exit")
        print("========================================")

        choice = input("Select an option: ")

        if choice == "1":

            login()

        elif choice == "2":

            show_dashboard()

        elif choice == "3":

            get_network_information()

        elif choice == "4":

            get_network_information()

            print()
            host = input("Enter host to scan: ")

            check_connectivity(host)
            check_common_ports(host)

        elif choice == "5":

            print("Exiting Enterprise SOC System.")
            break

        else:

            print("Invalid option. Please select 1-5.")


if __name__ == "__main__":
    main()
