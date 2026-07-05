# GitHub Copilot Usage Tracker — Personal Account

A Python script that fetches your personal GitHub Copilot subscription status and recent repository activity from github.com, then displays a dashboard summary and saves the data locally as JSON.

## Features

- Authenticates with your GitHub Personal Access Token
- Fetches Copilot subscription details (plan type, seat management, IDE/CLI settings)
- Retrieves your 5 most recently pushed repositories
- Displays a text-based dashboard in the terminal
- Saves collected data to `copilot_data/` as dated JSON files

## Prerequisites

- Python 3.8+
- `requests` library

```bash
pip install requests
```

## Setup

1. Create a GitHub Personal Access Token (classic) at:
   https://github.com/settings/tokens

2. Select the `copilot` scope (required to access subscription info)

3. Set your token using one of these methods:

   **Option A — Environment variable (recommended):**

   PowerShell:
   ```powershell
   $env:GITHUB_TOKEN = "ghp_your_token_here"
   ```

   Bash:
   ```bash
   export GITHUB_TOKEN=ghp_your_token_here
   ```

   **Option B — Edit the script directly:**

   Update the `GITHUB_TOKEN` variable in `github_copilot.py`.

## Usage

```bash
python github_copilot.py
```

## Output

The script produces:

- A terminal dashboard showing subscription info and recent repo activity
- A JSON file saved to `copilot_data/copilot_<date>.json`

Example output:

```
============================================================
   GITHUB COPILOT — Personal Subscription
============================================================
   User:          your-username
   Plan:          individual
   Seat type:     personal
   Created:       2024-01-15T10:30:00Z

   Recent Activity (repos pushed to):
   • your-username/project-a              Python       (pushed 2025-07-01)
   • your-username/project-b              TypeScript   (pushed 2025-06-28)
============================================================
```

## Notes

- If the Copilot subscription endpoint returns 404, it means either:
  - Your account doesn't have an active personal Copilot subscription
  - Your Copilot access is managed through an organization/enterprise (not visible via personal API)
  - Your token is missing the `copilot` scope
- The script targets `api.github.com`. For GitHub Enterprise Server, the base URL and auth headers would need adjustment.
