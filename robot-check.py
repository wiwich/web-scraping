### import libraries
import urllib.robotparser  # parsing robots.txt files
import urllib.request  # opening and reading URLs

###
### Function: is_allowed_to_scrape
### Parameters
### - base_url: the target website
### - user_agent: default is '*' which means any user agent
### - url_path: path you want to check (default is '/')
### Functions
### 1. Initializes a RobotFileParser object
### 2. Read the robots.txt file from the website
### 3. Uses the can_fetch method to check if te user agent is allowed to access
### 4. Returns True if access is allowed, otherwise False
def is_allowed_to_scrape(base_url,user_agent,url_path):
    # Construct the full URL to the robots.txt file
    robots_url = urllib.parse.urljoin(base_url,'/robots.txt')

    # Initialize the robots parser
    rp = urllib.robotparser.RobotFileParser()

    try:
        # Read the robots.txt file
        rp.set_url(robots_url)
        rp.read()

        # Check if the user agent is allowed to access the URL path
        is_allowed = rp.can_fetch(user_agent, urllib.parse.urljoin(base_url, url_path))
        
        return is_allowed
    except Exception as e:
        print(f"Error reading robots.txt: {e}")
        return False

### Example usage
if __name__ == "main":
  base_url = 'https://<URL_PATH>.com'
  user_agent = '*'
  url_path = '/'

  if is_allowed_to_scrape(base_url,user_agent,url_path):
    print(f"Scraping is allowed for user agent '{user_agent}' on {base_url}{url_path}")
  else:
      print(f"Scraping is NOT allowed for user agent '{user_agent}' on {base_url}{url_path}")