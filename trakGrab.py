# trakGrab7.py
# Daniel Guilbert and Teksyn
# 12.15.22
# v7.0

from requests import get
from bs4 import BeautifulSoup
import re
import os

# Get information
artist = input("Enter the artist name (e.g. greed): ")
song = input("Enter the song name (e.g. Excavate): ")

print("Connecting to traktrain.com...")

# Download the HTML of the website
try:
    html = get("http://www.traktrain.com/" + artist).text
except Exception as e:
    print("There was an error connecting to the website:")
    print(e)
    print("Please check your internet connection and try again.")
    exit()

print("Connected!\n")

# Parse the HTML with BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# Find the base URL of the AWS server
base_url = soup.find("script", {"id": "aws-config"}).text
base_url = base_url.split("AWS_BASE_URL")[1].split("'")[1]

# Create the directory to store the downloaded songs
pwd = os.getcwd()
pwd = pwd + "\\songs\\" + artist + "\\"
if not os.path.exists(pwd):
    os.makedirs(pwd)

# If downloading a single song
if song != '*':
    # Find the song metadata and create the full URL to the mp3 file
    song_div = soup.find("div", {"data-player-info": {"name": song}})
    if song_div is None:
        print("That song could not be found, please try again.")
        exit()

    song_src = song_div["data-player-info"]["src"]
    song_url = base_url + song_src

    print("Downloading '" + song + "'")
    # Download the mp3 file
    req = Request(song_url)
    req.add_header('Referer', 'https://traktrain.com/') #traktrain blocks access unless this is set

    song_name = re.sub(r'[^\w|\s]', '', song)
    outfile = open(pwd + song_name + ".mp3", 'wb')
