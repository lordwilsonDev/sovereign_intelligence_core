from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class GitHubIssueRef:
    number: int
    title: str
    url: str
    state: str = "open"


@dataclass(frozen=True)
class GitHubPRRef:
    number: int
    title: str
    url: str
    state: str = "open"
    merged: bool = False


def fetch_github_issues(owner: str, repo: str, *, limit: int = 20) -> List[GitHubIssueRef]:
    import urllib.request
    import json

    url = f"https://api.github.com/repos/{owner}/{repo}/issues?per_page={limit}&state=all&sort=updated&direction=desc"
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json", "User-Agent": "msb-v2"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read())
    items: List[GitHubIssueRef] = []
    for item in data:
        if "pull_request" in item:
            continue
        items.append(GitHubIssueRef(number=item["number"], title=item["title"], url=item["html_url"], state=item["state"]))
    return items


def fetch_github_prs(owner: str, repo: str, *, limit: int = 20) -> List[GitHubPRRef]:
    import urllib.request
    import json

    url = f"https://api.github.com/repos/{owner}/{repo}/pulls?per_page={limit}&state=all&sort=updated&direction=desc"
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json", "User-Agent": "msb-v2"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read())
    return [
        GitHubPRRef(number=item["number"], title=item["title"], url=item["html_url"], state=item["state"], merged=bool(item.get("merged", False)))
        for item in data
    ]
