from pydantic import BaseModel


class TaskParameter(BaseModel):
    owner: str
    repo: str
    git_provider: str
    ticket_id: str
    body: str
    repo_url: str
    skip_pull_request: bool = False
