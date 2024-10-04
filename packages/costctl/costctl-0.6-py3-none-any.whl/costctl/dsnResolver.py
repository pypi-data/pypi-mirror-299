import os
import subprocess
import socket
import requests
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse
import time

def resolve_dns(dns_name, resolution_count):
    for _ in range(resolution_count):
        try:
            ip_address = socket.gethostbyname(dns_name)
            print(f"Resolved IP Address for {dns_name}: {ip_address}")
            return ip_address
        except socket.error as e:
            print(f"Failed to resolve DNS for {dns_name}: {e}")
            # Retry for the specified number of times
    return None

def send_curl_request(url):
    try:
        response = requests.get(url)
        print(f"Response Code for {url}: {response.status_code}")
        print(f"Response Content for {url}:")
        print(response.text)
    except requests.RequestException as e:
        print(f"Failed to send curl request to {url}: {e}")

def main():
    # Get DNS names or IP addresses from environment variable
    os.environ['DNS_LIST'] = "google.com,example.com,github.com,internal-sadc-dev.carbon.lowes.com/test-path/calculator"
    os.environ['NumberOfTimes'] = 10
   # Get DNS names or IP addresses from environment variable
    dns_list_env = "google.com,example.com,github.com,internal-sadc-dev.carbon.lowes.com/test-path/calculator"
    NumberOfTimes = 10

    delay_between_iterations = 15 #15 seconds

    while True:
        with ThreadPoolExecutor() as executor:
            for dns_entry in dns_list.split(','):
                dns_entry = dns_entry.strip()

                parsed_url = urlparse(dns_entry)
                dns_name = parsed_url.netloc if parsed_url.netloc else parsed_url.path

                # Resolve DNS multiple times in parallel
                for _ in range(resolution_count):
                    executor.submit(process_dns_entry, dns_name, resolution_count)

        time.sleep(delay_between_iterations)

def process_dns_entry(dns_entry):

    ip_address = resolve_dns(dns_entry)
    if ip_address:
        # Construct URL with resolved IP address
        url = f"http://{ip_address}"

        # Send curl request
        print(f"Sending curl request to {url}...")
        send_curl_request(url)

if __name__ == "__main__":
    main()