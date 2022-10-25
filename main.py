# -*- coding: utf-8 -*-
import certifi
import random
import urllib3
from itertools import chain

class CommonMovies():

  def __init__(self):
    print("""
      Welcome to the Letterboxd Common Movies Tool.
      This tool will generate a list of common movies between two or more Letterboxd users. 
      Please enter the usernames of the two or more users you wish to compare, and press enter 
      or type 'done' when you have entered them all.
    """)

    self.movies = []
    usernames = self.getUserNames()

    for user in usernames: 
      page_num = self.getNumPagesInWatchlist(user)
      movies = self.getUserMovies(user, page_num)
      self.movies.append(movies)

    self.random_movie = self.getRandomMovie()
    self.result = self.getCommonMovies()
    self.printResults()
    
  def getUserNames(self):
    usernames, done = [], False
    while not done: 
      user = input("Enter a Letterboxd username or press enter when done: ")
      if user == "" or user == "done":
        if len(usernames) == 1:
          print("Warning: You must enter at least two usernames.")
        else:
          done = True
      elif user in usernames:
        print(f"Info: {user} already added.")
      else:
        usernames.append(user.strip())
    print(f"\nFinding common movies for {', '.join(usernames)}")
    return usernames

  def getNumPagesInWatchlist(self, username):
    userpage = http.request('GET', f"https://letterboxd.com/{username}/watchlist/page/1/")
    userpage_html = userpage.data.decode("utf-8")
    page_num = 1
    while "\n" in userpage_html:
      userpage_html = userpage_html.split("\n")      
    for line in userpage_html:
      if "paginate-current" in line:
        pos = line.find("paginate-current") + len("paginate-current")
        if line.find("page/3", pos) == -1:
          page_num = 2
        else:
          page_pos = line.find("page/3", pos) + len("page/3")
          if line.find("page/", page_pos) != -1:
            reduced = line[line.find("page/", page_pos) + len("page/"):]
            page_num = int(reduced.split("/")[0])
          else:
            page_num = 3
    return page_num

  def getUserMovies(self, username, page_num):
    print(f"Going through {username}'s watchlist...")   
    lst = []  
    for page in range(1, page_num + 1):
      watchlist = http.request('GET', f"https://letterboxd.com/{username}/watchlist/page/{page}/")
      watchlist_html = watchlist.data.decode("utf-8")
      while "\n" in watchlist_html:
        watchlist_html = watchlist_html.split("\n")
      for line in watchlist_html:
        if "film-poster" in line:
          film_start = line.find("alt=") + len("alt=")
          film_end = line.find("/>", film_start)
          try:
            lst.append(line[film_start:film_end]) 
          except:
            break
    return lst

  def getRandomMovie(self):
    allMovies = list(chain.from_iterable(self.movies))
    return random.choice(allMovies).replace('"', '')

  def getCommonMovies(self):
    result = set(self.movies[0]) 
    for s in self.movies[1:]:
      result.intersection_update(s)
    return result

  def printResults(self):
    length = len(self.result) 
    if length > 0:
      print(f"\nGood news! These users have {length} film(s) in common!")
      print('\nHere they are:')
      for idx, film in enumerate(self.result):
        film = film.replace("\\", "'").replace('"', '')
        print(f"{idx+1}: {film}")
    else:
      print(f"\nSorry! These users have no films in common!\n")

    print(f"\nFeeling lucky? Watch {self.random_movie}!\n")

if __name__ == '__main__':
  http = urllib3.PoolManager(ca_certs=certifi.where())
  CommonMovies()
