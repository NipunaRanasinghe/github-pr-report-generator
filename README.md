# GitHub Merged PR Exporter

A simple tool to export merged pull requests across multiple GitHub organizations within a given time frame. Outputs PR title and URL to a plain text file.

## 🔧 Configuration

Edit the `scripts/export_merged_prs.py` file and update the following:

- `ORGS = [...]` → Add the list of GitHub organizations
- `DAYS = 180` → Set time window (e.g., last 180 days)

## 🚀 Usage

### Run locally

```bash
export GITHUB_TOKEN=ghp_...
python scripts/export_merged_prs.py
