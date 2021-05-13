from bs4 import BeautifulSoup
import requests
import pandas as pd

#### Recovery of the url of the pages of films newly released in the theaters

url='http://www.allocine.fr/'
r = requests.get(url)
print(url, r.status_code)
soup = BeautifulSoup(r.content,'lxml')

# I notice that the relative link of the web page specific to the new movie on the poster is stored in these tags:

for p in soup.find_all('a'):
    print (p.text)

# In addition to the tag a, which is easily identifiable, we notice some additional
# information such as the value of the class variable of these identical tags.

# Can you retrieve the titles for me via the search for "title" in the items of the previous list?
for elem in soup.find_all('a', attrs={"class" :"meta-title meta-title-link"}):
    print('The tag element is: ', elem)
    print('The link ("href") is: ', elem.get('href'))
    print('The titles are: ', elem.get('title'), "\n")

# Let's start by building the url that we will use to retrieve the summaries
# Start by putting the href values in a list of links
links=[]
# I too ",attrs={"class" :"meta-title meta-title-link"}" out
for elem in soup.find_all('a'):
    # I simply put all of this in a list
    links.append(elem.get('href'))

print('Links of the websites for reviews: ', links)

# The absolute url of the searched movie pages is built in this
# form: http://www.allocine.fr/film/fichefilm_gen_cfilm=243835.html
# It is therefore necessary to repeat the previous list and build the absolute urls for our search
# It's up to you to play.

# NB: Do not take the links for the shows(series)

links_movie=['http://www.allocine.fr'+ elem for elem in links if 'fichefilm' in elem]
print(links_movie)

# Finally, on each page, the title and synopsis must be retrieved. Let's try for a movie, the first of the list

url=links_movie[0]
r = requests.get(url)
print(url, r.status_code)
soup = BeautifulSoup(r.content,'lxml')

for elem in soup.find_all('div', attrs={"class": "titlebar-title titlebar-title-lg"}):
    # Just like that
    print("Title: ", elem.text)

for elem in soup.find_all('div', attrs={"class": "content-txt"}):
    # Just like that
    print("Sipnosis: ", elem.text)

for elem in soup.find_all('meta', property="og:description"):
    # Just like that
    print("Sipnosis: ", elem['content'])

# 1) Automate this script for the entire list
# 2) Put the information in three lists (film_links, title, synopsis)
# 3) Create a dataframe that includes these three informations in three associated columns
# 4) Save this dataframe in a csv file

film_links, title, synopsis = links_movie.copy(), [], []
for link in links_movie:
    r = requests.get(link)
    soup = BeautifulSoup(r.content, 'lxml')

    for elem in soup.find_all('div', attrs={"class": "titlebar-title titlebar-title-lg"}):
        title.append(elem.text)
        print("Title: ", elem.text)

    for elem in soup.find_all('meta', property="og:description"):
        synopsis.append(elem['content'])
        print("Sypnosis: ", elem['content'])
from bs4 import BeautifulSoup
import requests
import pandas as pd

#### Recovery of the url of the pages of films newly released in the theaters

#ussing pandas library
# I check the length of the lists before creating the df
print(len(title),len(synopsis),len(links_movie))
films_allocine = pd.DataFrame(list(zip(film_links, title, synopsis)), columns=['link', 'title', 'sypnosis'])

#You can create a dataframe also like import pandas as pd
#df=pd.DataFrame({'Titre' : titre})
#df['synopsis'] = synopsis
#df['liens'] = liens_film

print(films_allocine.get('title'))
films_allocine.to_csv("allo_cine.csv", index=False)

films_allocine2 = list(zip(film_links, title, synopsis))
print(films_allocine2)

with open("allo_cine2.csv", "w", encoding='utf-8') as data_file:
    for elem in films_allocine2:
        data_file.write(",".join(elem) + '\n')


# And here's your first real scrap, you're real hackers now.