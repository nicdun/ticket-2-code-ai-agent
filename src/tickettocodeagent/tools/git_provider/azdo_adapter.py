from src.tickettocodeagent.tools.git_provider.git_provider_port import GitProviderPort


class AzdoAdapter(GitProviderPort):
    def __init__(self):
        pass

    def create_pull_request(
        self,
        *,
        owner: str,
        repo: str,
        title: str,
        head: str,
        base: str,
        body: str | None = None,
        draft: bool = False,
        maintainer_can_modify: bool | None = None,
    ) -> dict:
        pass
