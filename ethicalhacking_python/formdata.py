import requests

URL = 'https://docs.google.com/forms/d/e/1FAIpQLSe2AVPWndQNSqyzDbJV2Lf8IhN8momnj-m2vdcHfs2cnE9A_g/viewform?usp=sf_link'

form_data = {"Isn't Python Awesome":'Until Next time!'}

r = requests.post(url=URL,data=form_data)