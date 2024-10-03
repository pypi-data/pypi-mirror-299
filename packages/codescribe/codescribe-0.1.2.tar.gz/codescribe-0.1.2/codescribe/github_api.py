import requests
import base64
from typing import Dict, List, Tuple


class GithubAPI:
    def __init__(self, access_token: str = ""):
        self.access_token = access_token
        self.base_url = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github+json",
        }
        if access_token:
            self.headers["Authorization"] = f"token {access_token}"

    def parse_repo_url(self, url: str) -> Tuple[str, str, str, str]:
        url = url.rstrip("/")
        parts = url.split("/")

        owner, repo = parts[3], parts[4]
        ref = parts[6] if len(parts) > 6 and parts[5] == "tree" else "main"
        path = "/".join(parts[7:]) if len(parts) > 7 else ""

        return owner, repo, ref, path

    def fetch_repo_sha(self, owner: str, repo: str, ref: str, path: str) -> str:
        url = f"{self.base_url}/repos/{owner}/{repo}/contents/{path}"
        params = {"ref": ref} if ref else {}
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        content = response.json()

        if isinstance(content, list):
            # this is a directory so we need to get the commit SHA
            url = f"{self.base_url}/repos/{owner}/{repo}/commits/{ref}"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()["sha"]
        else:
            return content["sha"]

    def fetch_repo_tree(self, owner: str, repo: str, sha: str) -> List[Dict]:
        url = f"{self.base_url}/repos/{owner}/{repo}/git/trees/{sha}"
        params = {"recursive": "1"}
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()["tree"]

    def fetch_file_contents(self, url: str) -> str:
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        content = response.json()

        if content.get("encoding") == "base64":
            return base64.b64decode(content["content"]).decode("utf-8")
        else:
            return content.get("content", "")

    def get_repo_contents(self, repo_url: str) -> List[Dict]:
        owner, repo, ref, path = self.parse_repo_url(repo_url)
        sha = self.fetch_repo_sha(owner, repo, ref, path)
        tree = self.fetch_repo_tree(owner, repo, sha)
        contents = []
        for item in tree:
            if item["type"] == "blob":
                content = self.fetch_file_contents(item["url"])
                contents.append(
                    {
                        "path": item["path"],
                        "content": content,
                    }
                )
        return contents
