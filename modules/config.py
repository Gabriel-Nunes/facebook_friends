#!/usr/lib/python3.5
# -*- coding: utf-8 -*-

import os

BASE_URL='https://www.facebook.com/'

# TARGET_ID = sys.argv[1]  # recebe o id do alvo através de argumento da linha de comando
TARGET_ID=''
target_profile_name='//span/h1[@dir][1]'
target_name=''
FRIENDS_URL='{}{}/friends'.format(BASE_URL, TARGET_ID)
FRIENDS_PAGE_END='medley_header_photos'  # id da tag que aparece ao final da página de amigos

FRIENDS_BOXES="/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div[1]/div/div/div/div/div[3]/div"
FRIENDS_BOX="//a[text()='Amigos' or text()='Friends']/../../../../../../../div[3]"
RESULTS_FOLDER='results'
IMAGES_FOLDER=os.path.join(RESULTS_FOLDER, 'images')
