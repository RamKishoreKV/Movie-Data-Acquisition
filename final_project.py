#set up api token
import requests
import time
from bs4 import BeautifulSoup
import json

def get_plot(page_soup):
    full_plot = ""
    headers = page_soup.find_all('h2')
    for header in headers:
        if header['id'] == "Plot":
            paragraphs = header.find_next_siblings(['p'])
            for paragraph in paragraphs:
                full_plot += paragraph.getText()
                full_plot += "\n"
    return full_plot

def get_wiki_features(page_soup, wiki_fields, movie, movie_id): #parse table from wikipedia
    verify_movie = str(page_soup).lower()
    elementsToAdd = []
    if "film" in verify_movie or "movie" in verify_movie:
        table = page_soup.find('table')
        try:
            for row in table.find_all('tr'):
                if row.find('th'):
                    th = row.find('th')
                    if th.getText().strip() in wiki_fields:
                        if row.find('td'):
                            td = row.find('td')
                            if td.getText():
                                elementsToAdd.append([th.getText().replace("\n", ""), td.getText()])
                            else:
                                if td.find('a'):
                                    a = td.find('a')
                                    elementsToAdd.append([th.getText().replace("\n", ""), a.getText().replace("\n", "")])
        except AttributeError as attr_error:
            pass
    elementsToAdd.append(['Plot', get_plot(page_soup)]) #Add plot here too
    return wiki_dict(elementsToAdd, movie, movie_id)

def wiki_dict(wiki_features, movie, movie_id):
    key = {"Directed by": 'director', "Screenplay by": 'screenplay', "Produced by": 'producers', "Starring": 'starring', "Country": 'country', "Language": 'language', "Budget": 'budget', "Box office": 'box_office', "Countries": 'country', "Running time": 'runtime', "Plot": 'plot'}
    movie_wiki_dict = {}
    numerical_items = ["Budget", "Box office", "Running time"] #needs to be parsed differently
    list_items = ["Countries", "Starring", "Produced by", "Screenplay by", "Directed by"] #needs to be parsed differently
    for feature in wiki_features:
        if feature[0] in list_items:
            movie_wiki_dict.update({key[feature[0]]: feature[1].strip().split("\n")})
        else:
            feature[1] = feature[1].replace("\n", "")
            if feature[0] in numerical_items:
                feature[1] = parse_numerical(feature[0], feature[1], movie, movie_id)
            if feature[0] == "Country":
                feature[1] = [feature[1]]
            movie_wiki_dict.update({key[feature[0]]: feature[1]})
    print(movie_wiki_dict)
    return movie_wiki_dict

def parse_numerical(feature, value, movie, movie_id):
    try:
        value = value.split(' (')[0]
        money = value.split('[')[0]
        if '\xa0' in money:
            money_amount = money.split('\xa0')
        else:
            money_amount = money.split(' ')

        if '–' in money_amount[0]:
            format_money = money_amount[0].replace('$', '').split('–')
        else:
            format_money = money_amount[0].replace('$', '').split('-')

        #format_money = format_money[0].replace('+', '')
        if len(format_money) > 1:
            format_money = (float(format_money[0]) + float(format_money[1])) / 2
        else:
            format_money = [format_money[0].replace(',', '')] #handles the case if its in the thousands
            format_money = float(format_money[0])
        if len(money_amount) > 1:
            if money_amount[1] == 'million':
                format_money *= 1000000
                return format_money
            elif money_amount[1] == 'billion':
                format_money *= 1000000000
                return format_money
            elif money_amount[1] == 'minutes': #for running time, variables named oddly, could change this
                return format_money
    except ValueError:
        data = get_api_data(movie_id)
        if feature[0] == 'Budget':
            return data['budget']
        elif feature[0] == 'Box office':
            return data['revenue']
        else:
            return data['runtime']
    
def get_api_data(movie_id):
    headers = {
        "accept": "application/json",
        "Authorization": "xxxxxx"
    }
    movie_data_url = "https://api.themoviedb.org/3/movie/" + str(movie_id) + "?language=en-US"
    response = requests.get(movie_data_url, headers=headers)
    if response.status_code == 200:
        try:
            return response.json()
        except requests.exceptions.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")

def get_release_year(movie_id):
    data = get_api_data(movie_id)
    year = data['release_date'].split('-')[0]
    return year

def get_api_features(movie_id):
    data = get_api_data(movie_id)
    if data is not None:
        api_genres = data['genres']
        genres = []
        for genre in api_genres:
            genres.append(genre['name'])

        features = {
            'vote_average': data['vote_average'],
            'vote_count': data['vote_count'],
            'overview': data['overview'],
            'release_date': data['release_date'],
            'runtime': data['runtime'],
            'genres': genres
        }
        return features
    else:
        return {}
    

api_read_access_token = "xxxxx"
api_key = "xxxxxxx"
url = "https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=1&primary_release_date.gte=2010-01-01&release_date.gte=2010-01-01&sort_by=popularity.desc&vote_count.gte=100&with_original_language=en"

headers = {
    "accept": "application/json",
    "Authorization": "xxxxxxxx",}

start_time = time.time()
response = requests.get(url, headers=headers)
num_pages = int(response.json()['total_pages'])
data = response.json()
#Ran into a problem going 500+ pages

API_path = "https://en.wikipedia.org/api/rest_v1/"
wiki_fields = ["Directed by", "Screenplay by", "Produced by", "Starring", "Country", "Language", "Budget", "Box office", "Countries", "Running time"] #TODO: parse budget/box office amount, if theres a - in the middle, pick one, turn million into int

all_movies = []
for i in range(1, num_pages+1):
    try:
        url = "https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=" + str(i) + "&primary_release_date.gte=2010-01-01&release_date.gte=2010-01-01&sort_by=popularity.desc&vote_count.gte=100&with_original_language=en"
        response = requests.get(url, headers=headers)
        data = response.json()['results']

        for row in data:
            all_movies.append((row['title'], row['id']))
    except KeyError:
        print("Error: 'results' key not found in the response for page", str(i))

#Wikipedia Web Scraping
API_path = "https://en.wikipedia.org/api/rest_v1/"
count = 0
no_wiki = []
wiki_fields = ["Directed by", "Screenplay by", "Produced by", "Starring", "Country", "Language", "Budget", "Box office", "Countries"] #TODO: parse budget/box office amount, if theres a - in the middle, pick one, turn million into int

#Debugging/Testing on a single movie down commented out

"""
movie = "Oppenheimer"
wikipedia_movie = "Oppenheimer_(film)"
page_title = movie.replace(" ", "_")
url = API_path + "page/html/" + page_title
page_response = requests.get(url)
page_soup = BeautifulSoup(page_response.content, "html.parser")
print(page_soup)
movie_id = 1 #not the real movie ID, this was primary to test Wikipedia scraping
features = get_wiki_features(page_soup, wiki_fields, movie, movie_id)
print(features)
"""

movie_dicts = []
for i, (movie, movie_id) in enumerate(all_movies):#[:30]:
    print(i, movie)
    page_title = movie.replace(" ", "_")
    url = API_path + "page/html/" + page_title
    page_response = requests.get(url)
    page_soup = BeautifulSoup(page_response.content, "html.parser")

    wiki_features = get_wiki_features(page_soup, wiki_fields, movie, movie_id)

    if len(wiki_features) <= 1: #if wrong title of wiki page, try new page with _(film)
        page_title = movie.replace(" ", "_") + "_(film)"
        url = API_path + "page/html/" + page_title
        page_response = requests.get(url)
        page_soup = BeautifulSoup(page_response.content, "html.parser")
        wiki_features = get_wiki_features(page_soup, wiki_fields, movie, movie_id)

    if len(wiki_features) <= 1:
        release_year = get_release_year(movie_id)
        page_title = movie.replace(" ", "_") + "_(" + release_year + "_film)"
        url = API_path + "page/html/" + page_title
        page_response = requests.get(url)
        page_soup = BeautifulSoup(page_response.content, "html.parser")
        wiki_features = get_wiki_features(page_soup, wiki_fields, movie, movie_id)
        
    page_title = movie.replace(" ", "_") #reset page_title so it doesn't have the _film in the key, could make it weird

    #combine wiki features with the api features
    api_features = get_api_features(movie_id)
    finalDict = {}
    finalDict.update(wiki_features)
    finalDict.update(api_features)

    movie_dicts.append({page_title.lower(): finalDict})

file_path = 'all_movies.json'
# Open the file in write mode and use json.dump with indent
with open(file_path, 'w') as json_file:
    json.dump(movie_dicts, json_file, indent=4)

print("ALL MOVIES:", len(all_movies))

print("NO TABLE FOUND ON WIKIPEDIA:", count)
print("NO WIKIPEDIA", no_wiki)
end_time = time.time()
print("RUNTIME:", end_time - start_time)

"""
TODO: Abstract function to grab features from the Wikipedia table, put into some data structure, parse the data (an hour or two)
TODO: Build out dictionary for each movie under the for loop (15 mins)
TODO: Try for different URL links appending the _(film) and _(YEAR_film) - find how to check which is the right return value (30 mins)
TODO: Figure out what other fields I want from TMDB/Wikipedia - genres from TMDB (an hour)

TODO: Country is either single element or a list, make this a list universally

TODO: Some small analysis - which genre made the most per movie, which actor had the biggest impact/ratings (add revenue/ratings, divide by num movies they're in), directors who made the best ratings/money, does ratings = money?. (hour or so) 

TODO: Ask prof if this is valid and extensive enough
TODO: How to store this?
TODO: Constraints on runtime? Reporting runtime?

TODO: If I get bored and want to add more - add a description for each genre


Wikipedia: Directors, Starring, Budget, Plot, Runtime, Revenue
TMDB: Title, Genres, Overview, Release Date, Vote Average, Vote Count

"""