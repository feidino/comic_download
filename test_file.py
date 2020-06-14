import requests
import urllib3

res = requests.get('https://localprod.pandateacher.com/python-manuscript/crawler-html/chromedriver/ChromeDriver.html')
print(res.text)


