# Description: This is a virtual assistant program that will greet you with a random greeting, get the date,
# time, retrieve information on a person and perform basic calculations.

# Resource Used: https://randerson112358.medium.com/build-a-virtual-assistant-using-python-2b0f78e68b94

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
import webbrowser
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
        data = r.recognize_google(audio) # Google Speech Recognition converts audio to text.
        print('Hey, you said: ' + data)
    except sr.UnknownValueError:
        print('Google Speech Recognition could not understand')
    except sr.RequestError as e:
        print('Request error from Google Speech Recognition')
        
    return data.lower()


# Function to get the virtual assistant response
def assistantResponse(text):
    print(text)

    # Convert the text to speech
    myObj = gTTS(text=text, lang='en', slow=False)

    # Save the converted audio to a file
    myObj.save('assistant_response.mp3')    

    # Play the converted file and delete
    os.system('start assistant_response.mp3')
    os.remove('assistant_response.mp3')

# A function to check for wake word(s)
def wakeWord(text):
    WAKE_WORDS = ['hey charlie', 'okay charlie', 'hey computer', 'okay computer', 'charlie']
    text = text.lower() # Convert the text to lower case

    # Check to see if the users command/text contains a wake word
    for phrase in WAKE_WORDS:
        if phrase in text:
            return True

    # Result if wake word was not found
    return False

def getDate():
    now = datetime.datetime.now()
    my_date = datetime.datetime.today
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

# Function to get a person first and last name
def getPerson(text):
    wordList = text.split() # Split text into a list of words

    for i in range(0, len(wordList)):
        if i + 3 <= len(wordList) - 1 and wordList[i].lower() == 'who' and wordList[i + 1].lower() == 'is':
            return wordList[i + 2] + ' ' + wordList[i + 3]

    
while True:
    # Record the audio
    text = recordAudio()
    response = '' # Empty response string initiially

    # Checking for the wake word/phrase 
    if (wakeWord(text) == True):
        # Check for greetings by the user
        response = response + greeting(text)

        # Check to see if the user ask for date
        if ('date' in text):
            get_date = getDate()
            response = response + ' ' + get_date

        # Check to see if the user said time
        elif ('time' in text):
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
            
            response = response + ' ' + 'It is ' + str(hour) + ':' + minute + ' ' + meridiem + '. ' 


        # Check to see if the user wants to know about a person
        elif ('who is' in text):
            person = getPerson(text)
            wiki = wikipedia.summary(person, sentences = 2)
            response = response + ' ' + wiki

        # Search Google
        elif 'open google and search' in text:
            reg_ex = re.search('open google and search (.*)', text)
            search_for = text.split("search", 1)[1] # Stores search keyword from the user
            url = 'https://www.google.com/'
            # if reg_ex:
            #     subgoogle = reg_ex.group(1)
            #     url = url + 'r/' + subgoogle
            # print('Okay!')

            driver = webdriver.Chrome("C:/Users/cogbo2/Computer Programs/Python/chromedriver.exe")
            driver.get('http://www.google.com')
            search = driver.find_element_by_name('q') # Finds search box element
            search.send_keys(str(search_for)) # Sends search keys
            search.send_keys(Keys.RETURN) # Hits enter

        elif 'what is' in text:
            reg_ex = re.search('what is (.*)', text)
            search_for = text.split("is", 1)[1] # Stores search keyword from the user
            url = 'https://www.google.com/'
            # if reg_ex:
            #     subgoogle = reg_ex.group(1)
            #     url = url + 'r/' + subgoogle
            # print('Okay!')

            driver = webdriver.Chrome("C:/Users/cogbo2/Computer Programs/Python/chromedriver.exe")
            driver.get('http://www.google.com')
            search = driver.find_element_by_name('q') # Finds search box element
            search.send_keys(str(search_for)) # Sends search keys
            search.send_keys(Keys.RETURN) # Hits enter
        

        if (len(response) > 0):
            # Assistant Audio Response 
            assistantResponse(response)
        else:
            continue
        
        

