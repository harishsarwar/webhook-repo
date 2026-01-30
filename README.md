# GitHub Webhook Event Tracker

A Flask application that receives GitHub webhook events and displays them in a web UI.

---

## Overview

This application:
- Receives webhooks from GitHub when you push code or create pull requests
- Stores events in MongoDB database
- Displays events in a web interface that updates every 15 seconds

---

## Complete Setup (First Time Only)

### Step 1: Install MongoDB

```bash
# Install MongoDB
brew tap mongodb/brew
brew install mongodb-community

# Verify installation
mongod --version
```

You should see: `db version v7.0.x`

### Step 2: Create MongoDB Data Directory

```bash
# Create directory for MongoDB to store data
mkdir -p ~/data/db
```

### Step 3: Setup Python Virtual Environment

```bash
# Navigate to webhook-repo folder
cd /Users/YOUR_USERNAME/Documents/webhook-repo

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# You should see (venv) before your terminal prompt
```

### Step 4: Install Python Dependencies

```bash
# Make sure virtual environment is activated (you should see (venv))
# Install required packages
pip install Flask==3.1.0 pymongo==4.10.1
```

You should see: `Successfully installed Flask-3.1.0 pymongo-4.10.1`

### Step 5: Install ngrok

```bash
# Install ngrok
brew install ngrok

# Verify installation
ngrok --version
```

### Step 6: Authenticate ngrok

```bash
# Sign up at https://ngrok.com (free account)
# Get your auth token from: https://dashboard.ngrok.com/get-started/your-authtoken

# Authenticate (replace YOUR_TOKEN with actual token)
ngrok config add-authtoken YOUR_TOKEN
```

You should see: `Authtoken saved`

---

## Running the Application

**Open 3 separate Terminal windows and run these commands:**

### Terminal 1: Start MongoDB

```bash
# Start MongoDB
mongod --dbpath ~/data/db
```

**Success indicator:** You should see this line at the end:
```
"msg":"Waiting for connections","attr":{"port":27017}
```

**DO NOT CLOSE THIS TERMINAL**

---

### Terminal 2: Start Flask Application

```bash
# Navigate to webhook-repo
cd /Users/YOUR_USERNAME/Documents/webhook-repo

# Activate virtual environment
source venv/bin/activate

# Start Flask app
python app.py
```

**Success indicator:** You should see:
```
* Serving Flask app 'app'
* Debug mode: on
* Running on http://0.0.0.0:5001
```

**Verify it works:** Open browser and go to http://localhost:5001

You should see: "GitHub Webhook Events" page

**DO NOT CLOSE THIS TERMINAL**

---

### Terminal 3: Start ngrok

```bash
# Start ngrok
ngrok http 5001
```

**Success indicator:** You should see:
```
Session Status                online
Forwarding                    https://xxxx-xxxx.ngrok-free.app -> http://localhost:5001
```

**COPY THE HTTPS URL** (e.g., `https://abc123.ngrok-free.app`)

**DO NOT CLOSE THIS TERMINAL**

---

## Configure GitHub Webhook (First Time Only)

1. Go to: `https://github.com/YOUR_USERNAME/action-repo`
2. Click: **Settings** (top menu)
3. Click: **Webhooks** (left sidebar)
4. Click: **Add webhook** (green button)
5. Fill in:
   - **Payload URL:** `https://your-ngrok-url/webhook` (paste your ngrok URL + /webhook)
   - **Content type:** `application/json`
   - **Which events:** Select "Let me select individual events"
   - Check: **Pushes**
   - Check: **Pull requests**
6. Click: **Add webhook**

You should see a green checkmark next to your webhook.

---

## Testing the Application

### Test 1: Push Event

**Open a new Terminal (4th terminal):**

```bash
# Navigate to action-repo
cd /Users/YOUR_USERNAME/Documents/action-repo

# Edit test file
echo "Counter: 2" > test.txt

# Commit and push
git add .
git commit -m "Test push event"
git push origin main
```

**Check Result:**
- Open browser: http://localhost:5001
- Wait 15 seconds
- You should see: "YOUR_USERNAME pushed to main on [date/time]"

---

### Test 2: Pull Request Event

**In the same terminal:**

```bash
# Create new branch
git checkout -b feature-branch

# Edit file
echo "Counter: 3" > test.txt

# Commit and push
git add .
git commit -m "Feature update"
git push origin feature-branch
```

**On GitHub website:**
1. Go to your action-repo
2. Click yellow "Compare & pull request" button
3. Click green "Create pull request" button

**Check Result:**
- Refresh: http://localhost:5001
- Wait 15 seconds
- You should see: "YOUR_USERNAME submitted a pull request from feature-branch to main on [date/time]"

---

## Stopping the Application

**In each of the 3 terminals:**

```bash
# Press: Ctrl + C
```

This will stop MongoDB, Flask, and ngrok.

---

## Restarting the Application (After First Setup)

**You only need these 3 commands (in 3 separate terminals):**

### Terminal 1:
```bash
mongod --dbpath ~/data/db
```

### Terminal 2:
```bash
cd /Users/YOUR_USERNAME/Documents/webhook-repo
source venv/bin/activate
python app.py
```

### Terminal 3:
```bash
ngrok http 5001
```

**Important:** If ngrok URL changes, update GitHub webhook:
- Settings → Webhooks → Edit → Update Payload URL

---

## Viewing MongoDB Data

```bash
# Open new terminal
mongosh

# Switch to database
use github_webhook_db

# View all events
db.events.find().pretty()

# Exit
exit
```

---

## Troubleshooting

### MongoDB won't start

```bash
# Make sure data directory exists
mkdir -p ~/data/db

# Try starting again
mongod --dbpath ~/data/db
```

### Flask won't start - Port 5001 in use

```bash
# Find what's using port 5001
lsof -i :5001

# Kill it (replace PID with actual number)
kill -9 PID

# Try starting Flask again
python app.py
```

### Virtual environment not activated

You should see `(venv)` before your terminal prompt. If not:

```bash
cd /Users/YOUR_USERNAME/Documents/webhook-repo
source venv/bin/activate
```

### ngrok URL changed

```bash
# Get new URL from Terminal 3
# Update GitHub webhook:
# Settings → Webhooks → Edit → Update Payload URL with new ngrok URL
```

---

## Quick Command Reference

**Start everything:**
```bash
# Terminal 1
mongod --dbpath ~/data/db

# Terminal 2
cd /Users/YOUR_USERNAME/Documents/webhook-repo
source venv/bin/activate
python app.py

# Terminal 3
ngrok http 5001
```

**Test push:**
```bash
cd /Users/YOUR_USERNAME/Documents/action-repo
echo "test" >> test.txt
git add .
git commit -m "test"
git push
```

**View UI:**
```
http://localhost:5001
```

**Check database:**
```bash
mongosh
use github_webhook_db
db.events.find().pretty()
exit
```

---

## Success Checklist

Application is running when:

- [ ] Terminal 1 shows: "Waiting for connections" on port 27017
- [ ] Terminal 2 shows: "Running on http://0.0.0.0:5001"
- [ ] Terminal 3 shows: ngrok forwarding URL
- [ ] Browser http://localhost:5001 shows "GitHub Webhook Events" page
- [ ] All 3 terminals remain open

Application is working when:

- [ ] Push to action-repo appears in UI within 15 seconds
- [ ] Pull request in action-repo appears in UI within 15 seconds

---

Last Updated: January 30, 2026