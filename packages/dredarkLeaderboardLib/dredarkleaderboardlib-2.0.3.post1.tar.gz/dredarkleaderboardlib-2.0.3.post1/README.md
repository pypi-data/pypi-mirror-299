# dredarkLeaderboardLib
Dredark Leaderboard Library for Python!  
The library contains functions to fetch data from the Deep Space Airships (drednot.io) leaderboard pages.

Current Verison: 2.0.2

**Usage of This Library to Violate the Deep Space Airships Terms of Service Is Not Allowed**

Base Example:
``` python
import src.dredarkLeaderboardLib as dll

URL="https://drednot.io/leaderboard/?cat=boss_shield&by=pilot"
PER_PAGE_LIMIT=10 # Fetches the first 10 leaderboard entries on each page
TOTALPAGES=10 # Only reads from the first 10 pages
statistics=dll.Leaderboard() # Initiates the Leaderboard Object
statistics.scan_Leaderboard(URL, TOTALPAGES, PER_PAGE_LIMIT) # Scrapes the provided URL and stores the data
print(statistics.shipData) # Prints the scrapped data
#Or
print(statistics.return_data()) # Alternative Method to print data
print(statistics.fetch_ship("rank",10)) # Prints the entry at rank 10
print(statistics.fetch_ranks(1,10,True,True)) # Fetches Ranks 1-10 (1 & 10 are Included)
print(statistics.fetch_ranks(1,10,True,False)) # Fetches Ranks 1-10 (10 is exclusive, so only ranks 1-9 are actually returned)
print(statistics.fetch_ranks(1,10,False,True)) # Fetches Ranks 1-10 (1 is exclusive, so only ranks 2-10 are actually returned)
print(statistics.fetch_ranks(1,10,False,False)) # Fetches Ranks 1-10 (1 & 10 are exclusive, so only ranks 2-9 are actually returned)```
