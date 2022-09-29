from distutils.command.config import config
import os
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

class Facebook:
    def __init__(self, driver):
        self.driver = driver
        self.url = config.BASE_URL

    # TODO create test for login
    def login(self):
        print('\nAuthenticating...')
        self.driver.get(config.BASE_URL)
        sleep(1)
        
    def get_target_id(self):
        sleep(2)
        os.system('cls')
        config.TARGET_ID = input('\nEnter target\'s "profile name" or "ID": ')
        config.FRIENDS_URL = f'https://www.facebook.com/{config.TARGET_ID}/friends'
        return config.TARGET_ID


class FriendsPage:
    def __init__(self, driver):
        self.driver = driver
        self.url = config.FRIENDS_URL
        self.results = []

    def fsleep(self):
        sleep(choice(arange(0.5, 2.5, 0.1)))

    def navigate(self):
        print(f'\nGetting target\'s friends page...')
        sleep(3)
        self.driver.get('{}{}/friends'.format(config.BASE_URL, config.TARGET_ID))

    # Expands and render all friends page
    def show_friends(self):
        friends_link = self.driver.find_element(By.XPATH, "//a[text()='Amigos' or text()='Friends']")
        friends_link.click()
        os.system('cls')
        sleep(2)
        os.system('cls')
        print('\nRendering results page. Please wait...')

        while True:
            self.fsleep()
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                self.driver.find_element(By.XPATH, "//a[text()='Check-ins']")
                break
            except:
                pass
    
    # Save all friends elements into a list
    def _get_friends_boxes(self):
        self.fsleep()
        friends_boxes = self.driver.find_elements(By.XPATH, config.FRIENDS_BOXES)
        return friends_boxes

    def _get_friend_name(self, box):
        self.fsleep()
        try:
            name = box.find_element(By.XPATH, './/div[2]/div/a/span').text
            return normaliza(name)
        except:
            pass

    def _get_friend_img_src(self, box):
        try:
            img = box.find_element(By.XPATH, './/img')
            img_src = img.get_attribute('src')
            return img_src
        except:
            pass

    def _get_friend_id(self, box):
        try:
            link_id = box.find_element(By.XPATH, './/div[2]/div/a').get_attribute('href')
            id = link_id.strip('https://www.facebook.com/rofile.php?id=')
            return id
        except:
            pass

    def _get_friend_url(self, box):
        return config.BASE_URL + self._get_friend_id(box)

    def _get_target_profile_name(self):
        config.target_name = self.driver.find_element(By.XPATH, '//h1').text
        config.target_name = normaliza(config.target_name)
        return config.target_name

    # Get all friends data
    def get_all_data(self):
        self.fsleep()
        target_name = self._get_target_profile_name()
        results_list = []
        friends_boxes = self._get_friends_boxes()
        print('\nExtraindo dados...')

        # Parse all results into a iterable
        for box in tqdm(friends_boxes[:-1]):  # the last element is not a friend
            try:
                results_list.append([config.TARGET_ID,
                                     target_name,
                                     'facebook_friends',  # relationship
                                     self._get_friend_name(box),  # Friend name
                                     self._get_friend_id(box),  # Friend id
                                     # self._get_friend_work(box),  # Friend details (i.e. "Works at...")
                                     'images\\{}_{}.jpg'.format(self._get_friend_name(box).replace(' ', '_'),
                                                                self._get_friend_id(box)),  # Friend image path
                                     self._get_friend_url(box),  # Friends url
                                     self._get_friend_img_src(box)])  # Friends image url
            except:
                pass
        self.results = results_list
        return self.results

    # Downloads friends images
    def download_friends_images(self):
        images_folder = config.IMAGES_FOLDER
        # Create images folder
        os.makedirs(images_folder, exist_ok=True)
        # if not os.path.exists(images_folder):
        #     os.makedirs(images_folder)
        friends_boxes = self._get_friends_boxes()
        for box in tqdm(friends_boxes[:-1]):  # the last element is not a friend
            try:
                img_src = self._get_friend_img_src(box)
                res = requests.get(img_src)
            except requests.exceptions.InvalidURL:
                print(f'Image URL {img_src} invalid for friend {self._get_friend_name}')
            except requests.exceptions.MissingSchema:
                print(f'Image URL {img_src} invalid for friend {self._get_friend_name}')
            with open(os.path.join(images_folder, '{}_{}.jpg'.format(self._get_friend_name(box).replace(' ', '_'),
                                                                     self._get_friend_id(box))),
                      mode='wb') as imageFile:
                for chunk in res.iter_content(100000):
                    imageFile.write(chunk)
