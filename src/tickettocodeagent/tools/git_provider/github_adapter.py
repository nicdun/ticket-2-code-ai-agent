import logging
from typing import Any

import requests

from src.tickettocodeagent.config.env import env
from src.tickettocodeagent.tools.git_provider.git_provider_port import GitProviderPort

log = logging.getLogger(__name__)


class GitHubAdapter(GitProviderPort):
    _access_token: str
    _api_base: str

    def __init__(self) -> None:
        self._access_token = env.GITHUB_PAT_TOKEN.get_secret_value()
        # Support enterprise by allowing base path override via env.GIT_BASE_PATH
        # env.GIT_BASE_PATH defaults to "github.com"; API base is derived accordingly.
        base_host = env.GIT_BASE_PATH
        if base_host == "github.com":
            self._api_base = "https://api.github.com"
        else:
            # GitHub Enterprise typically exposes REST at /api/v3
            self._api_base = f"https://{base_host}/api/v3"

    def _headers(self) -> dict[str, str]:
        return {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {self._access_token}",
            "X-GitHub-Api-Version": "2022-11-28",
        }

    def _create_pull_request(
        self,
        owner: str,
        repo: str,
        title: str,
        head: str,
        base: str = "main",
        body: str | None = None,
        draft: bool = False,
        maintainer_can_modify: bool | None = None,
    ) -> dict[str, Any]:
        """
        Create a pull request.

        Parameters
        - owner: repository owner/organization
        - repo: repository name
        - title: pull request title
        - head: name of the branch where your changes are implemented; can be "user:branch"
        - base: name of the branch you want the changes pulled into
        - body: optional PR description
        - draft: create as draft PR
        - maintainer_can_modify: if provided, sets whether maintainers can modify the PR

        Returns JSON response from GitHub API.
        Raises for HTTP errors with detailed logging.
        """

        url = f"{self._api_base}/repos/{owner}/{repo}/pulls"
        payload: dict[str, Any] = {
            "title": title,
            "head": head,
            "base": base,
            "draft": draft,
        }
        if body is not None:
            payload["body"] = body
        if maintainer_can_modify is not None:
            payload["maintainer_can_modify"] = maintainer_can_modify

        try:
            response = requests.post(
                url, json=payload, headers=self._headers(), timeout=30
            )
            if response.status_code >= 400:
                log.error(
                    "GitHub create PR failed: %s %s — %s",
                    response.status_code,
                    response.reason,
                    response.text,
                )
            response.raise_for_status()
            pr = response.json()
            log.info("Created PR #%s: %s", pr.get("number"), pr.get("html_url"))
            return pr
        except requests.RequestException:
            log.exception("Error while creating pull request")
            raise
