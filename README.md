# Python-Code-Execution-HTTP-Server

## Description

This project is a Python-based HTTP server that dynamically executes user-provided Python code.

## Key Features:

### 1. Execute Python code snippets via a POST request at the `/execute` endpoint.
### 2. Enforce execution limits, including a 2-second timeout and 100MB memory restriction.

## Prerequisites

- **Python 3** is required to run this project. Ensure that you have **Python 3.6 or higher** installed on your machine.

### Check Python version:
To check if Python 3 is installed, run:
```bash
python --version
```
or
```bash
python3 --version
```

## Installation Instructions For Windows and Linux

### For Windows and Linux:

1. **Open CMD for Windows or Terminal for Linux.**

2. **Install Python 3 (if not installed):**
   - **For Windows:**
     - Visit [Python Downloads](https://www.python.org/downloads/) and download the latest version of Python 3 for Windows.
     - During installation, make sure to **check the box** that says "Add Python to PATH."
   - **For Linux (Ubuntu/Debian):**
     - Run the following commands to install Python 3:
       ```bash
       sudo apt update
       sudo apt install python3 python3-pip
       ```

3. **Clone the repository:**
   ```bash
   git clone https://github.com/Mo-Adel1/Python-Code-Execution-HTTP-Server.git
   ```
4. Navigate to the project directory:
   ```bash
   cd Python-Code-Execution-HTTP-Server
   ```
5. Create venv:
   ```bash
   python -m venv venv
   ```
6. Activate venv:
   - Windows:
   ```bash
   .\venv\Scripts\activate
   ```
   - Linux:
   ```bash
   source venv/bin/activate
   ```
7. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
## Running the Project

To run the project, execute the following command (make sure you are in the root folder):

```bash
python main.py
```


