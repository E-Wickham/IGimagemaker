
import requests
from bs4 import BeautifulSoup
from io import BytesIO
from PIL import Image,ImageFont,ImageDraw, ImageFilter
import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

'''
0. Enter personal info
'''

#get JSON data from podcast host
response = requests.get('INSERT API REQUEST URL HERE')

#Unsplash API KEYS
access_key = 'INSERT UNSPLASH API KEY'
secret_key = 'INSERT UNSPLASH SECRET KEY'

#Instagram login information
username = "INSERT INSTAGRAM USERNAME"
password = "INSERT INSTAGRAM PASSWORD"

'''

1. API CALL 
'''


#place data into variables
episodes = response.json()
epTitle = episodes[0]["title"]
epDesc = episodes[0]['description']

'''
2. IMAGE CAPTION
'''

#Create image caption for Instagram
cleantext = BeautifulSoup(epDesc, "lxml").text
cleantextSplit = cleantext.split("Plugs and Recs")  
imgCaption = cleantextSplit[0]

promoText = "**NEW EPISODE: " +epTitle+ "** "
hashtags = "Head to bigshinytakes.com (or wherever you get your podcasts) and listen now! #podcast #news #newspaper #canada #tech #billionaires #tesla #boomers"
caption = promoText + ''.join(imgCaption) + hashtags

print(caption)

'''
3. UNSPLASH IMAGE PULL
'''
#enter keyword to search on Unsplash
category = input("Enter a keyword for the image you want: ")



#API Call
picture_url = "https://api.unsplash.com/search/photos"
picture_response = requests.get(picture_url, headers={'content-type': 'applications/json'}, params={'query': category, 'client_id': access_key})
data = picture_response.json()

#instead of the first result pick a random one
number = random.randint(0,10)

image_url = data['results'][number]['urls']['raw']
image_width = int(data['results'][number]['width'])
image_height = int(data['results'][number]['height'])

image_owner_name = data['results'][number]['user']['name']

response = requests.get(image_url)
img = Image.open(BytesIO(response.content))

## TO DO: set a prompt to make sure the random image is the one that you want


print("current image height: ")
print(image_height)

## resize image so it is more in line with the size of the instagram post
if image_height > image_width:
    if image_width > 6000:
        # divide image w/h by 5
        image_width = int(image_width/5)
        image_height = int(image_height/5)
    elif image_width > 5000:
        #divide image w/h by 4
        image_width = int(image_width/4)
        image_height = int(image_height/4)
    elif image_width > 4000:
        #divide image w/h by 3
        image_width = int(image_width/3)
        image_height = int(image_height/3)
    elif image_width > 3000:
        #divide image w/h by 2.5
        image_width = int(image_width/2.5)
        image_height = int(image_height/2.5)
    elif image_width > 2500:
        #divide image w/h by 2
        image_width = int(image_width/2)
        image_height = int(image_height/2)
elif image_width > image_height:
    if image_height > 6000:
        # divide image w/h by 5
        image_width = int(image_width/5)
        image_height = int(image_height/5)
    elif image_height > 5000:
        #divide image w/h by 4
        image_width = int(image_width/4)
        image_height = int(image_height/4)
    elif image_height > 4000:
        #divide image w/h by 3
        image_width = int(image_width/3)
        image_height = int(image_height/3)
    elif image_height > 3000:
        #divide image w/h by 2.5
        image_width = int(image_width/2.5)
        image_height = int(image_height/2.5)
    elif image_height > 2500:
        #divide image w/h by 2
        image_width = int(image_width/2)
        image_height = int(image_height/2)

print("new image height: ")
print(image_height)

newImg =  img.resize((image_width,image_height))


## if portrait or landscape, and if the longer side is more than double etc 
## check automate the boring stuff for the proper way to resize something

newImg.save('assets/unsplashPull.png','PNG')

imgLocation = 'assets/unsplashPull.png'
'''
4. SOCIAL MEDIA IMAGE CREATION
'''
##set constants in the image creator bot
SQUARE_FIT_SIZE = 1080
OVERLAY_FILENAME = 'assets/fancysquare.png'

## open image file and crop it to 1080px x 1080px
img = Image.open(imgLocation)
img = img.filter(ImageFilter.GaussianBlur(5))

imgCropped = img.crop(box = (0,0,1080,1080))
imgCroppedWidth, imgCroppedHeight = imgCropped.size

##open overlay 
overlayImg = Image.open(OVERLAY_FILENAME)
overlayWidth, overlayHeight = overlayImg.size

imgCropped.paste(overlayImg,(0,0),overlayImg)

##String can be 36 Characters long at size 50 
##              45 at size 40
##              58 at size 30
str1 = epTitle

## instead of line break write an if statement based on the string length of the text - > if it's over a certain amount -> make the font size THIS much smaller
if len(str1) <= 36:
    font = ImageFont.truetype("assets/Montserrat-Bold.ttf",50)
elif len(str1) <= 45:
    font = ImageFont.truetype("assets/Montserrat-Bold.ttf",45)
elif len(str1) <=58:
    font = ImageFont.truetype("assets/Montserrat-Bold.ttf",30)
elif len(str1) <=68:    
    font = ImageFont.truetype("assets/Montserrat-Bold.ttf",28)
else:
    str1 = "New Episode"
    font = ImageFont.truetype("assets/Montserrat-Bold.ttf",90)


w,h = font.getsize(str1)

# draw the text on to the image
draw = ImageDraw.Draw(imgCropped)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
draw.text(((1080-w)/2,(1080-h)/2),str1,font=font,fill="white")

#show your work
imgCropped.show()
imgCropped.save('assets/newIGimg.png')

    ## to do:   take the image and post it to instagram
    ##          find a way to monitor whether the Episode Title has changed from the previous one

'''
5. OPEN BROWSER
'''



mobile_emulation = {

   "deviceMetrics": { "width": 400, "height": 800, "pixelRatio": 3.0 },

   "userAgent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Mobile Safari/537.36" }

chrome_options = Options()

chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)


driver = webdriver.Chrome('assets/chromedriver.exe', chrome_options = chrome_options)  # Optional argument, if not specified will search path.

driver.get('https://www.instagram.com/accounts/login/');

time.sleep(5) # Let the user actually see something!

username_input = driver.find_element_by_css_selector("input[name='username']")
password_input = driver.find_element_by_css_selector("input[name='password']")

username_input.send_keys(username)
password_input.send_keys(password)

login_button = driver.find_element_by_xpath("//button[@type='submit']")
login_button.click()
