import subprocess
import re

class GitBuddy:
  def __init__(self, repository, coder_llm, n=1, bug_label=None):
    self.repository = repository
    self.bug_label = bug_label
    self.issue_limit = n
    self.coder_llm = coder_llm
    self.scraper = GithubScraper()

  def repo_search(self, api):
    subprocess.run(["git", "clone", self.repository+".git"])
    folder_name = self.repository.split("/")[-1]
    output = subprocess.check_output(["grep", "-rnw", f"./{folder_name}", "-e", api])
    print(str(output))
    files_to_search = []
    for line in output.split(b'\n'):
      line = str(line)
      file_name_raw = line.split(' ')[0].strip()
      _file = file_name_raw.split(":")[0]
      remove_first_2 = _file.index("b'") == 0
      if remove_first_2:
        _file = _file[2:]
      files_to_search.append(_file)
    print("files_to_search", files_to_search)
    return files_to_search
    
  def file_fixer(self, code, api, issue_description):
    prompt = self.coder_llm.get_instruction_prompt(self.coder_llm.get_code_fixer_prompt(code, api, issue_description)) 
    output = self.coder_llm.generate(
        prompt, max_new_tokens=2048
    )[0]
    print("\n\n\n\n-----FIXER OUTPUT-----")
    print(output)
    output = output[output.index("### Response:"):]

    code_blocks = re.findall(r"```(.*?)```", output, re.DOTALL)
    code = code_blocks[-1]
    new_code = "\n".join(code.split("\n")[1:])
    return new_code

  def code_fetcher(self, files_to_search, issue_description):
    for file_path in files_to_search:
      with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        code = "\n".join(lines)
        code = code[:2048] #approximation
      print("\n\n\n\n\n\nChecking file....", file_path)
      prompt = self.coder_llm.get_instruction_prompt(self.coder_llm.get_code_relevance_prompt(code, issue_description)) 
      output = self.coder_llm.generate(
          prompt, max_new_tokens=2048
      )[0]
      
      output = output[output.index("### Response:"):]
      if "yes" in output.lower():
        return code, file_path
      
  def issue_api_finder(self, issue_link):
    issue_description = self.scraper.scrape_issue_description(issue_link)
    # print("\n\n\n\n")
    # print("-----USER DESCRIPTION-----")
    # print(issue_description)

    prompt = self.coder_llm.get_instruction_prompt(self.coder_llm.get_api_prompt(issue_description)) 
    print('\n\n\n\n')
    print("-----PROMPT------")
    print(prompt)
    output = self.coder_llm.generate(
        prompt, max_new_tokens=2048
    )[0]
    # print('\n\n\n\n')
    # print("-----OUTPUT-----")
    # print(output)
    # print("------END------")

    if "APIS:" in output:
      output = output[output.index("### Response:"):]
      apis = list(map(lambda x: x.strip(), output[output.index("APIS:")+len("APIS:"):].split(",")))
      print("apis:", apis)
      filtered_apis = list(filter(lambda x: len(x.split(" ")) == 1, apis))
      print("filtered apis:", filtered_apis)
      return filtered_apis, issue_description
    else:
      return [], issue_description

  def issue_fixer(self):
    issue_links = self.scraper.scrape_issues(self.repository, bug_label=self.bug_label)
    issue_links = issue_links[:self.issue_limit]
    print(issue_links)


    for i, issue_link in enumerate(issue_links):
      print("Finding API for", issue_link)

      apis, issue_description = self.issue_api_finder(issue_link)
      for api in apis:
        print("\n\n\n\nGETTING FILE LINKS")
        # file_links = self.scraper.scrape_api_search(self.repository, api)
        file_paths = self.repo_search(api)
        code, file_path = self.code_fetcher(file_paths, issue_description)
        # fix the first file for now
        new_code = self.file_fixer(code, api, issue_description)
        
        print("Fixed issue attempt #"+str(i+1))
        print("Issue:", issue_link)
        print("Fixed File Path:", file_path)
        print("Fixed Source Code:\n", new_code)

 