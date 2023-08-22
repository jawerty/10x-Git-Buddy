import argparse
from git_buddy import GitBuddy

parser = argparse.ArgumentParser(
                    prog='10x-git-buddy',
                    description='This is 10x-git-buddy cli. Use this to generate PRs for your desired GitHub repository',
                    epilog='help')

parser.add_argument('repository')           
parser.add_argument('-l', '--bug-label')
parser.add_argument('-i', '--issue-count')
parser.add_argument('-f', '--find-bug')
parser.add_argument('-a', '--auto') # will automatically clone the repo, create a new branch with the file changes and generate a PR description

args = parser.parse_args()
print(args)

buddy = GitBuddy(args.repository, n=args.issue_count, bug_label=args.bug_label)
buddy.issue_fixer()