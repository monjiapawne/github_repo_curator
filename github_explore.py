from dataclasses import dataclass
import textwrap
from github import Github
from github import Auth
from github.Repository import Repository
import langid

CONFIG = {
    "config" : {
        "repo_range": 20,
        "min_issues": 50,
        "github_auth": "AUTH_TOKEN_HERE",
        "query": "language:python stars:150..1500",
        
    },
    "toggles" : {
        "language": "true",
        "filters": "true",
    }
}

@dataclass
class Config:
    repo_range: int
    min_issues: int
    github_auth: str
    query: str


filters = {"ai", "transformer", "llm", "agent", "model"}


def is_english(text: str) -> bool:
    lang, _ = langid.classify(text[:40])
    return lang == "en"


def min_collab(repo: Repository, min: int = 3) -> bool:
    return repo.get_contributors().totalCount >= min


def min_issues(repo: Repository, min: int = 10) -> bool:
    return repo.open_issues_count > min


def filter_repo(repo: Repository, cfg: Config) -> bool:
    if not repo.description:
        return False
      
    if not min_collab(repo):
        return False
    
    if not min_issues(repo, cfg.min_issues):
        return False
    
    desc = set(repo.description.lower().split())
    for word in filters:
        if word in desc:
            return False

    if not is_english(repo.description):
        return False

    return True


def search(g: Github, cfg: Config) -> list[Repository]:
    repos = g.search_repositories(
        query=cfg.query,
        sort="updated"
        )
    
    i = 1
    valid_repos = []

    while len(valid_repos) < cfg.repo_range:
        repo = repos[i]
        if filter_repo(repo, cfg):
            valid_repos.append(repo)
        i += 1
    
    return valid_repos


def display(repos: list[Repository]):
    for i, repo in enumerate(repos, 1):
        print(f"{i})")
        print(f"Name: {repo.name}")
        print(f"Stars: {repo.stargazers_count}")
        print(f"Issues: {repo.open_issues_count}")
        print(f"Desc: {'\n'.join(textwrap.wrap(repo.description, 70))}")
        print(f"Url: {repo.html_url}")
        print("\033[32m", "─" * 70, "\033[0m")


def main():
    cfg = Config(**CONFIG["config"])
    auth = Auth.Token(cfg.github_auth)

    repos = search(Github(auth=auth), cfg)
    display(repos)
    

if __name__ == "__main__":
    main()
