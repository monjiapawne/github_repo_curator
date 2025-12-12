import textwrap
from github.Repository import Repository

def display(repos: list[Repository]):
    for i, repo in enumerate(repos, 1):
        print(f"{i})")
        print(f"Name: {repo.name}")
        print(f"Stars: {repo.stargazers_count}")
        print(f"Issues: {repo.open_issues_count}")
        print(f"Desc: {'\n'.join(textwrap.wrap(repo.description, 70))}")
        print(f"Url: {repo.html_url}")
        print("\033[32m", "─" * 70, "\033[0m")