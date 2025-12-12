import yaml
from dataclasses import dataclass
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
CONFIG_ROOT_PATH = BASE_DIR / "configs"
CONFIG_FILE = CONFIG_ROOT_PATH / "config.yaml"

@dataclass
class CoreConfig:
    repo_range: int
    min_issues: int
    query: str

@dataclass
class Toggles:
    language: bool
    filters: bool

@dataclass
class Settings:
    core: CoreConfig
    toggles: Toggles
    github_auth: str
    excludes: set

    
def load_settings(path: Path = CONFIG_FILE) -> Settings:
    with open(path, "r") as f:
        data = yaml.safe_load(f)

    return Settings(
        core=CoreConfig(**data["config"]),
        toggles=Toggles(**data["toggles"]),
        github_auth=data["github_auth"]["key"],
        excludes=set(data["excludes"]),
    )
