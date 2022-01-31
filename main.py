from random import randrange
from flask import Flask, render_template, json
import requests
from dotenv import find_dotenv, load_dotenv
import os

load_dotenv(find_dotenv())

app = Flask(__name__)


movieList = ["155","49521","791373", "634649", "370172", "460465", "157336","11688"]

@app.route("/")
def homepage():
    random_number = randrange(len(movieList))
    response = requests.get("https://api.themoviedb.org/3/movie/" + movieList[random_number] + "?api_key=" + os.getenv("TMDB_KEY"))
    array = response.json()
    movie_details = api_call(array)
    #print(movie_details)
    #return (movie_details)
    page_url = url_api(movie_details["Name"])
    return render_template("index.html", movie_details = movie_details, page_url = page_url)

def api_call(api_response):
    #print(type(api_response))
    movie_details = {"Name": "", "Overview":"", "Genre":"", "Image":""}
    movie_details.update({"Name": api_response["original_title"]})
    movie_details.update({"Overview": api_response["overview"]})
    movie_details.update({"Image": "https://image.tmdb.org/t/p/w500" + api_response["poster_path"]})
    length_of_genre = len(api_response["genres"])
    print (length_of_genre)
    list_of_genre = []
    for i in range(length_of_genre):
        list_of_genre.append(api_response["genres"][i]["name"])
    new_list_genre = ", ".join(list_of_genre)
    movie_details.update({"Genre": new_list_genre})
    #print(movie_details)
    return movie_details

def url_api(movie_name):
    session_name = requests.Session()
    url = "https://en.wikipedia.org/w/api.php"
    search_page = movie_name

    PARAMS = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": search_page
    }
    response = session_name.get(url=url, params=PARAMS)
    data = response.json()
    page_id = data['query']['search'][0]['pageid']
    print(json.dumps(data, indent=4))
    url_page = "http://en.wikipedia.org/?curid=" + str(page_id)
    return url_page

app.run()
