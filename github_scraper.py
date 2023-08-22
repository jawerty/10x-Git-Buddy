import urllib.parse
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

class GithubScraper:
  def __init__(self, user_credentials=None):
    driver_path = '/usr/bin/chromedriver'
    chrome_options = Options()

    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--remote-debugging-port=9222")


    service = Service(executable_path=driver_path)

    self.driver = webdriver.Chrome(service=service, options=chrome_options)
    self.logged_in = False
    self.user_credentials = user_credentials
  
  # user_credentials=dict({ username, password })
  def login(self):
    self.driver.get("https://github.com/login")

    user_input = self.driver.find_element(By.CSS_SELECTOR, 'input[name="login"]')
    password_input = self.driver.find_element(By.CSS_SELECTOR, 'input[name="password"]')
    
    user_input.send_keys(self.user_credentials["username"])
    password_input.send_keys(self.user_credentials["password"])

    submit_button = self.driver.find_element(By.CSS_SELECTOR, '[type="submit"]')
    submit_button.click()
    # time.sleep(2)
    print(self.driver.page_source)
    self.logged_in = True

  def scrape_issues(self, repo, bug_label=None):
    ends_with_slash = repo[-1] == "/"
    slash = "" if ends_with_slash else "/"
    if bug_label:
      url = f"{repo}{slash}labels/{bug_label}"
    else:
      url = f"{repo}{slash}issues"

    print("Scraping url for issues:", url)
    
    self.driver.get(url);
    links = self.driver.find_elements(By.CSS_SELECTOR, '[aria-label=\"Issues\"] .Link--primary')
    issue_links = list(map(lambda x: x.get_attribute("href"), links))
    return list(filter(lambda x: "/issues" in x, issue_links))

  def scrape_issue_description(self, issue_link):
    self.driver.get(issue_link);
    description = self.driver.find_element(By.CSS_SELECTOR, '.comment-body')
    return description.text

  def scrape_api_search(self, repository, api):
    if self.logged_in == False:
      print("\n\n\n\nLogging in...\n\n\n\n")
      self.login()
    
    # structure of search = `repo:user/repo_name {search_query}`
    search_query = f"repo:{'/'.join(repository.split('/')[-2:])} {api}" # last two things
    
    search_url = f"https://github.com/search?q={search_query}&type=code"
    print("\nSearching....", search_url)
    self.driver.get(search_url)
    print(self.driver.page_source)
    links = self.driver.find_elements(By.CSS_SELECTOR, '.search-title a')
    print("links", links)
    return list(map(lambda x: x.get_attribute("href"), links))
