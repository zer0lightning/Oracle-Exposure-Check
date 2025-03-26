import requests
import json
import csv
import os
import base64
import random
import string
import sys
from colorama import Fore, Back, Style, init

# Initialize colorama
init(autoreset=True)

# Function to set the title of the terminal window
def set_terminal_title():
    if os.name == 'nt':  # Windows
        os.system("title Oracle Exposure Check")
    else:  # Linux or macOS
        print("\033]0;Oracle Exposure Check\007")

# Function to display the tool's information
def print_tool_info():
    print(Fore.CYAN + Style.BRIGHT + "-" * 70)
    print(Fore.LIGHTGREEN_EX + "Oracle Exposure Check")
    print(Fore.LIGHTGREEN_EX + "Author: Lewis Saludo")
    print(Fore.LIGHTGREEN_EX + "Version: 1.0")
    print(Fore.LIGHTGREEN_EX + "Credits: CloudSEK [https://exposure.cloudsek.com/]")
    print(Fore.CYAN + Style.BRIGHT + "-" * 70)
    print(Fore.CYAN + "This tool is provided 'as-is' for educational and informational purposes only.")
    print(Fore.CYAN + "Use at your own risk. The author is not responsible for any misuse, damage, or unintended consequences.")
    print(Fore.CYAN + "Ensure that you have the proper authorization to perform any scans or actions using this tool.")
    print(Fore.CYAN + "It is your responsibility to comply with all applicable laws and regulations.")
    print("\n")
	
# Function to generate a random Base64-encoded Proxy-Authorization key
def generate_proxy_auth_key():
    # Generate a random string of 16 characters to simulate Base64-encoded authorization token
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    base64_encoded = base64.b64encode(random_string.encode('utf-8')).decode('utf-8')
    return f"Basic {base64_encoded}"

# Function to query the domain
def query_domain(domain_input, proxy_auth_value):
    # Define the URL and headers
    url = "https://exposure.cloudsek.com/api/v1/get-oracle-affected"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:136.0) Gecko/20100101 Firefox/136.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",  # Automatically handled by requests
        "Referer": "https://exposure.cloudsek.com/oracle",
        "Origin": "https://exposure.cloudsek.com",
        "DNT": "1",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "no-cors",
        "Sec-Fetch-Site": "same-origin",
        "Sec-GPC": "1",
        "TE": "trailers",
        "Content-Type": "application/json",
        "Proxy-Authorization": f"Basic {proxy_auth_value}"
    }

    payload = {
        "domain": domain_input
    }

    # Make the POST request
    response = requests.post(url, headers=headers, json=payload)

    # Initialize the result values
    domain = "N/A"
    impacted_oracle_attack = "N/A"

    # Check if the response is successful
    if response.status_code == 200:
        try:
            response_json = response.json()  # Try to parse the JSON from the response

            # Extract the domain and impacted_oracle_attack
            domain = response_json.get("domain", "N/A")
            impacted_oracle_attack = "Yes" if response_json.get("impacted_oracle_attack", False) else "No"

        except ValueError:
            # In case JSON parsing fails
            domain = impacted_oracle_attack = "N/A"
    else:
        # If response status is not 200, handle accordingly
        domain = impacted_oracle_attack = "N/A"

    return domain, impacted_oracle_attack

# Function to clear the console window
def clear_console():
    if os.name == 'nt':  # For Windows
        os.system('cls')
    else:  # For Linux/MacOS
        os.system('clear')

# Function to query domains from a file and save results to CSV automatically
def query_domains_from_file(file_path, proxy_auth_value):
    results = []
    try:
        # Clean up the file path by stripping extra spaces and quotes
        file_path = file_path.strip().strip('""')
        
        # Check if the file path is valid
        if not os.path.isfile(file_path):
            print(Fore.RED + f"File '{file_path}' does not exist or is not a valid file path.")
            return

        with open(file_path, 'r') as file:
            domains = file.readlines()  # Read all lines from the file
            domains = [domain.strip() for domain in domains]  # Strip whitespace/newlines

            # Query each domain and store results
            for domain in domains:
                domain_result, impacted_oracle_attack = query_domain(domain, proxy_auth_value)

                # Print the result for real-time feedback
                print(Fore.YELLOW + f"Domain: {domain_result} | Impacted Oracle Attack: {impacted_oracle_attack}")

                # Store the results for later CSV export
                results.append({'Domain': domain_result, 'Impacted Oracle Attack': impacted_oracle_attack})

            # Automatically save the results to a CSV file after querying all domains
            csv_filename = "oracle_attack_results.csv"
            csv_file_path = os.path.join(os.getcwd(), csv_filename)

            # Open the CSV file for writing
            with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
                fieldnames = ['Domain', 'Impacted Oracle Attack']
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(results)

            print(Fore.GREEN + f"Results have been automatically saved to '{csv_file_path}'.")

            # Prompt to ask the user if they want to continue or exit
            continue_choice = input(Fore.LIGHTMAGENTA_EX + "Do you want to continue? (y/n): ").strip().lower()
            if continue_choice != 'y':
                print(Fore.RED + "Exiting the program...")
                sys.exit(0)
            else:
                clear_console()  # Clear the console window
                print_tool_info()  # Print the tool information again
                print(Fore.CYAN + f"Generated Proxy-Authorization key: {proxy_auth_value}")

                # Ask the user if they want to check a single domain or multiple domains from a file again
                continue_check_option = input(Fore.LIGHTBLUE_EX + "Scan single Domain or provide a list file? (single/list): ").strip().lower()
                if continue_check_option == "single":
                    domain_input = input(Fore.LIGHTBLUE_EX + "Please provide the domain to check: ").strip()
                    domain_result, impacted_oracle_attack = query_domain(domain_input, proxy_auth_value)
                    print(Fore.YELLOW + f"Domain: {domain_result} | Impacted Oracle Attack: {impacted_oracle_attack}")

                    # Automatically save the result to CSV after querying the single domain
                    results = [{'Domain': domain_result, 'Impacted Oracle Attack': impacted_oracle_attack}]
                    csv_filename = "oracle_attack_results.csv"
                    csv_file_path = os.path.join(os.getcwd(), csv_filename)

                    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
                        fieldnames = ['Domain', 'Impacted Oracle Attack']
                        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                        writer.writeheader()
                        writer.writerows(results)

                    print(Fore.GREEN + f"Results have been automatically saved to '{csv_file_path}'.")

                    # Ask if the user wants to continue or exit
                    continue_choice = input(Fore.LIGHTMAGENTA_EX + "Do you want to continue? (y/n): ").strip().lower()
                    if continue_choice != 'y':
                        print(Fore.RED + "Exiting the program...")
                        sys.exit(0)
                    else:
                        clear_console()
                        print_tool_info()

                elif continue_check_option == "list":
                    file_input = input(Fore.LIGHTBLUE_EX + "Enter the path to the file containing domains (one per line): ").strip()
                    query_domains_from_file(file_input, proxy_auth_value)

                else:
                    print(Fore.RED + "Invalid option. Please choose either 'single' or 'list'.")

    except FileNotFoundError:
        print(Fore.RED + f"File '{file_path}' not found.")
    except Exception as e:
        print(Fore.RED + f"An error occurred: {e}")

# Option for file input and Proxy-Authorization input
def main():
    try:
        set_terminal_title()  # Set the terminal window title

        print_tool_info()  # Display tool information at the beginning

        # Generate the Proxy-Authorization key
        proxy_auth_value = generate_proxy_auth_key()
        print(Fore.CYAN + f"Generated Proxy-Authorization key: {proxy_auth_value}")

        # Ask if the user wants to check a single domain or multiple domains from a file
        check_option = input(Fore.LIGHTBLUE_EX + "Scan single Domain or provide a list file? (single/list): ").strip().lower()

        if check_option == "single":
            domain_input = input(Fore.LIGHTBLUE_EX + "Please provide the domain to check: ").strip()
            domain_result, impacted_oracle_attack = query_domain(domain_input, proxy_auth_value)
            print(Fore.YELLOW + f"Domain: {domain_result} | Impacted Oracle Attack: {impacted_oracle_attack}")

            # Automatically save the result to CSV after querying the single domain
            results = [{'Domain': domain_result, 'Impacted Oracle Attack': impacted_oracle_attack}]
            csv_filename = "oracle_attack_results.csv"
            csv_file_path = os.path.join(os.getcwd(), csv_filename)

            with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
                fieldnames = ['Domain', 'Impacted Oracle Attack']
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(results)

            print(Fore.GREEN + f"Results have been automatically saved to '{csv_file_path}'.")

            # Ask if the user wants to continue or exit
            continue_choice = input(Fore.LIGHTMAGENTA_EX + "Do you want to continue? (y/n): ").strip().lower()
            if continue_choice != 'y':
                print(Fore.RED + "Exiting the program...")
                sys.exit(0)
            else:
                clear_console()  # Clear the console window
                print_tool_info()  # Print the tool information again
                print(Fore.CYAN + f"Generated Proxy-Authorization key: {proxy_auth_value}")

                # Ask if the user wants to check a single domain or multiple domains from a file again
                continue_check_option = input(Fore.LIGHTBLUE_EX + "Scan single domain or provide a list file? (single/list): ").strip().lower()
                if continue_check_option == "single":
                    domain_input = input(Fore.LIGHTBLUE_EX + "Please provide the domain to check: ").strip()
                    domain_result, impacted_oracle_attack = query_domain(domain_input, proxy_auth_value)
                    print(Fore.YELLOW + f"Domain: {domain_result} | Impacted Oracle Attack: {impacted_oracle_attack}")

                    # Automatically save the result to CSV after querying the single domain
                    results = [{'Domain': domain_result, 'Impacted Oracle Attack': impacted_oracle_attack}]
                    csv_filename = "oracle_attack_results.csv"
                    csv_file_path = os.path.join(os.getcwd(), csv_filename)

                    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
                        fieldnames = ['Domain', 'Impacted Oracle Attack']
                        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                        writer.writeheader()
                        writer.writerows(results)

                    print(Fore.GREEN + f"Results have been automatically saved to '{csv_file_path}'.")

                    # Ask if the user wants to continue or exit
                    continue_choice = input(Fore.LIGHTMAGENTA_EX + "Do you want to continue? (y/n): ").strip().lower()
                    if continue_choice != 'y':
                        print(Fore.RED + "Exiting the program...")
                        sys.exit(0)
                    else:
                        clear_console()
                        print_tool_info()

                elif continue_check_option == "list":
                    file_input = input(Fore.LIGHTBLUE_EX + "Enter the path to the file containing domains (one per line): ").strip()
                    query_domains_from_file(file_input, proxy_auth_value)

                else:
                    print(Fore.RED + "Invalid option. Please choose either 'single' or 'list'.")

    except KeyboardInterrupt:
        print(Fore.RED + "\nProcess interrupted by user. Exiting...")
        sys.exit(0)

if __name__ == "__main__":
    main()
