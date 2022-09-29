import os
from modules.utils import show_exception_and_exit
import sys
sys.excepthook = show_exception_and_exit

from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import selenium.webdriver.chrome.service as service


OS_NAME = 'linux' if 'posix' in os.name else 'windows'
DESKTOP = {'linux': os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop'),
            'windows': os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')}

# Main class
class Browser:
    def __init__(self) -> None:
        self.chrome_path = "src\\GoogleChromePortable\\App\\Chrome-bin\\chrome.exe"
        self.chromedriver_path = "src\\GoogleChromePortable\\App\\Chrome-bin\\chromedriver.exe"
        self.start_url = "https://www.facebook.com/"

        self.options = Options()
        self.options.add_argument('--incognito')
        self.options.add_argument('--ignore-certificate-errors')
        self.options.add_argument('log-level=3')  # Supress all warnings and ERRORS

        self.serv = service.Service(self.chromedriver_path)
        self.serv.start()
        self.capabilities = {'chrome.binary': self.chrome_path}

        self.driver = webdriver.Remote(self.serv.service_url, self.capabilities, options=self.options)
        
        # Show the user agent used
        print()
        print(self.driver.execute_script("return navigator.userAgent;"))
        print()

    def go(self, url):
        self.driver.get(url)