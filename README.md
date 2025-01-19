# AUTO-VERIFY-MAIL

A Python script to automatically verify email addresses for Roblox accounts using their API.

## Features
- Bulk email verification for multiple accounts
- Simple combo file format (email:cookie)
- Uses Roblox's official API endpoints

## Setup
1. Install the required dependency:
```bash
pip install requests
```

2. Create a `combo.txt` file in the same directory with the following format:
```
email1@example.com:cookie1
email2@example.com:cookie2
```

## Usage
Run the script using:
```bash
python main.py
```

The script will:
1. Read the combo file
2. Process each line
3. Attempt to verify the email for each account
4. Print the status code for each verification attempt

## Note
Make sure your `.ROBLOSECURITY` cookies are valid and not expired.

