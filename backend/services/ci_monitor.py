import requests
import time


class CIMonitor:
    def __init__(self, github_token: str):
        self.github_token = github_token

    def wait_for_ci(self, repo_full_name: str, branch: str, timeout: int = 120):
        headers = {
            "Authorization": f"token {self.github_token}",
            "Accept": "application/vnd.github+json",
        }

        start_time = time.time()

        while time.time() - start_time < timeout:
            url = f"https://api.github.com/repos/{repo_full_name}/actions/runs"
            response = requests.get(url, headers=headers)

            if response.status_code != 200:
                return "unknown"

            data = response.json()

            for run in data.get("workflow_runs", []):
                if run["head_branch"] == branch:
                    status = run["conclusion"]
                    if status:
                        return status

            time.sleep(5)

        return "timeout"
