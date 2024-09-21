from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import re
import json
import requests

class AuroraParser:
    service = Service(ChromeDriverManager().install())
    URL = "https://www.swpc.noaa.gov/communities/aurora-dashboard-experimental"

    def __init__(self, wind_speed, const_distance):
        self.driver = webdriver.Chrome(service=AuroraParser.service)
        self.wind_speed = wind_speed
        self.const_distance = const_distance

    def get_source_code(self) -> None:
        self.driver.get(AuroraParser.URL)

        while True:
            try:
                e = self.driver.find_element(By.ID, "WindSpeed")
                self.wind_speed = float(e.text)
                e2 = self.driver.find_element(By.ID, "Flux")
                e3 = self.driver.find_element(By.ID, "Bt")
                e4 = self.driver.find_element(By.ID, "Bz")
                e5 = self.driver.find_element(By.XPATH, "/html/body/div[4]/section/div/div/div/div/section[1]/div/div/div[1]/div[4]/div[1]/div/div[2]/div[4]/div[1]")

                p = requests.get("https://services.swpc.noaa.gov/products/noaa-planetary-k-index.json")
                Kp = json.loads(p.text)
                with open("Kp.txt", "w") as l:
                    l.write(str(Kp))
                with open("Kp.txt", "r") as l:
                    text = l.read()
                    pattern = r"\d+\.\d+"
                    numbers = re.findall(pattern, text)
                    if numbers:
                        last_number = numbers[-1]
                        with open("parameters.txt", "w") as a:
                            a.write("Solar Wind Speed: " + str(self.wind_speed) + " km/s" + "\n")
                            a.write("Flux: " + e2.text + " sfu" + "\n")
                            a.write("Bt: " + e3.text + " nT" + "\n")
                            a.write("Bz: " + e4.text + " nT" + "\n")
                            a.write("Storm: " + e5.text + " " "\n")
                            a.write(f"Kp: {last_number}" + "\n")
                            a.write("\n" + "Time to Earth: " + str(round(self.const_distance / self.wind_speed, 1)) + " minutes" + "\n")

                break
            except TimeoutException as _ex:
                print(_ex)
                break

        with open("parameters.txt", "r") as b:
            for line in b:
                location_vars = {"Storm: G ":65, "G1":60, "G2":55, "G3":50, "G4":45, "G5":40}
                for loc_var in location_vars.keys():
                    if loc_var in line:
                        with open("parameters.txt", "a", encoding="utf-8") as b:
                            b.write(f"Location: north to {location_vars[loc_var]}" + "°" + "\n")

        with open("parameters.txt", "r", encoding="utf-8") as c:
            content = c.read()
            with open("parameters.txt", "a", encoding="utf-8") as c:
                if re.search(r"[G]\d+", content):
                    c.write("Visibility: YES when Bz < 0" + "\n")
                elif re.search(r"-\d{1}", content):
                    c.write("Low chance to see aurora 😾")
                elif re.search(r"(-1[0-9]|-19)", content):
                    c.write("Good chance to see aurora 😺")
                elif re.search(r"(-[2-9][0-9]|-100)", content):
                    c.write("WOW! High chance to see aurora! 🙀")
                else:
                    c.write("Visibility: NO 😿 (G = 0, Bz ≥ 0)")