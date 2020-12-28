# Description: This is a virtual assistant program that will greet you with a random greeting, get the date,
# time, retrieve information from wikipedia, open videos on Youtube and read the latest news.


# Import the libraries
import speech_recognition as sr 
import os
from gtts import gTTS 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import datetime
import warnings
import calendar 
import random 
import wikipedia 
import re 
import pyttsx3
import webbrowser
from bs4 import BeautifulSoup as soup
import urllib.request #used to make requests
import urllib.parse #used to parse values into the url


# Ignore any warning messages
warnings.filterwarnings('ignore')

# Record audio and return it as a string
def recordAudio():
    # Record the audio
    r = sr.Recognizer()
    with sr.Microphone() as source: # Create an instance of microphone
        print ('Say something...')
        r.pause_threshold = 1
        #wait for a second to let the recognizer adjust the  
        #energy threshold based on the surrounding noise level 
        r.adjust_for_ambient_noise(source, duration=1)
        #listens for the user's input
        audio = r.listen(source)

    # Speech recognition using Google's Speech Recognition
    data = ''
    try: 
        data = r.recognize_google(audio).lower() # Google Speech Recognition converts audio to text.
        print('Hey, you said: ' + data)
    except sr.UnknownValueError:
        print('Google Speech Recognition could not understand')
    except sr.RequestError as e:
        print('Request error from Google Speech Recognition')
        
    return data.lower()


# Function to get the virtual assistant response in speech
def assistantResponse(text):
    print(text)

    # # Convert the text to speech
    # myObj = gTTS(text=text, lang='en', slow=False)
    
    # # Save the converted audio to a file
    # myObj.save('assistant_response.mp3')    

    # # Play the converted file and delete
    # os.system('start assistant_response.mp3')
    # os.remove('assistant_response.mp3')

    # Using python text to speech offline since there has been some problems with gTTS 
    # (https://github.com/pndurette/gTTS/issues/232)
    # (https://github.com/luoliyan/chinese-support-redux/issues/161#issuecomment-727697730)
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    engine.stop()


# A function to check for wake word(s)
def wakeWord(text):
    WAKE_WORDS = ['hey charlie', 'okay charlie', 'hey computer', 'okay computer', 'charlie', 'computer']
    text = text.lower() # Convert the text to lower case

    # Check to see if the users command/text contains a wake word
    for phrase in WAKE_WORDS:
        if phrase in text:
            return True

    # Result if wake word was not found
    return False

# A function to get the current date 
def getDate():
    now = datetime.datetime.now()
    my_date = datetime.datetime.today()
    weekday = calendar.day_name[my_date.weekday()] # Returns weekdays e.g. Monday
    monthNum = now.month
    dayNum = now.day
    month_names = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    ordinalNumbers = ['1st', '2nd', '3rd', '4th', '5th', '6th', 
                      '7th', '8th', '9th', '10th', '11th', '12th',                      
                      '13th', '14th', '15th', '16th', '17th', 
                      '18th', '19th', '20th', '21st', '22nd', 
                      '23rd', '24th', '25th', '26th', '27th', 
                      '28th', '29th', '30th', '31st']
    
    return 'Today is ' + weekday + ', ' + month_names[monthNum - 1] + ' the ' + ordinalNumbers[dayNum - 1] + '.'

# A function to get the current timer 
def getTime():
    now = datetime.datetime.now()
    meridiem = ''
    if now.hour >= 12:
        meridiem = 'p.m' # Post Meridiem (PM)
        hour = now.hour - 12
    else:
        meridiem = 'a.m' # Ante Meridiem (AM)
        hour = now.hour
    
    # Convert minute into a proper string e.g. '09' 
    if now.minute < 10:
        minute = '0' + str(now.minute)
    else:
        minute = str(now.minute)
    
    return 'Time is ' + str(hour) + ':' + minute + ' ' + meridiem + '. ' 


# Function to retrieve headlines (titles) from rss feed and return them as list
def getRSSHeadlines(rss_url):
    Client = urllib.request.urlopen(rss_url)
    xml_page = Client.read()
    Client.close()
    soup_page = soup(xml_page, "lxml") # Install lxml for parsing
    return soup_page.findAll("item") # Returns all news items from the RSS news feed

# Function to return random greeting response to user
def greeting(text):
    # Greeting Inputs
    GREETING_INPUTS = ['hi', 'hey', 'yo', 'wassup', 'hola', 'greetings', 'hello']

    # Greeting Response back to the user 
    GREETING_RESPONSES = ['howdy', 'whats good', 'hello', 'hey there', 'how are you', 'hey', 'hey homie', 'hello friend']

    # If the user input is a greeting, then return random response
    for word in text.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES) + '.'
    
    # If no greeting was detected, then return an empty string
    return ''


if __name__ == "__main__":
        
    while True:
        # Record the audio
        text = recordAudio()

        # Checking for the wake word/phrase 
        if (wakeWord(text) == True):
            # Check for greetings by the user
            assistantResponse(greeting(text))
            
            # Charlie's Introduction
            if ('your name' in text):
                assistantResponse("I am Charlie, your Virtual Assistant!")

            # Check to see if the user asked for date
            elif ('date' in text):
                get_date = getDate()
                assistantResponse(get_date)

            # Check to see if the user said time
            elif ('time' in text):
                get_time = getTime()
                assistantResponse(get_time)

            # Search Google
            elif 'open google and search' in text:
                reg_ex = re.search('open google and search (.*)', text)
                search_for = text.split("search ", 1)[1] # Stores search keyword from the user
                # For debugging
                # print(search_for)

                # Install Chrome driver for desired platform and place on system path
                driver = webdriver.Chrome() 
                driver.get('http://www.google.com')
                search = driver.find_element_by_name('q') # Finds search box element
                search.send_keys(str(search_for)) # Sends search keys
                search.send_keys(Keys.RETURN) # Hits enter

            # Open videos on YouTube
            elif ('youtube' in text):
                assistantResponse("Ok!")
                reg_ex = re.search('youtube (.+)', text)
                if (reg_ex):
                    domain = text.split("search ", 1)[1]
                    query_string = urllib.parse.urlencode({"search_query" : domain})
                    html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string) 
                    search_results = re.findall(r'watch\?v=(\S{11})', html_content.read().decode()) # finds all links in search result
                    webbrowser.open("http://www.youtube.com/watch?v={}".format(search_results[0]))
                    pass
            
            # Search for terms on Wikipedia
            elif ('search wikipedia for' in text):
                assistantResponse("Searching through wikipedia ")
            
                try: 
                    reg_ex = re.search('search wikipedia for (.*)', text)
                    if (reg_ex):
                        wiki_search = text.split("wikipedia for ", 1)[1] # Stores search keyword from the user
                        # For debugging
                        # print(wiki_search)

                        wiki = wikipedia.summary(wiki_search, sentences = 3)
                        assistantResponse(wiki)
                except: 
                    assistantResponse("The term could not be found on Wikipedia")

            # Retrieve latest news feeds
            elif ('news for today') in text:
                try:
                    news_url = "https://news.google.com/news/rss"
                    news_list = getRSSHeadlines(news_url)
                    
                    for news in news_list[:15]:
                        assistantResponse(news.title.text)
                except Exception as e:
                    print(e)

            