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


class Friend:
    def __init__(self, name: str, id: str, profile_url: str, image_url: str):
        self.id = id
        self.name = name
        self.profile_url = profile_url
        self.image_url = image_url


class Facebook:
    base_url = 'https://www.facebook.com/'
    
    def __init__(self, driver):
        self.driver = driver
        self.target_id = ''

    # TODO create test for login
    def login(self):
        print('\nAuthenticating...')
        self.driver.get(self.base_url)
        sleep(1)
        
    def get_target_id(self):
        sleep(2)
        os.system('cls')
        config.TARGET_ID = input('\nEnter target\'s "profile name" or "ID": ')
        config.FRIENDS_URL = f'{self.base_url}{config.TARGET_ID}/friends'
        return config.TARGET_ID


class FriendsPage(Facebook):
    def __init__(self, driver):
        self.driver = driver
        self.url = config.FRIENDS_URL
        self.target_id = config.TARGET_ID
        self.target_name = config.target_name
        self.results = []
        self.friends_box = self.driver.find_element(By.XPATH, config.FRIENDS_BOX)
        self.friends_box_html = ''
    
    def _get_target_profile_name(self):
        try:
            config.target_name = self.driver.find_element(By.XPATH, '//h1').text
            config.target_name = normaliza(config.target_name)
            return config.target_name
        except:
            print("Profile locked!")
            return ''

    def fsleep(self):
        sleep(choice(arange(0.5, 2.5, 0.1)))

    def navigate(self):
        print(f'\nFetching target\'s friends page...')
        sleep(3)
        self.driver.get('{}{}/friends'.format(config.BASE_URL, config.TARGET_ID))

    # Get the number of target's friends
    def _get_number_of_friends(self):
        number_of_friends_tag = self.driver.find_element(By.XPATH, f"//a[@href='https://www.facebook.com/profile.php?id={config.TARGET_ID}&sk=friends'][1]")
        number_of_friends_text = number_of_friends_tag.text
        return int(re.sub(r"(\samigos.*|\sfriends.*)", "", number_of_friends_text)) - 1  # Facebook always show one friend more

    # Expands and render all friends page
    def _show_friends(self):
        try:
            self.driver.get(f"{config.FRIENDS_URL}")
            os.system('cls')
            sleep(2)
            os.system('cls')
            print('\nRendering results page. Please wait...')
            num_friends = self._get_number_of_friends()
            while True:
                self.fsleep()
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                # Try to fetch the last friend box
                try:
                    self._get_friends_boxes()[num_friends]
                    self.fsleep()
                    self.friends_box_html = self.friends_box.get_attribute('innerHTML')
                    break
                except:
                    pass
        except:
            print(f"Friends of - {config.TARGET_ID} - {config.target_name} - may not be available for you!")

    # Parse friends data from an html string
    def parse_friends(box_string) -> list:
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
                new_friend = Friend(friend_id, friend_name, friend_profile, friend_image_url)
                results.append(new_friend)
            except:
                pass
        return results

    # Get all friends data
    def get_all_data(self):
        self.fsleep()
        self._show_friends()
    
        print('\nExtracting data...')

        # Parse all results into a iterable
        self.results = self.parse_friends(self.friends_box_html)

    # TODO Downloads friends images using self.results links
    def download_friends_images(self):
        images_folder = config.IMAGES_FOLDER
        # Create images folder
        os.makedirs(images_folder, exist_ok=True)
        # if not os.path.exists(images_folder):
        #     os.makedirs(images_folder)
        friends_boxes = self._get_friends_boxes()
        for box in tqdm(friends_boxes):
            friend_name = self._get_friend_name(box)
            friend_id = self._get_friend_id(box)
            try:
                img_src = self._get_friend_img_src(box)
                res = requests.get(img_src)
            except requests.exceptions.InvalidURL:
                print(f'Image URL {img_src} invalid for friend {friend_name}')
            except requests.exceptions.MissingSchema:
                print(f'Image URL {img_src} invalid for friend {friend_name}')
            with open(os.path.join(images_folder, '{}_{}.jpg'.format(friend_name.replace(' ', '_'),
                                                                     friend_id)),
                      mode='wb') as imageFile:
                for chunk in res.iter_content(100000):
                    imageFile.write(chunk)
