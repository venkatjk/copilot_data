"""
GitHub Copilot Usage Tracker — Personal Account Version
========================================================
This script fetches your personal GitHub Copilot subscription and usage data
from github.com, stores it locally as JSON, and displays a summary.

Prerequisites:
    pip install requests

Setup:
    1. Create a GitHub Personal Access Token (classic) with scope: copilot
    2. Go to: https://github.com/settings/tokens → Generate new token (classic)
    3. Set your token below (or use environment variable)

Usage:
    python github_copilot.py
"""

import requests
import json
import os
from datetime import datetime, timezone

# === CONFIGURATION ===
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN', '<<replace with gitub PAT token')

# Output directory
OUTPUT_DIR = 'copilot_data'
os.makedirs(OUTPUT_DIR, exist_ok=True)

# API Base
BASE_URL = 'https://api.github.com'
HEADERS = {
    'Authorization': f'Bearer {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github+json',
    'X-GitHub-Api-Version': '2022-11-28'
}


def check_token_and_user():
    """Verify the token works and get username."""
    print(f"\n[1] Checking token & user...")
    response = requests.get(f'{BASE_URL}/user', headers=HEADERS)

    if response.status_code == 200:
        user = response.json()
        login = user.get('login')
        print(f"    ✓ Authenticated as: {login}")
        scopes = response.headers.get('X-OAuth-Scopes', '')
        print(f"    Token scopes: {scopes}")
        return login
    else:
        print(f"    ✗ Error {response.status_code}: {response.text[:200]}")
        return None


def fetch_copilot_subscription():
    """Fetch personal Copilot subscription info."""
    url = f'{BASE_URL}/user/copilot'
    print(f"\n[2] Fetching Copilot subscription...")
    print(f"    GET {url}")

    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        data = response.json()
        print(f"    ✓ Success")
        return data
    elif response.status_code == 404:
        print(f"    ✗ 404 — Copilot may not be active, or token needs 'copilot' scope")
        return None
    else:
        print(f"    ✗ Error {response.status_code}: {response.text[:200]}")
        return None


def fetch_user_repos(login):
    """Fetch user's repos to show activity context."""
    url = f'{BASE_URL}/users/{login}/repos'
    print(f"\n[3] Fetching recent repos...")
    response = requests.get(url, headers=HEADERS, params={'sort': 'pushed', 'per_page': 5})

    if response.status_code == 200:
        repos = response.json()
        print(f"    ✓ Found {len(repos)} recent repos")
        return repos
    return []


def print_dashboard(login, subscription, repos):
    """Print a text-based dashboard."""
    print("\n")
    print("=" * 60)
    print("   GITHUB COPILOT — Personal Subscription")
    print("=" * 60)

    if subscription:
        plan = subscription.get('plan_type', 'unknown')
        seat_type = subscription.get('seat_management_setting', 'N/A')
        created = subscription.get('created_at', 'N/A')

        print(f"   User:          {login}")
        print(f"   Plan:          {plan}")
        print(f"   Seat type:     {seat_type}")
        print(f"   Created:       {created}")

        # IDE suggestions setting
        ide = subscription.get('ide_chat', None)
        cli = subscription.get('cli', None)
        if ide is not None:
            print(f"   IDE Chat:      {'enabled' if ide else 'disabled'}")
        if cli is not None:
            print(f"   CLI:           {'enabled' if cli else 'disabled'}")
    else:
        print(f"   User:          {login}")
        print(f"   Subscription:  Not found or not accessible")

    if repos:
        print(f"\n   Recent Activity (repos pushed to):")
        for repo in repos[:5]:
            name = repo.get('full_name', '')
            pushed = repo.get('pushed_at', 'N/A')[:10]
            lang = repo.get('language') or 'N/A'
            print(f"   • {name:<35} {lang:<12} (pushed {pushed})")

    print("\n" + "=" * 60)


def save_results(login, subscription, repos):
    """Save data locally."""
    today = datetime.now(timezone.utc).strftime('%Y-%m-%d')

    data = {
        'collection_date': today,
        'user': login,
        'subscription': subscription,
        'recent_repos': [{'name': r.get('full_name'), 'language': r.get('language'), 'pushed_at': r.get('pushed_at')} for r in repos]
    }

    filepath = os.path.join(OUTPUT_DIR, f'copilot_{today}.json')
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2, default=str)

    print(f"\n[4] Saved to: {filepath}")


def main():
    print("=" * 60)
    print("  GitHub Copilot Usage Tracker — Personal Account")
    print("=" * 60)

    if GITHUB_TOKEN == 'YOUR_TOKEN_HERE':
        print("\n  ⚠️  SETUP REQUIRED:")
        print("  Set your GitHub token (github.com PAT with 'copilot' scope).")
        print("")
        print("  Option 1 — Edit this file:")
        print("    GITHUB_TOKEN = 'ghp_your_token_here'")
        print("")
        print("  Option 2 — Environment variable (PowerShell):")
        print('    $env:GITHUB_TOKEN = "ghp_your_token_here"')
        print("")
        print("  Create token at: https://github.com/settings/tokens")
        print("  Required scope: copilot")
        return

    # Step 1: Verify token
    login = check_token_and_user()
    if not login:
        print("\n  ✗ Token invalid. Check your GITHUB_TOKEN value.")
        return

    # Step 2: Fetch Copilot subscription
    subscription = fetch_copilot_subscription()

    # Step 3: Fetch recent repos
    repos = fetch_user_repos(login)

    # Step 4: Save data
    save_results(login, subscription, repos)

    # Step 5: Display dashboard
    print_dashboard(login, subscription, repos)

    print(f"\n  ✓ Done!")


if __name__ == '__main__':
    main()
