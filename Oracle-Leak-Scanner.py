import requests
import json
import csv
import os
import base64
import random
import string

# Function to display the tool's information
def print_tool_info():
    print("-" * 50)
    print("Oracle Leak Scanner")
    print("Author: Lewis Saludo")
    print("Version: 1.0")
    print("Credits: CloudSEK API")
    print("-" * 50)

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


# Function to query domains from a file and save results to CSV automatically
def query_domains_from_file(file_path, proxy_auth_value):
    results = []
    try:
        with open(file_path, 'r') as file:
            domains = file.readlines()  # Read all lines from the file
            domains = [domain.strip() for domain in domains]  # Strip whitespace/newlines

            # Query each domain and store results
            for domain in domains:
                domain_result, impacted_oracle_attack = query_domain(domain, proxy_auth_value)

                # Print the result for real-time feedback
                print(f"Domain: {domain_result} | Impacted Oracle Attack: {impacted_oracle_attack}")

                # Store the results for later CSV export
                results.append({'Domain': domain_result, 'Impacted Oracle Attack': impacted_oracle_attack})

            # Automatically save the results to a CSV file after querying all domains
            csv_filename = "oracle_attack_results.csv"
            csv_file_path = os.path.join(os.getcwd(), csv_filename)

            # Open the CSV file for writing
            with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
                fieldnames = ['Domain', 'Impacted Oracle Attack']
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

                # Write the header to the CSV file
                writer.writeheader()

                # Write the results to the CSV file
                writer.writerows(results)

            print(f"Results have been automatically saved to '{csv_file_path}'.")

    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


# Option for file input and Proxy-Authorization input
print_tool_info()  # Display tool information at the beginning

# Generate the Proxy-Authorization key
proxy_auth_value = generate_proxy_auth_key()
print(f"Generated Proxy-Authorization key: {proxy_auth_value}")

# Ask if the user wants to check a single domain or multiple domains from a file
check_option = input("Scan single Domain or provide a list file? (single/list): ").strip().lower()

if check_option == "single":
    domain_input = input("Please provide the domain to check: ").strip()
    domain_result, impacted_oracle_attack = query_domain(domain_input, proxy_auth_value)
    print(f"Domain: {domain_result} | Impacted Oracle Attack: {impacted_oracle_attack}")

    # Automatically save the result to CSV after querying the single domain
    results = [{'Domain': domain_result, 'Impacted Oracle Attack': impacted_oracle_attack}]
    csv_filename = "oracle_attack_results.csv"
    csv_file_path = os.path.join(os.getcwd(), csv_filename)

    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['Domain', 'Impacted Oracle Attack']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"Results have been automatically saved to '{csv_file_path}'.")

elif check_option == "list":
    file_input = input("Enter the path to the file containing domains (one per line): ")
    query_domains_from_file(file_input, proxy_auth_value)

else:
    print("Invalid option. Please choose either 'single' or 'list'.")
