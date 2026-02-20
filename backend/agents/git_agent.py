import re
from git import Repo


class GitAgent:
    def __init__(self, repo_path: str):
        self.repo_path = repo_path
        self.repo = Repo(repo_path)


    def generate_branch_name(self, team_name: str, leader_name: str) -> str:
        team = team_name.replace(" ", "").upper()
        leader = leader_name.replace(" ", "").upper()
        return f"{team}_{leader}_AI_Fix"



    def create_and_checkout_branch(self, branch_name: str) -> None:
        if branch_name in [b.name for b in self.repo.branches]:
            self.repo.git.checkout(branch_name)
        else:
            self.repo.git.checkout("-b", branch_name)

    def commit_changes(self, message: str) -> None:
        self.repo.git.add(A=True)

        if not self.repo.is_dirty(untracked_files=True):
            return

        commit_message = f"[AI-AGENT] {message}"
        self.repo.index.commit(commit_message)



    def push_branch(self, branch_name: str) -> None:
     
        if branch_name.lower() == "main":
            raise RuntimeError("Pushing to main branch is not allowed.")

        origin = self.repo.remote(name="origin")
        origin.push(branch_name)
