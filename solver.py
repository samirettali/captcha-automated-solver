#!/usr/bin/env python3
import time
import subprocess
import requests
import urllib.parse
from selenium import webdriver

url = 'http://192.168.22.129/captcha/example7/'
captcha_selector = 'html body div.container form img'
input_selector = 'body > div.container > form > input[type=text]:nth-child(2)'
form_selector = 'body > div.container > form'

# Start a browser
browser = webdriver.Firefox()
browser.get(url)

# Find the image
elem = browser.find_element_by_tag_name(captcha_selector)
captcha_path = elem.get_attribute('src')

# Build the complete url
captcha_url = urllib.parse.urljoin(url, captcha_path)

# Get and save the image
img_raw = requests.get(captcha_url)
img = open('c.png', 'wb').write(img_raw.content)

# Clean the captcha
# subprocess.run(['magick', 'c.png', '-implode', '-0.6%', '-threshold', '41%', 'clean.jpg'], capture_output=True)
result = subprocess.run(['magick', 'c.png', '-threshold', '41%', 'clean.jpg'], capture_output=True)
subprocess.run(['open', 'clean.jpg'], capture_output=True)

# Run tesseract
result = subprocess.run(['tesseract', 'clean.jpg', 'stdout'], capture_output=True)
captcha = result.stdout.decode().strip()

print(captcha)

# Type the captcha
input_elem = browser.find_element_by_tag_name(input_selector)
for char in captcha:
    input_elem.send_keys(char)
    time.sleep(0.5)
input_elem.submit()
