# webhook-repo

This is the Flask application that receives GitHub webhooks and displays events in UI.

## Files in this folder:
- **app.py** - Main Flask application (webhook receiver + API)
- **index.html** - UI page that shows events
- **requirements.txt** - Python packages needed
- **README.md** - This file

## What it does:
1. Receives webhook from GitHub when you push or create pull request
2. Stores event data in MongoDB
3. Shows events on a webpage (updates every 15 seconds)

## MongoDB Schema:
```
Database: github_webhook_db
Collection: events

Document structure:
{
    "author": "string",
    "action": "push" or "pull_request",
    "from_branch": "string" or null,
    "to_branch": "string",
    "timestamp": datetime
}
```

## Event Display Format:
- **Push**: "{author} pushed to {to_branch} on {timestamp}"
- **Pull Request**: "{author} submitted a pull request from {from_branch} to {to_branch} on {timestamp}"