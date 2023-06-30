# Refresh Metabase session
Update the Metabase session by Signing in with Google and Saving it to Rentry automatically.

## How to use
- Step 1: Create `profile` folder by running the `create_google_profile` script and logging in Google Account manually.
- Step 2: Prepare `metabase_url.txt` and `rentry.txt`.
- Step 3: Run the `refresh_metabase_session.py` to refresh the Metabase session.

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