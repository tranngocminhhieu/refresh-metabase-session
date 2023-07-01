# Refresh Metabase session
Update the Metabase session by Signing in with Google and Saving it to Rentry automatically.

## How to use
- Step 1: Create `profile` folder by running the `create_google_profile` script and logging in Google Account manually.
- Step 2: Prepare `metabase_url.txt` and `rentry.txt`.
- Step 3: Run the `refresh_metabase_session` script to refresh the Metabase session.
- Step 4 (optional): Set a crontab to run the script automatically.

*Note: The `create_google_profile` is not working for personal Gmail, but working with a Google Workspace account.*

## Example files
`rentry.txt`: URL and Edit code.
```text
https://rentry.co/your-url/edit
123456
```

`metabase_url.txt`: Metabase domain.
```text
https://your-metabase-domain.com
```