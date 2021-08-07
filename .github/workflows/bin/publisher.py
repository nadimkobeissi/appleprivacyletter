#!/usr/bin/env python3
import os
import json
import requests
import subprocess


def fetch_unhandled_issues():
    r = requests.get(
        f"https://api.github.com/repos/{os.environ['GITHUB_REPOSITORY']}/issues?labels=signature-approved&state=open",
        headers={"Authorization": f'token {os.environ["GITHUB_TOKEN"]}'},
    )
    return r.json()


def main():
    issues = fetch_unhandled_issues()
    env = os.environ.copy()
    issues_to_close = []
    for issue in issues:
        env["ISSUE_AUTHOR_URL"] = issue["user"]["html_url"]
        env["ISSUE_BODY"] = issue["body"] if issue["body"] else ""
        subprocess.run(
            ["python3", ".github/workflows/bin/sign_handler.py", "--commit-sign"],
            env=env,
        )
        issues_to_close.append(issue["number"])

    for issue in issues_to_close:
        print(f"closes #{issue}", end=", ")


if __name__ == "__main__":
    main()