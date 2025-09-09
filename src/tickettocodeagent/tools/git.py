import logging

import git
from src.tickettocodeagent.config.env import env

log = logging.getLogger(__name__)


class Git:
    _access_token: str

    def __init__(self) -> None:
        self._access_token = env.GITHUB_PAT_TOKEN.get_secret_value()

    def clone(
        self, repo_url: str, into_path: str, base_commit: str | None = None
    ) -> None:
        repo_url = repo_url.replace("git://", "https://")
        if self._access_token:
            repo_url = repo_url.replace("https://", f"https://{self._access_token}@")
        if not repo_url.endswith(".git"):
            repo_url = repo_url + ".git"

        try:
            repo = git.Repo.clone_from(repo_url, into_path)
            log.info(
                "successfully cloned repository '%s' into directory '%s'",
                repo_url,
                into_path,
            )
            if base_commit:
                repo.git.checkout(base_commit)
                log.info("successfully checked out commit '%s'", base_commit)
        except Exception:
            log.exception("Error cloning repository")
            raise

    def create_and_push_branch(
        self, workspace_path: str, branch_name: str, commit_message: str
    ) -> None:
        repo = git.Repo(workspace_path)

        # create new branch
        new_branch = repo.create_head(branch_name)
        new_branch.checkout()

        # add files to staging
        repo.git.add("--all")

        # Commit created
        repo.index.commit(commit_message)

        # Push to origin
        origin = repo.remotes.origin
        origin.push(new_branch)

        log.info("Successfully created and pushed branch '%s'", branch_name)
