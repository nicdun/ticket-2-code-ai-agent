from typing import NamedTuple
import logging
from abc import ABC, abstractmethod

from src.tickettocodeagent.model.model import TaskParameter

log = logging.getLogger(__name__)


def _is_promising_patch(info: dict) -> bool:
    """[From swe-agent(sweagent/run/common.py)]
    Do we actually believe that the patch will solve the issue?
    Or are we just submitting the last patch we generated before hitting an error?
    """
    # The exit status can also be `submitted (exit_cost)` etc.
    return info.get("exit_status") == "submitted" and info.get("submission") is not None


class TrajectoryData(NamedTuple):
    action: str
    execution_time: str
    extra_info: str
    observation: str
    response: str
    state: str
    thought: str


ACCEPT_THRESHOLD = 0.5


class PullRequestMessageFormatter:
    def format_message(self, info: dict, trajectories: list) -> str:
        if info.get("review"):
            accept_score = float(info["review"].get("accept"))
            review_output = info["review"].get("outputs")
            accept_msg = (
                "ACCEPTED:"
                if (accept_score and accept_score > ACCEPT_THRESHOLD)
                else "DECLINED:"
            )
        else:
            accept_score = "[Not reviewed]"
            review_output = "[Not reviewed]"
            accept_msg = "[Not reviewed]"

        return (
            f"""{accept_msg}\n"""
            f"""### review-accept-score: {accept_score}\n"""
            f"""### reason:\n"""
            f"""    {review_output}\n"""
            f"""<details>\n"""
            f"""<summary>[SWE-RUN]</summary>\n"""
            f"""## Trajectories:\n"""
            f"""{self._format_trajectories(trajectories)}\n"""
            f"""</details>"""
            f"""\n"""
        )

    def _format_trajectories(self, trajectory: list) -> str:
        output = []

        for index, item in enumerate(trajectory):
            output.append(
                self._format_trajectory(
                    index=index,
                    trajectory_data=TrajectoryData(
                        action=str(item.get("action", "N/A")),
                        execution_time=str(item.get("execution_time", "N/A")),
                        extra_info=str(item.get("extra_info", "N/A")),
                        observation=str(item.get("observation", "N/A")),
                        response=item.get("response", "N/A"),
                        state=str(item.get("state", "N/A")),
                        thought=str(item.get("thought", "N/A")),
                    ),
                ),
            )

        return "\n".join(output)

    def _format_trajectory(
        self,
        index: int,
        trajectory_data: TrajectoryData,
    ) -> str:
        return (
            f"""<details>\n"""
            f"""<summary>\n"""
            f"""[Action {index}]\n"""
            f"""{trajectory_data.action}\n"""
            f"""</summary>\n"""
            f"""- Action\n{trajectory_data.action}\n"""
            f"""- Execution Time\n{trajectory_data.execution_time}\n"""
            f"""- Extra Info\n{trajectory_data.extra_info}\n"""
            f"""- Observation\n{trajectory_data.observation}\n"""
            f"""<details>\n"""
            f"""<summary>\n"""
            f"""[Query]\n"""
            f"""</summary>\n"""
            f"""</details>\n"""
            f"""- Response\n{trajectory_data.response}\n"""
            f"""- State\n{trajectory_data.state}\n"""
            f"""- Thought\n{trajectory_data.thought}\n"""
            f"""</details>\n"""
        )


class GitProviderPort(ABC):
    """
    A GitProviderPort is responsible for handling a specific git provider. Each git provider has its own GitProviderPort.
    """

    def create_pull_request(
        self,
        task: TaskParameter,
        # info: dict,
        # trajectories: list[dict],
        patch_branch_name: str,
    ) -> None:
        # implement this
        # if not _is_promising_patch(info=info):
        #     log.info("patch is not promissing... swe-agent definition")
        #     self._comments_on_ticket_github(
        #         task,
        #         f"Patch was rejected (_is_promising_patch returned False) reason\nexit_status:{info.get('exit_status')}",
        #     )
        #     return

        pr_message_body = (
            "PR message body"  # self._format_pull_request_message(info, trajectories)
        )
        self._create_pull_request(
            owner=task.owner,
            repo=task.repo,
            title="just a test",
            head=f"{task.owner}:{patch_branch_name}",
            body=pr_message_body,
        )

    @abstractmethod
    def _create_pull_request(
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
        """
        Defines for which git provider this GitProviderPort is responsible.
        :return: a string for the name of the message type.
        """
