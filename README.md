# Join

Linear: https://linear.app/unimus/join/5d88102e95523f2bf021fb5b5a538e3b?s=4

Publish: packagesub@unimus.odoo.com

---
# Unimus Documentation

Unimus is a versatile security tool designed to perform various network and web-related tasks. It allows you to perform FTP brute-force attacks, gather links from websites, save webpages, install modules from GitHub repositories, and much more. Unimus is a powerful and flexible tool for security professionals and enthusiasts.

---

## Table of Contents
- [Installation](#installation)
- [Features](#features)
  - [FTP Brute Force Attack](#ftp-brute-force-attack)
  - [Web Tree Scanning](#web-tree-scanning)
  - [Save Webpage](#save-webpage)
  - [Module Management](#module-management)
- [Usage](#usage)
- [License](#license)
- [Contributing](#contributing)

---

## Installation

Before you start using Unimus, you need to install the required dependencies. You can install them using the following command:

```bash
pip install requests colorama tabulate beautifulsoup4
```

Once the dependencies are installed, you can run the program with:

```bash
python main.py
```

---

## Features

### FTP Brute Force Attack

Unimus allows you to perform a brute-force attack on FTP servers by attempting multiple username and password combinations.

**Configuration:**
- **host**: The target FTP server's IP or domain.
- **port**: The default FTP port is 21.
- **username**: The username to attempt.
- **wordlist**: A file containing potential passwords.

**Example:**
To start the FTP brute-force attack package:

```bash
package ftpbruteforce
```

Set the parameters using the following commands:

```bash
set host 192.168.1.1
set username admin
set wordlist /path/to/wordlist.txt
```

To start the attack, use the `run` command.

---

### Web Tree Scanning

Unimus can extract and analyze links from a given website. It allows you to recursively scan and gather links to a specified depth.

**Configuration:**
- **url**: The website to scan.
- **depth**: The depth of the link recursion (default is 2).

**Example:**
To run the web tree scanning package:

```bash
package webtree
```

Set the parameters:

```bash
set url https://example.com
set depth 3
```

To start the scan, use the `run` command.

---

### Save Webpage

Unimus allows you to save a webpage locally for offline analysis.

**Example:**
To save a webpage:

```bash
freeze_web https://example.com
```

This will save the webpage as an `.html` file.

---

### Module Management

Unimus allows you to load and install custom modules from GitHub repositories. Modules are placed in the `mods/` directory and can be executed directly.

**Install Module from GitHub:**
To install a module from GitHub, use:

```bash
package install <module_name>
```

**Example:**
```bash
package install ftpbruteforce
```

---

## Usage

Once you launch the program with `python unimus.py`, you can interact with it via the command-line interface. Unimus provides a simple CLI where you can select packages, set parameters, and run tasks.

**Example Workflow:**
1. Start the program:
   ```bash
   python main.py
   ```

2. Choose a package (e.g., FTP brute-force):
   ```bash
   package ftpbruteforce
   ```

3. Set the parameters for the package:
   ```bash
   set host 192.168.1.1
   set username admin
   set wordlist /path/to/wordlist.txt
   ```

4. Run the package:
   ```bash
   run
   ```

5. If needed, you can go back to the main menu:
   ```bash
   back
   ```

---

## License

Unimus is an open-source project. Feel free to use it for educational purposes and security testing. **Please use this tool responsibly and ensure you have proper authorization before testing any systems.**

---

## Contributing

If you'd like to contribute to Unimus, feel free to fork the repository and create a pull request. Contributions are always welcome!
