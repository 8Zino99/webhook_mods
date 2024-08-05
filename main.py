import requests
import threading
import time
import os
from pyfiglet import figlet_format
# made by zino-aq 
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    clear_screen()
    title = figlet_format("𝚉𝙸𝙽𝙾", font="big")
    print(f"{Colors.HEADER}{Colors.BOLD}{title}{Colors.ENDC}")

def send_message(webhook_url, content):
    data = {'content': content}
    response = requests.post(webhook_url, json=data)
    if response.status_code == 204:
        print(f"{Colors.OKGREEN}Message sent successfully.{Colors.ENDC}")
    else:
        print(f"{Colors.FAIL}Error sending message: {response.status_code} - {response.text}{Colors.ENDC}")

def send_messages_parallel(webhook_url, content, count, num_threads):
    def worker():
        for _ in range(count // num_threads):
            send_message(webhook_url, content)
            time.sleep(1)  # Delay to respect rate limits

    thread_list = []
    for _ in range(num_threads):
        thread = threading.Thread(target=worker)
        thread_list.append(thread)
        thread.start()

    for thread in thread_list:
        thread.join()

def get_webhook_info(webhook_url):
    response = requests.get(webhook_url)
    if response.status_code == 200:
        webhook_info = response.json()
        print(f"{Colors.OKBLUE}Webhook Information:{Colors.ENDC}")
        for key, value in webhook_info.items():
            print(f"{Colors.OKBLUE}{key}: {value}{Colors.ENDC}")
    else:
        print(f"{Colors.FAIL}Error retrieving webhook info: {response.status_code} - {response.text}{Colors.ENDC}")

def delete_webhook(webhook_url):
    response = requests.delete(webhook_url)
    if response.status_code == 204:
        print(f"{Colors.OKGREEN}Webhook successfully deleted.{Colors.ENDC}")
    else:
        print(f"{Colors.FAIL}Error deleting webhook: {response.status_code} - {response.text}{Colors.ENDC}")

def main():
    print_header()
    print(f"{Colors.OKBLUE}1. Send Message{Colors.ENDC}")
    print(f"{Colors.OKBLUE}2. Get Webhook Info{Colors.ENDC}")
    print(f"{Colors.OKBLUE}3. Delete Webhook{Colors.ENDC}")
    
    choice = input(f"{Colors.BOLD}Select an option (1/2/3): {Colors.ENDC}")
    
    webhook_url = input(f"{Colors.BOLD}Enter the Webhook URL: {Colors.ENDC}")
    
    if choice == '1':
        content = input(f"{Colors.BOLD}Enter the message content: {Colors.ENDC}")
        count = int(input(f"{Colors.BOLD}How many messages to send? {Colors.ENDC}"))
        num_threads = int(input(f"{Colors.BOLD}Number of threads to use? {Colors.ENDC}"))
        send_messages_parallel(webhook_url, content, count, num_threads)
    elif choice == '2':
        get_webhook_info(webhook_url)
    elif choice == '3':
        delete_webhook(webhook_url)
    else:
        print(f"{Colors.FAIL}Invalid selection.{Colors.ENDC}")

if __name__ == "__main__":
    main()
