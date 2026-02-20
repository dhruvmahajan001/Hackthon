import os
import shutil
import stat
from git import Repo


BASE_CLONE_DIR = os.path.abspath("cloned_repos")


def _handle_remove_readonly(func, path, exc_info):
    """
    Fix Windows readonly file deletion issue (.git objects)
    """
    os.chmod(path, stat.S_IWRITE)
    func(path)


class RepoService:
    def __init__(self) -> None:
        os.makedirs(BASE_CLONE_DIR, exist_ok=True)

    def clone_repo(self, repo_url: str) -> str:
        repo_name = repo_url.rstrip("/").split("/")[-1].replace(".git", "")
        clone_path = os.path.join(BASE_CLONE_DIR, repo_name)

        # If already exists, delete safely (Windows compatible)
        if os.path.exists(clone_path):
            shutil.rmtree(clone_path, onerror=_handle_remove_readonly)

        Repo.clone_from(repo_url, clone_path)

        return clone_path
