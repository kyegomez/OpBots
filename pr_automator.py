import logging
from github import Github
import os
from dotenv import load_dotenv

load_dotenv()


github_api_fetch = os.environ.get("GITHUB_API_TOKEN")

class PullRequestAutomator:
    def __init__(self, token):
        self.github = Github(token)
        self.excluded_repos = []

    def exclude_repos(self, repo_names):
        self.excluded_repos.extend(repo_names)

    def accept_pull_requests(self, author):
        results = []
        for repo in self.github.get_user().get_repos():
            if repo.name not in self.excluded_repos:
                pulls = repo.get_pulls(state='open', sort='created', base='master')
                for pr in pulls:
                    if pr.user.login == author:
                        try:
                            pr.merge()
                            results.append(f"Merged pull request {pr.number} from {repo.name}")
                        except Exception as e:
                            results.append(f"Failed to merge pull request {pr.number} from {repo.name}: {str(e)}")
        return results

automator = PullRequestAutomator(token=github_api_fetch)
automator.exclude_repos(["swarms", "zeta"])
out = automator.accept_pull_requests('dependabot')
print(out)