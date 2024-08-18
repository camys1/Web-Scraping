import requests
from bs4 import BeautifulSoup

URL = "https://web.archive.org/web/20200518073855/https://www.empireonline.com/movies/features/best-movies-2/"

response = requests.get(URL)
response.raise_for_status()
movie_web_page = response.text

soup = BeautifulSoup(movie_web_page, "html.parser")

all_movies = soup.find_all(name="h3", class_="title")
movie_titles = [movie.getText() for movie in all_movies]
movies = movie_titles[::-1]

with open("/Users/samui/Desktop/Python/Web Scraping/38-Top 100 Movies to watch/movies to watch.txt", "w", encoding="utf-8") as output_file:
    for movie in movies:
        output_file.write(f"{movie}\n")
