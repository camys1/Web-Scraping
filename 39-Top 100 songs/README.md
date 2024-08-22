# Billboard 100 Spotify Playlist Creator

This Python project creates a private Spotify playlist based on the Billboard Hot 100 chart for a specific date. It scrapes the Billboard website to extract the top 100 songs for the given date and then adds these songs to a new Spotify playlist.

## Project Overview

This project uses the requests library to fetch the Billboard Hot 100 webpage and BeautifulSoup from the bs4 package to parse the HTML content. It extracts the titles of the top 100 songs, searches for them on Spotify, and adds them to a newly created private playlist.

### Features
- Fetches the Billboard Hot 100 list for a specific date.
- Searches for each song on Spotify and collects their URIs.
- Creates a new private Spotify playlist with the title YYYY-MM-DD Billboard 100.
- Adds the found songs to the newly created Spotify playlist.

## Requirements

To run this project, you need Python installed on your system, along with the following Python packages:

- `requests`
-`beautifulsoup4`
-`spotipy`
-`pprint`

You can install these packages using `pip`:

bash
Copy code
pip install requests beautifulsoup4 spotipy pprint

## Setup
Spotify API Setup:

- Create a Spotify Developer account and register a new app.
- Obtain your Spotify API credentials (Client ID and Client Secret).
- Set your Redirect URI to http://example.com.

## Environment Variables:

You can either set environment variables for SPOTIFY_CLIENT_ID, SPOTIFY_SECRET, and REDIRECT_URI, or directly include them in your script.
Usage

## Run the script:

bash
Copy code
python billboard_to_spotify.py

Input the desired date when prompted:

Enter the date in the format YYYY-MM-DD.

Authenticate with Spotify:

A browser window will open to log in to your Spotify account and authorize the app.

Playlist Creation:

The script will scrape the Billboard Hot 100 for the given date, create a private playlist on your Spotify account, and add the available songs to it.

### Troubleshooting
- Authentication Issues: Ensure the Redirect URI matches between your Spotify Developer Dashboard and the script.
- Missing Songs: Some songs may not be available on Spotify and will be skipped.
- Token Issues: If the token.txt file isn't created, double-check your OAuth setup.
