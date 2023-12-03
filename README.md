# SIP  
[![CI](https://github.com/xNatthapol/SIP/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/xNatthapol/SIP/actions/workflows/ci.yml)

SIP is a web-based application, designed to cater to cocktail enthusiasts, home bartenders, and anyone interested in mixing and enjoying liquors and cocktails. The app serves as a comprehensive resource for alcoholic drink recipes, and community engagement.

## Requirements

Requires Python 3.8 and later.  Required Python packages are listed in [requirements.txt](./requirements.txt).

## Install and Run

### How to Install and Configure

You can install and configure the project by following the [Installation](Installation.md).

### How to Run

1. Activate the Virtual Environment
- On MacOS or Linux
    ```bash
    source venv/bin/activate
    ```
- On Windows
    ```cmd
    venv\Scripts\activate
    ```

2. Start the Django Development Server
   > **Note:** If python is not found, try using `python3` instead of `python`.
    ```bash
    python manage.py runserver
    ```
    If you receive an error message indicating that the port is unavailable, try running the server on a different port (1024 thru 65535), such as
    ```bash
    python manage.py runserver 12345
    ```

3. Navigate to http://localhost:8000 in your web browser.
   
4. To stop the server, press **Ctrl-C** / **control-C** in the terminal window.

5. Exit the virtual environment by closing the window or typing
    ```bash
    deactivate
    ```

## Demo Accounts

### Demo Admin

| Username  | Password |
|:---------:|:--------:|
|   admin   |   admin  |

This is the admin we generated as a demo. You can use this to login to the admin page of SIP app.

## Project Documents

All project documents are in the [Project Wiki](../../wiki/Home).

### Documents
- [Vision Statement](../../wiki/Vision%20Statement)
- [Requirements](../../wiki/Requirements)
- [Development Plan](../../wiki/Development%20Plan)
- [Coding Standard](../../wiki/Coding%20Standard)

### Iteration Plans
- [Iteration 1 Plan](../../wiki/Iteration%201%20Plan)
- [Iteration 2 Plan](../../wiki/Iteration%202%20Plan)
- [Iteration 3 Plan](../../wiki/Iteration%203%20Plan)
- [Iteration 4 Plan](../../wiki/Iteration%204%20Plan)
- [Iteration 5 Plan](../../wiki/Iteration%205%20Plan)