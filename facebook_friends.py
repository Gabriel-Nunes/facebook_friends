from modules.facebook import Facebook
# from modules.facebook import FriendsPage
from modules.facebook_bs4 import Facebook, FriendsPage
from modules.browser import Browser
from time import sleep
from modules import config
import os
import csv

# Keep console on top right (OS Windows)
# if 'posix' not in os.name:
#     import win32gui, win32con

#     windowList = []
#     win32gui.EnumWindows(lambda hwnd, windowList: windowList.append((win32gui.GetWindowText(hwnd),hwnd)), windowList)
#     cmdWindow = [i for i in windowList if "python" in i[0].lower()]
#     win32gui.SetWindowPos(cmdWindow[0][1],win32con.HWND_TOP,800,0,600,350,0) #100,100 is the size of the window

if __name__ == '__main__':

    clear_screen = 'clear' if 'posix' in os.name else 'cls'

    browser = Browser()
    driver = browser.driver
    driver.get("https://www.facebook.com")
    sleep(2)
    input("Please login on Facebook and press any key to continue...")
    os.system(clear_screen)
    continua = ''
    while continua not in ['n', 'N']:
        facebook = Facebook(driver)
        friends_page = FriendsPage(driver, facebook.target_id, facebook.target_name)
        friends_page.navigate()
        # friends_page.show_friends()
        friends = friends_page.get_all_data()

        print('\nRecording results. Wait...\n')
        # create results folder
        os.makedirs(config.RESULTS_FOLDER, exist_ok=True)
        # TODO change target name to facebook class
        with open(os.path.join(config.RESULTS_FOLDER, 'friends_{}_{}.csv'.format(friends_page.target_name, friends_page.target_id)), mode='w', newline='',
                  encoding='utf-8') as file:
            headers = ['target_id', 'target_name', 'link_name', 'friend_id', 'friend_name', 
                       'friend_image', 'url_friend_profile', 'url_friend_image']
            writer = csv.writer(file)
            writer.writerow(headers)
            for friend in friends:
                image_uri = os.path.join('images', '{}_{}.jpg'.format(friend.name.replace(' ', '_'),
                                                                        friend.id))
                writer.writerow([facebook.target_id, 
                                friends_page.target_name, 
                                'facebook friends', 
                                friend.id,
                                friend.name,
                                image_uri,
                                friend.profile_url,
                                friend.image_url])

        print('\nData file generated!\n\n')
        sleep(2)

        print('\nDownloading images...\n')
        friends_page.download_friends_images()

        print(('\nOk!\n'))
        continua = input('\nWant to crawl another profile? (s/n) ')
        print()

    print('\nFinished!!!')
    os.startfile(config.RESULTS_FOLDER)
    driver.quit()

    print('Press any key to exit...')
    os.system('pause')