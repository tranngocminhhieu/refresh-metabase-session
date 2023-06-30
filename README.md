# refresh-metabase-session
Update the Metabase session by Signing in with Google and Saving it to Rentry automatically.

## How to use
- Step 1: Create `profile` folder by running the `create_google_profile.py` and logging in Google Account manually.
- Step 2: Prepare `metabase_url.txt` and `rentry.txt`.
- Step 3: Run the `refresh_metabase_session.py`.
- Step 4 (optional): Copy this directory to your server and set a crontab. Make sure `refresh_metabase_session.py`, `metabase_url.txt`, `rentry.txt`, and `profile` folder in the same place.

## Example files
`rentry.txt`
- URL
- Code password
```text
https://rentry.co/your-url/edit
123456
```

`metabase_url.txt`
- Domain
```text
https://your-metabase-domain.com
```