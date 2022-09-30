from modules.facebook import Facebook
from modules.facebook import FriendsPage
from modules.browser import Browser
from time import sleep
from modules import config
import os
import csv


if __name__ == '__main__':
    if 'posix' not in os.name:
        from modules import screen_pos
        screen_pos.run()

    clear_screen = 'clear' if 'posix' in os.name else 'cls'

    browser = Browser()
    driver = browser.driver
    driver.get("https://www.facebook.com")
    facebook = Facebook(driver)
    
    sleep(2)
    os.system(clear_screen)
    input("Please login on Facebook and press any key to continue...")
    friends_page = FriendsPage(driver)
    
    continua = ''
    while continua not in ['n', 'N']:
        facebook.get_target_id()
        friends_page.navigate()
        friends_page.show_friends()
        results = FriendsPage(driver).get_all_data()

        print('\nRecording results. Wait...\n')
        # create results folder
        os.makedirs(config.RESULTS_FOLDER, exist_ok=True)
        with open(os.path.join(config.RESULTS_FOLDER, 'friends_{}_{}.csv'.format(config.target_name, config.TARGET_ID)), mode='w', newline='',
                  encoding='utf-8') as file:
            headers = ['target_id', 'target_name', 'link_name', 'friend_name', 'friend_id', 
                       'friend_image', 'url_friend_profile', 'url_friend_image']
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(results)

        print('\nData file generated!\n\n')
        sleep(2)

        print('\nDownloading images...\n')
        FriendsPage(driver).download_friends_images()

        print(('\nOk!\n'))
        continua = input('\nWant to crawl another profile? (s/n) ')
        print()

    print('\nFinished!!!')
    os.startfile(config.RESULTS_FOLDER)
    driver.quit()

    print('Press any key to exit...')
    os.system('pause')