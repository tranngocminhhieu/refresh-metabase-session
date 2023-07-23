# Refresh Metabase session with Gooogle profile
These scripts will help you update the Metabase session by Signing in with Google and Saving it to Rentry automatically.

![Refresh the Metabase session](../images/thumb.png)

## Usage
**Step 1: Create `profile` folder.**

Run the `create_google_profile` script and sign in your Google Account manually in the first time.

*Note: The script is not working for personal Gmail, but working with a Google Workspace account.*

**Step 2: Prepare `metabase.txt` and `rentry.txt`.**

Read the example files.

**Step 3: Refresh the Metabase session.**

Run the `refresh_metabase_session` script to refresh Metabase session automatically. Place the script on your server and set a crontab to schedule for the script.

## Example files
`rentry.txt`

URL id and Edit code.
```text
vk47a3
123456
```

`metabase.txt`

Metabase URL
```text
https://your-metabase-domain.com
```

*Thank for your reading!*