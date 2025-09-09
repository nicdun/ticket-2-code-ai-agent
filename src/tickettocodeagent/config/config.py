import yaml

from minisweagent.config import get_config_path
from minisweagent.agents.default import AgentConfig
from src.tickettocodeagent.config.env import env


import logging

log = logging.getLogger(__name__)


class CustomAgentConfig:
    def __init__(self):
        self._config_file_path: str = f"{env.SWE_AGENT_CONFIG_ROOT}"

    def get_config(self) -> dict[str, any]:
        config = yaml.safe_load(get_config_path(self._config_file_path).read_text())
        return config


custom_agent_config = CustomAgentConfig()
