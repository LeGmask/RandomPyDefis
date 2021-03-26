import requests
from typing import List
from bs4 import BeautifulSoup

class Callicode:
    def __init__(self, config) -> None:
        self.config = config.CALLICODE

    def getChallenges(self) -> List:
        """
        Get all the accessible pydefis challenges

        Returns:
            List: list of dict for each challenges such as:
                {
                    "level": the difficulty level,
                    "name": challenge name,
                    "url": challenge url,

                }
        """
        req = requests.get("https://pydefis.callicode.fr/user/liste_defis")
        soup = BeautifulSoup(req.text, "html.parser")

        challenges = [challenges.find_all("td") for challenges in soup.find("tbody").find_all("tr")]
        return [{
            "level": defis[2].find("img").get("src")[13:14],
            "name": defis[3].text[21:],
            "url": f"{self.config.baseURL}{defis[3].find('a').get('href')}",
        } for defis in challenges]
    
    def filter(self, challenges, level="all", name="all"):
        filteredChallenges = []

        if name == "all" and "level" == "all":
                return challenges

        for challenge in challenges:
            if level != "all":
                if int(challenge["level"]) == int(level):
                    filteredChallenges.append(challenge)

            if name != "all":
                if str(name) in str(challenge["name"]).lower():
                    filteredChallenges.append(challenge)

        return filteredChallenges
