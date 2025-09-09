import logging
from pythonjsonlogger import jsonlogger
import sys

from src.tickettocodeagent.processor import TaskProcessor
from src.tickettocodeagent.model.model import TaskParameter
from src.tickettocodeagent.tools.git_provider.github_adapter import GitHubAdapter

log = logging.getLogger()


def configure_logging() -> None:
    log.setLevel(logging.INFO)
    # formatter = logging.Formatter("✏️ %(levelname)s - %(module)s: %(message)s")
    formatter = jsonlogger.JsonFormatter("✏️ %(levelname)s - %(name)s: %(message)s")

    # log output to stdout for log analytics
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # log output to file
    file_handler = logging.FileHandler("system.log")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    log.handlers.clear()
    log.addHandler(console_handler)
    log.addHandler(file_handler)


def main():
    configure_logging()
    log.info("Starting ticket-to-code-agent")

    task_processor = TaskProcessor(git_provider=GitHubAdapter())

    if len(sys.argv) < 2:
        log.error("No message provided")
        return

    task_parameter = _parse_message(sys.argv[1])
    task_processor.process(task_parameter)


def _parse_message(message: str) -> TaskParameter | None:
    try:
        return TaskParameter.model_validate_json(message)
    except Exception:
        log.exception("Could not parse message %s", message)
        return None


if __name__ == "__main__":
    main()
