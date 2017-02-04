"""
Sample data for tests
"""

import base64


NSFW_IMAGE_URL = 'http://xxx-picture.com/wp-content/uploads/2016/09/Kriti-Kharbanda-Hardcore-Sex-Nude-Picss.jpg'
NSFW_IMAGE = open('tests/data/files/nsfw.jpeg', "rb")

SFW_IMAGE_URL = 'http://ichef.bbci.co.uk/news/660/cpsprodpb/37B5/production/_89716241_thinkstockphotos-523060154.jpg'
SFW_IMAGE = open('tests/data/files/random.png', "rb")

NSFW_IMAGE_BASE64 = open('tests/data/files/nsfw_b64', "r").read()
SFW_IMAGE_BASE64 = open('tests/data/files/sfw_b64', "r").read()
