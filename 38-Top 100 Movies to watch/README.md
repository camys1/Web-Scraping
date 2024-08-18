# Top 100 Movies Web Scraper

This Python project is a web scraper that extracts the titles of the top 100 movies from a specific webpage. The movie titles are then saved to a text file in descending order, starting from the best movie.

## Project Overview

This project uses the `requests` library to fetch a webpage and `BeautifulSoup` from the `bs4` package to parse the HTML content. The scraper targets the titles of the top 100 movies, reverses the list, and then saves it to a text file.

### Features

- Fetches a list of the top 100 movies from a webpage.
- Reverses the list so the movies are ordered from 1 to 100.
- Saves the movie titles to a text file.

## Requirements

To run this project, you need Python installed on your system, along with the following Python packages:

- `requests`
- `beautifulsoup4`

You can install these packages using `pip`:

```bash
pip install requests beautifulsoup4
