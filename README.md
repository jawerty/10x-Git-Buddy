# 10x-Git-Buddy
Live streamed here: https://www.youtube.com/live/NdhCfM5jW8g?feature=share

## What is it
An LLM agent that finds solvable github issues and fixes the relevant files

This entire project was live coded on August 21st 2023 and will be further fine-tuned and fixed in the following weeks. Please request any changes in the Issues or fork to make changes of your own

# How it works
10x-Git-Buddy uses [WizardCoder](https://huggingface.co/WizardLM/WizardCoder-15B-V1.0#inference) (or any open llm of your choice) to scrape github issues filtered by bug label (optional) and attempts to fix the affected files by cloning the repo and searching for the relevant "APIs" in the Github issue.

The 10x-Git-Buddy will keep fixing files until you accept a solution. Also it will attempt to fix various related APIs from the documentation. This is highly experimental and is an MVP for a more comprehensive solution that will be worked on in the upcoming weeks.

Example (running):
![Screen Shot 2023-08-22 at 4 50 27 AM](https://github.com/jawerty/10x-Git-Buddy/assets/1999719/586d41b5-bbe6-4901-b31d-80e62560f22f)

Example (response):
![Screen Shot 2023-08-22 at 4 50 02 AM](https://github.com/jawerty/10x-Git-Buddy/assets/1999719/dde6d28d-db0e-4ac7-91dc-dc9ab3af5824)

# How to use it

## Recommended
Get a copy of the [Google Colab](https://colab.research.google.com/drive/1-YXyJ3JjozzDtyKph4daHBznictxqjHi?usp=sharing) and run live

## Run from source.
First clone the repository
```
$ git clone git@github.com:jawerty/10x-git-buddy.git
$ cd 10x-git-buddy
```

pip install from the requirements txt
```
pip install -r requirements.txt
```

and run the following command to test
```
$ python main.py [repo-url] --bug-label="insert bug label here"
```


# Todo
- Add a long/short term memory (learn how to fix issues over time)
- Add an option to summarize the fixes
- Automatically make PRs with the output
- Better prompting
