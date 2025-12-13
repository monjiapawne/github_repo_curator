import textwrap
from github.Repository import Repository
import markdown

def display_cli(repos: list[Repository]):
    for i, repo in enumerate(repos, 1):
        print(f"{i})")
        print(f"Name: {repo.name}")
        print(f"Stars: {repo.stargazers_count}")
        print(f"Issues: {repo.open_issues_count}")
        print(f"Desc: {'\n'.join(textwrap.wrap(repo.description, 70))}")
        print(f"Url: {repo.html_url}")
        print("\033[32m", "─" * 70, "\033[0m")


def display(repos: list[Repository]):
    lines = ["# Github Curator\n\n"]

    for repo in repos:
        lines.append(f"## {repo.name}\n\n")
        lines.append(f"> {repo.description}  \n\n")
        lines.append(f"Stars: {repo.stargazers_count}  \n")
        lines.append(f"Issues: {repo.open_issues}  \n")
        lines.append(f"{repo.html_url}  \n\n")

    text = "".join(lines)

    with open("README.md", 'w') as f:
        f.write(text)