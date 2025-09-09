from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class EnvSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    SWE_AGENT_CONFIG_ROOT: str

    GEMINI_API_KEY: SecretStr
    LLM_API_BASE: str
    LLM_MODEL_NAME: str

    GITHUB_PAT_TOKEN: SecretStr
    GIT_BASE_PATH: str = "github.com"

    # RUN_INSIDE_DOCKER_LOCALLY: bool = False

    # this is needed by the sweagent to make calls to different models from openai correctly
    # LITELLM_DROP_PARAMS: bool = True


env = EnvSettings()
