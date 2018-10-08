import inkyphat
from datetime import date, timedelta
import glob
from PIL import Image, ImageFont
import datetime
from darksky import forecast
import textwrap


#inkyphat: https://learn.pimoroni.com/tutorial/sandyj/getting-started-with-inky-phat
#darksky: https://darksky.net/dev/docs#response-format



##### Get the weather from Darksky #####

#set lat/long for location
LOCATION = 40.8791, -81.4656

#set Darksky API Key
APIKEY='KEY-HERE'


with forecast(APIKEY, *LOCATION) as location:
    #today
    summary = location['daily']['data'][0]['summary']
    summaryWeek = location['daily']['summary']
    currentTemp = location['currently']['temperature']
    highTemp = location['daily']['data'][0]['temperatureHigh']
    lowTemp = location['daily']['data'][0]['temperatureLow']
    iconDesc = location['currently']['icon']
    precipProbability = location['currently']['precipProbability']
    precipType = location['daily']['data'][0]['precipType']

    #n+1
    iconDesc2 = location['daily']['data'][1]['icon']
    highTemp2 = location['daily']['data'][1]['temperatureHigh']
    lowTemp2 = location['daily']['data'][1]['temperatureLow']
    precipProbability2 = location['daily']['data'][1]['precipProbability']
    precipType2 = location['daily']['data'][1]['precipType']


    #n+2
    iconDesc3 = location['daily']['data'][2]['icon']
    highTemp3 = location['daily']['data'][2]['temperatureHigh']
    lowTemp3 = location['daily']['data'][2]['temperatureLow']
    precipProbability3 = location['daily']['data'][2]['precipProbability']
    precipType3 = location['daily']['data'][2]['precipType']


# today  variables 
currentTempFormatted = "{0:.0f}".format(currentTemp)
highTempToday = "High " + "{0:.0f}".format(highTemp)
lowTempToday = "Low " + "{0:.0f}".format(lowTemp) 
if precipProbability > 8:
    precipLine1 = "{0:.0%}".format(precipProbability) + " chance"
    precipLine2 = "of " + precipType
else: 
    precipLine1 = "No precip"
    precipLine2 = "today"


# day 2 variables 
tempsDay2 = "High " + "{0:.0f}".format(highTemp2) + " Low " + "{0:.0f}".format(lowTemp2)

if precipProbability2 > 8:
    precipDay2 = "{0:.0%}".format(precipProbability2) + " chance of " + precipType2
else: 
    precipDay2 = "No precipitation"

if iconDesc2 == "clear-day" or "clear-night":
    descriptionDay2 = "Clear skies"
elif iconDesc2 == "partly-cloudy-day" or "partly-cloudy-night":
    descriptionDay2 = "Partly Cloudy"
else:
    descriptionDay2 = iconDesc2.capitalize()



# day 3 variables 
tempsDay3 = "High " + "{0:.0f}".format(highTemp3) + " Low " + "{0:.0f}".format(lowTemp3)

if precipProbability3 > 8:
    precipDay3 = "{0:.0%}".format(precipProbability3) + " chance of " + precipType3
else: 
    precipDay3 = "No precipitation"

if iconDesc3 == "clear-day" or "clear-night":
    descriptionDay3 = "Clear skies"
elif iconDesc3 == "partly-cloudy-day" or "partly-cloudy-night":
    descriptionDay3 = "Partly Cloudy"
else:
    descriptionDay3 = iconDesc3.capitalize()







##### Draw on the inkyphat screen #####

# set screen type color. Be sure to change this to the color of your screen
inkyphat.set_colour("yellow")

# create font objects
fontBig = ImageFont.truetype(inkyphat.fonts.FredokaOne, 16)
fontMid = ImageFont.truetype(inkyphat.fonts.FredokaOne, 12)
fontSmall = ImageFont.truetype("/home/pi/Pimoroni/inkyphat/examples/04B.ttf" , 8)


#define weekday text
weekday = date.today()
day = date.strftime(weekday, '%A')

weekday2 = datetime.date.today() + datetime.timedelta(days=1)
day2 = date.strftime(weekday2, '%A')

weekday3 = datetime.date.today() + datetime.timedelta(days=2)
day3 = date.strftime(weekday3, '%A')


#draw some lines
inkyphat.line((118, 20, 118, 90),2) # Vertical line


### now draw the text##

#format today's name to center over left side
dayName = day
w, h = fontBig.getsize(day)
x = (inkyphat.WIDTH / 4) - (w / 2)
y = (inkyphat.HEIGHT / 4) - (h / 2)

#format the summary text for today
summaryFormatted = textwrap.fill(summary, 20)


#draw the suff on the left side of the screen
inkyphat.text((20, 5), day, inkyphat.BLACK, font=fontBig)
inkyphat.text((60, 29), highTempToday, inkyphat.BLACK, font=fontMid)
inkyphat.text((60, 41), lowTempToday, inkyphat.BLACK, font=fontMid)
inkyphat.text((60, 59), precipLine1, inkyphat.BLACK, font=fontSmall)
inkyphat.text((60, 69), precipLine2, inkyphat.BLACK, font=fontSmall)
inkyphat.text((60, 80), summaryFormatted, inkyphat.BLACK, font=fontSmall)


#draw the suff on the right side of the screen
#for weekday n+1
inkyphat.text((125, 12), day2, inkyphat.BLACK, font=fontMid)
inkyphat.text((125, 27), descriptionDay2, inkyphat.BLACK, font=fontSmall)
inkyphat.text((125, 35), tempsDay2, inkyphat.BLACK, font=fontSmall)
inkyphat.text((125, 43), precipDay2, inkyphat.BLACK, font=fontSmall)

#for weekday n+2
inkyphat.text((125, 57), day3, inkyphat.BLACK, font=fontMid)
inkyphat.text((125, 72), descriptionDay3, inkyphat.BLACK, font=fontSmall)
inkyphat.text((125, 80), tempsDay3, inkyphat.BLACK, font=fontSmall)
inkyphat.text((125, 88), precipDay3, inkyphat.BLACK, font=fontSmall)


# Load our icon files and generate masks
weather_icon = None
iconFromDS = iconDesc
icons = {}
masks = {}

#map description from the darksky API
icon_map = {
	"snow": ["snow", "sleet"],
	"rain": ["rain"],
	"cloud": ["cloudy", "partly-cloudy-day", "cloudy", "partly-cloudy-night"],
	"sun": ["clear-day", "clear-night"],
	"storm": ["thunderstorm", "tornado", "hail"],
    "wind": ["wind", "fog"]
}

for icon in icon_map:
    if iconFromDS in icon_map[icon]:
        weather_icon = icon
        break

for icon in glob.glob("resources/icon-*.png"):
    icon_name = icon.split("icon-")[1].replace(".png", "")
    icon_image = Image.open(icon)
    icons[icon_name] = icon_image
    masks[icon_name] = inkyphat.create_mask(icon_image)

if weather_icon is not None:
    inkyphat.paste(icons[weather_icon], (10, 27), masks[weather_icon])


#show current temp
inkyphat.text((21, 76), currentTempFormatted, inkyphat.YELLOW, font=fontBig)
inkyphat.text((11, 95), "currently. ", inkyphat.BLACK, font=fontSmall)


#push to the screen! 
inkyphat.show()
