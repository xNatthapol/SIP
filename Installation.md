## Installation and Configuration

You can install and configure the SIP app by following these steps.

> **Note:** For each step if python is not found, try using `python3` instead of `python`.  

1. Open a command-line interface
    - MacOS or Linux: Open the Terminal.
    - Windows: Open the Command Prompt, PowerShell, or Windows Terminal, depending on which you prefer.

2. Check Python is installed
    ```bash
    python --version
    ```
    > If Python is installed, it should show the version.

3. Clone the repository from GitHub
    ```bash
    git clone https://github.com/xNatthapol/SIP.git
    ```

4. Change the directory to the SIP project
    ```bash
    cd SIP
    ```

5. Create a Virtual Environment
    ```bash
    python -m venv venv
    ```

6. Activate the Virtual Environment
- On MacOS or Linux
    ```bash
    source venv/bin/activate
    ```
- On Windows
    ```cmd
    venv\Scripts\activate
    ```

7. Install dependencies
    ```bash
    pip install -r requirements.txt
    ```

8. Create .env file and copy the content from sample.env file
- On MacOS or Linux
    ```bash
    cp sample.env .env
    ```
- On Windows
    ```cmd
    copy sample.env .env
    ```

9. GitHub OAuth Setup  
    - Create access credentials
      - Go to [GitHub Developer Settings](https://github.com/settings/developers)
    
10. Google OAuth Setup
    - Create access credentials
      - Go to [Google Cloud Console](https://console.cloud.google.com/getting-started)

11. Database PostgreSQL Setup
    - Install PostgreSQL
      - Download, install, and setup [PostgreSQL Downloads](https://www.postgresql.org/download/)
    - Set Environment Variables for PostgreSQL  
        Add the following to the .env file
        ```env
        DATABASE_URL=postgres://<username>:<password>@<host>:<port>/<database_name>
        ```

12. Amazon CloudFront Setup
    - Create access credentials
      - Go to [Amazon CloudFront](https://aws.amazon.com/cloudfront/)
    - Set Environment Variables for Amazon CloudFront  
        Add the following to the .env file
        ```env
        AWS_ACCESS_KEY_ID=your_aws_access_key_id
        AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
        AWS_STORAGE_BUCKET_NAME=your_aws_storage_bucket_name
        AWS_S3_REGION_NAME=your_aws_s3_region_name
        AWS_CLOUDFRONT_KEY_ID=your_aws_cloudfront_key_id
        AWS_CLOUDFRONT_KEY=your_aws_cloudfront_key
        AWS_S3_CUSTOM_DOMAIN=your_aws_s3_custom_domain
        ```

13. Run migrations
    ```bash
    python manage.py migrate
    ```

14. Load demo admin data
    ```bash
    python manage.py loaddata data/demo-admin.json
    ```

15. Run tests
    ```bash
    python manage.py test
    ```

16. Run server
    ```bash
    python manage.py runserver
    ```