import requests
from datetime import datetime, timedelta
import os

# --- CONFIGURATION ---
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # must be set as env var or secret
ORGS = ["ballerina-platform", "wso2", "wso2-enterprise"]  # ✅ your orgs here
DAYS = 180  # last 6 months

HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

since_date = datetime.utcnow() - timedelta(days=DAYS)
output_lines = []

def get_all_repos(org):
    repos = []
    page = 1
    while True:
        url = f"https://api.github.com/orgs/{org}/repos?per_page=100&page={page}&type=all"
        res = requests.get(url, headers=HEADERS)
        if res.status_code != 200:
            print(f"Failed to get repos for {org}: {res.status_code}")
            break
        data = res.json()
        if not data:
            break
        repos.extend([r["name"] for r in data])
        page += 1
    return repos

def get_merged_prs(org, repo):
    page = 1
    while True:
        url = f"https://api.github.com/repos/{org}/{repo}/pulls?state=closed&per_page=100&page={page}"
        res = requests.get(url, headers=HEADERS)
        if res.status_code != 200:
            print(f"Failed to fetch PRs for {org}/{repo}: {res.status_code}")
            break
        prs = res.json()
        if not prs:
            break
        for pr in prs:
            merged_at = pr.get("merged_at")
            if merged_at:
                merged_date = datetime.strptime(merged_at, "%Y-%m-%dT%H:%M:%SZ")
                if merged_date > since_date:
                    title = pr["title"].replace("\n", " ")
                    output_lines.append(f"{org}/{repo}: {title} - {pr['html_url']}")
        page += 1

def main():
    for org in ORGS:
        print(f"\n🔍 Processing org: {org}")
        repos = get_all_repos(org)
        print(f"  → {len(repos)} repositories found")
        for repo in repos:
            print(f"    • Checking {repo}")
            get_merged_prs(org, repo)

    with open("merged_prs.txt", "w") as f:
        f.write("\n".join(output_lines))

    print(f"\n✅ Done. Found {len(output_lines)} merged PRs.")
    print("📄 Output written to: merged_prs.txt")

if __name__ == "__main__":
    main()
