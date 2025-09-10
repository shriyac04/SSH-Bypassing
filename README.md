
# SSH Brute-force Script

A brief description of what this project does and who it's for

SSH Brute Force Script 🔐
## 📌 Overview

This Python script performs a **multi-threaded SSH brute-force attack** using the `paramiko` library. It attempts to connect to a target SSH server with different username and password combinations until valid credentials are found.

⚠️ **Disclaimer**: This script is for **educational and authorized penetration testing purposes only**. Do **NOT** use it against systems you don’t own or don’t have explicit permission to test. Unauthorized usage may be illegal.

---
⚙️ Features

- Multi-threaded brute-force (faster than sequential attempts).
- Gracefully stops when valid credentials are found.
- Handles connection timeouts and blocked attempts.
- Supports loading usernames and passwords from custom wordlists.
- Clean output with success/failure status.

---

## 📦 Requirements

- Python 3.x

- Libraries:

``` pip install paramiko ```

---


## 🚀 Usage

Run the script

` python3 ssh_brute.py <target_ip> `


### Example

` python3 ssh_brute.py 192.168.1.10 `


You will then be prompted for:

- Path to usernames file
- Path to passwords file

### Example input:

```
Enter path to usernames file: usernames.txt
Enter path to passwords file: passwords.txt
```

## 📂 Wordlist Format

- Usernames file (usernames.txt)

```
root
admin
test
```


- Passwords file (passwords.txt)

```
123456
password
qwerty
admin123
```

### 📝 Sample Output
```
Trying root:123456
Trying root:password
[!] Connection timed out or blocked
Trying admin:admin123

[+] SUCCESS: Username: admin | Password: admin123

[+] Found valid credentials: admin:admin123
```

### If no credentials are found:
```
[-] Failed to find valid credentials.
```
--- 

## ⚡ Script Options

- target_ip → The SSH server’s IP address.
- target_port → Defaults to port 22.
- timeout → Connection timeout in seconds (default: 3).
- max_threads → Maximum concurrent threads (default: 15).

---

## ⚠️ Legal Notice

This tool is intended for:

- Ethical hacking training
- Red team exercises
- Security auditing of systems you own or have written permission to test

Unauthorized use against third-party systems may be considered illegal activity. The author is not responsible for misuse.
