from distutils.command.config import config
import os
import re
from time import sleep
from random import choice
import requests
from time import sleep
from random import choice
from numpy import arange
from tqdm import tqdm
from . import config
from modules.utils import normaliza
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup


class FacebookUser:
    def __init__(self, id: str, name: str, profile_url: str, image_url: str):
        self.id = id
        self.name = name
        self.profile_url = profile_url
        self.image_url = image_url


class Facebook:
    base_url = 'https://www.facebook.com'
    
    def __init__(self, driver):
        self.driver = driver
        sleep(2)
        self.target_id = input('\nEnter target\'s "profile name" or "ID": ')
        self.driver.get(f'{self.base_url}/{self.target_id}')
        self.target_name = self._get_target_profile_name()

    # TODO create test for login
    def login(self):
        print('\nAuthenticating...')
        self.driver.get(self.base_url)
        sleep(1)
        
    def _get_target_id(self):
        sleep(2)
        os.system('cls')
        config.FRIENDS_URL = f'{self.base_url}/{config.TARGET_ID}/friends'
        return config.TARGET_ID

    # Get the target profile name from Friends page
    def _get_target_profile_name(self):
        try:
            target_name = self.driver.find_element(By.XPATH, '//h1').text
            return normaliza(target_name)
        except:
            print("Error: can't find profile name.")
            return ''


#TODO change target name to Facebook class
class FriendsPage(Facebook):
    def __init__(self, driver, target_id, target_name):
        self.driver = driver
        self.target_id = target_id
        self.url = f"{self.base_url}/{target_id}/friends"
        self.target_name = target_name
        self.results = []
        self.friends_box = ''
        self.friends_box_html = ''
        self.num_friends = 0
    
    # Set a random interval
    def fsleep(self):
        sleep(choice(arange(0.5, 2.5, 0.1)))

    # Go to target's friends page
    def navigate(self):
        print(f'\nFetching target\'s friends page...')
        sleep(3)
        self.driver.get(self.url)

    # Get the number of target's friends and if the profile is blocked
    def _get_num_of_friends_and_status(self):
        number_of_friends_tag = self.driver.find_element(By.XPATH, config.NUM_OF_FRIENDS)
        # number_of_friends_text = number_of_friends_tag.text.replace(',', '.')
        # self.num_friends = int(re.sub(r"(\samigos.*|\sfriends.*)", "", number_of_friends_text)) - 1  # Facebook always show one friend more
        if "amigos em comum" in number_of_friends_tag.text or "friends in common" in number_of_friends_tag.text:
            self.status = 'total or partial blocked'
            print(f"'Warning: Friends of - {self.target_id} - {self.target_name} - may not be available for you!'")
        else:
            self.status = 'unblocked'

    # Expands and render all friends page
    def _show_friends(self):
        try:
            # self.driver.get(f"{self.url}")
            os.system('cls')
            sleep(2)
            os.system('cls')
            print('\nRendering results page. Please wait...')
            self._get_num_of_friends_and_status()
            # friends_boxes = self._get_friends_boxes()
            while True:
                self.fsleep()
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                # Try to fetch the last friend box
                try:
                    self.driver.find_element(By.XPATH, config.FRIENDS_BOX_FOLLOWING_SIBLING)
                    self.fsleep()
                    self.friends_box = self.driver.find_element(By.XPATH, config.FRIENDS_BOX)
                    self.friends_box_html = self.friends_box.get_attribute('innerHTML')
                    break
                except:
                    pass
        except:
            print(f"Can't render friends page :(")

    # Parse friends data from an html string
    def parse_friends(self, box_string) -> list:
        html = BeautifulSoup(box_string, 'html.parser')
        results = []

        def get_id(link_id):
            if 'id=' in link_id:
                id = link_id.replace('https://www.facebook.com/profile.php?id=', '')
            else:
                id = link_id.replace('https://www.facebook.com/', '')
            return id
        
        for content in html.contents:
            try:
                friend_id = get_id(content.a['href'])
                friend_name = content.contents[1].span.text
                friend_profile = content.a['href']
                friend_image_url = content.img['src']
                new_friend = FacebookUser(friend_id, friend_name, friend_profile, friend_image_url)
                results.append(new_friend)
            except:
                pass
        return results

    # Get all friends data
    def get_all_data(self):
        self.fsleep()
        self._show_friends()
        print('\nExtracting data...')

        # Parse all results into an iterable
        self.results = self.parse_friends(self.friends_box_html)
        # return [[friend.id, friend.name, friend.profile_url, friend.image_url] for friend in self.results]
        return self.results

    # Downloads friends images using self.results links
    def download_friends_images(self):
        images_folder = config.IMAGES_FOLDER
        # Create images folder
        os.makedirs(images_folder, exist_ok=True)
        # if not os.path.exists(images_folder):
        #     os.makedirs(images_folder)
        # friends_boxes = self._get_friends_boxes()
        for friend in tqdm(self.results):
            try:
                res = requests.get(friend.image_url)
                with open(os.path.join(images_folder, '{}_{}.jpg'.format(friend.name.replace(' ', '_'),
                                                                        friend.id)),
                        mode='wb') as imageFile:
                    for chunk in res.iter_content(100000):
                        imageFile.write(chunk)
            except requests.exceptions.ConnectionError:
                print(f"{friend.name}'s image not found.\n")
                pass