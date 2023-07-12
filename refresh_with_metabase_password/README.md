# Refresh Metabase session with password
These scripts will help you update the Metabase session by Signing in with Metabase password and Saving it to Rentry automatically.

![Refresh the Metabase session](../images/sign-in-with-password.png)

## Usage
**Step 1: Prepare `metabase.txt` and `rentry.txt`.**

Read the example files.

**Step 2: Refresh the Metabase session.**

Run the `refresh_metabase_session` script to refresh Metabase session automatically. Place the script on your server and set a crontab to schedule for the script.

## Example files
`rentry.txt`

URL id and Edit code.
```text
vk47a3
123456
```

`metabase.txt`

Metabase login with password URL, username, and password.
```text
https://your-metabase-domain.com
username
password
```

*Thank for your reading!*