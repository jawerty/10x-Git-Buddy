# 10x-Git-Buddy
Live streamed here: https://www.youtube.com/live/NdhCfM5jW8g?feature=share

## What is it
An LLM agent that finds solvable github issues and fixes the relevant files

This entire project was live coded on August 21st 2023 and will be further fine-tuned and fixed in the following weeks. Please request any changes in the Issues or fork to make changes of your own

# How it works
10x-Git-Buddy uses [WizardCoder](https://huggingface.co/WizardLM/WizardCoder-15B-V1.0#inference) (or any open llm of your choice) to scrape github issues filtered by bug label (optional) and attempts to fix the affected files by cloning the repo and searching for the relevant "APIs" in the Github issue.

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
