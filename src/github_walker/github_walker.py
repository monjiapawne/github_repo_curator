from github import Github
from github import Auth
from github.Repository import Repository
from config import load_settings
from display import display
import langid


def is_english(text: str) -> bool:
    lang, _ = langid.classify(text[:40])
    return lang == "en"


def min_collab(repo: Repository, min: int = 3) -> bool:
    return repo.get_contributors().totalCount >= min


def min_issues(repo: Repository, min: int = 10) -> bool:
    return repo.open_issues_count > min


def filter_repo(repo: Repository, cfg, filters: set) -> bool:
    if not repo.description:
        return False
      
    if not min_collab(repo):
        return False
    
    if not min_issues(repo, cfg.min_issues):
        return False
    
    desc = set(repo.description.lower().split())
    for prefix in filters:
       if any(prefix in word for word in desc):
           return False

    if not is_english(repo.description):
        return False

    return True


def search(g: Github, cfg, filters) -> list[Repository]:
    repos = g.search_repositories(
        query=cfg.query,
        sort="updated"
        )
    
    i = 1
    valid_repos = []

    while len(valid_repos) < cfg.repo_range:
        repo = repos[i]
        if filter_repo(repo, cfg, filters):
            valid_repos.append(repo)
        i += 1
    
    return valid_repos


def main():
    settings = load_settings()
    auth = Auth.Token(settings.github_auth)
    repos = search(Github(auth=auth), settings.core, settings.excludes)
    display(repos)
    

if __name__ == "__main__":
    main()
