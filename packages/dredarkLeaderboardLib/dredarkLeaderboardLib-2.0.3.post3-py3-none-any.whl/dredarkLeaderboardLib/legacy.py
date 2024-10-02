import requests
from bs4 import BeautifulSoup

from .errors import *
from .checks import *


class LegacyLeaderboard():
  """
    This class is used to scrape the Deep Space Airships 
legacy leaderboards (DEPRECATED)
    """

  def __init__(self):
    self.shipData = []
    self.bs4Soup=None
    from warnings import warn
    warn("The LegacyLeaderboard Module has been deprecated, please use the Archive Module.")
    raise DeprecatedModule("LegacyLeaderboard","The LegacyLeaderboard Module is depreciated, please use the ArchiveLeaderboard Module.")

  @linkCheck("legacy")
  def scan_Leaderboard(self, url: str, totalPages=10, limit=None):
    """
        Scrapes the DSA leaderboard provided

        Args:
            url (str): The leaderboard URL to scrape.
            totalPages (int): The total number of pages for the leaderboard. (The number below the table). Default is 10 
            limit (int): Limit of how many ships to retrieve from the page.

        Returns:
            Nothing. The scanned data is stored in the 'shipData' instance variable.
        """
    pageNum=1
    shipCount=0
    ship_info = {}
    currentURL=url
    while pageNum<totalPages:
      response = requests.get(currentURL)
      soup = BeautifulSoup(response.text, 'html.parser')
      self.bs4Soup=soup
      tables=str(soup.find_all("table", {"class": "leaderboard"})).replace("[","").replace("]","").replace('<table class="leaderboard">','').replace("</table>","").replace("<tr>","").replace("<td>","")
      lbEntries=tables.split("</tr>")
      ships=lbEntries
      for ship in ships:
        try:
          rawData = ship.split("</td>")
          rawData.remove("")
          data = rawData
          listEntry={
            "name": data[1],
            "rank": int(data[0].replace("#","")),
            "score": int(data[2].split(" ")[0].replace(",",""))
          }
          self.shipData.append(listEntry)
        except Exception as e:
          pass
      pageNum+=1
      currentURL=f"{url}&p={pageNum}"

  def return_data(self):
    """
        Returns:
            dict : The dictionary of ship data from the 'shipData' instance variable
        """
    return self.shipData

  def fetch_ship(self, searchKey, searchTerm):
    """
        Fetches entries based on the key and term
        Viable Keys: name, rank, points

        Args:
            searchKey (str): Search for an individual ship by `name, rank, points`. 
            searchTerm (str): 

        Returns:
            Nothing. The scanned data is stored in the 'shipData' instance variable.
        """
    viableKeys = ["name", "rank", "score"]
    if searchKey not in viableKeys:
      raise BadSearchKey
    else:

      def scan_data(data, term):
        return list(filter(lambda x: x.get(searchKey) == term, data))

      return scan_data(self.shipData, searchTerm)

  def fetch_ranks(self, start : int,  end : int, startInclusive=True, endInclusive=True):
    """
        Fetches ranks within the designated start-end range.
  
        Args:
            start (int): The rank at the start of the range
            end (int): The rank at the end of the range
            startInclusive: Default is True; if False, the start is not included in the list
            endInclusive: Default is True; if False, the end is not included in the list
  
        Returns:
            A List Of Entries Within The Specified Rank Range
        """
    def scan_data(data):
      if startInclusive and endInclusive:
        return list(filter(lambda x: (x.get("rank") >= start and x.get("rank") <= end) , data))
      elif startInclusive and not endInclusive:
        return list(filter(lambda x: (x.get("rank") >= start and x.get("rank") < end) , data))
      elif endInclusive and not startInclusive:
        return list(filter(lambda x: (x.get("rank") > start and x.get("rank") <= end) , data))
      else:
        return list(filter(lambda x: (x.get("rank") > start and x.get("rank") < end) , data))
  
    return scan_data(self.shipData)
