from Helper import *
import time

class Spider:
    def __init__(self, Url, urlStarter):
        self.Url = Url
        self.urlStarter = urlStarter
        self.helper = Helper()
        self.soup = self.helper.getSoup(Url)


    def processData(self):
        self.provinceList = []
        province_table = self.soup.find("table", {"class", "provincetable"})
        province_list = province_table.find_all("a")
        # for province in province_list:
        #     province_dist = {}
        #     province_dist["name"] = province.get_text()
        #     province_dist["href"] = province.get("href")
        #     province_dist["parent"] = "null"
        #     province_dist["child"] = self.processDataRecursively(province_dist["href"], province_dist["name"])
        #     self.provinceList.append(province_dist)

        #lets only get ZJ province for speed.
        province_dist = {}
        province = province_list[10]
        province_dist["name"] = province.get_text()
        province_dist["parent"] = "null"
        province_dist["children"] = self.processDataRecursively(province.get("href"), province_dist["name"])
        self.provinceList.append(province_dist)

    def processDataRecursively(self, href, parent):
        print(parent)
        childList = []
        url = self.urlStarter+href
        soup = self.helper.getSoup(url)

        #If in village page, finish the recursive
        village_tables = soup.find_all("table", {"class", "villagetable"})
        if len(village_tables)>0:
            village_table = village_tables[0]
            village_tr_list = village_table.find_all("tr", {"class", "villagetr"})
            for village_tr in village_tr_list:
                village_dist = {}
                village_name = village_tr.find_all("td")[-1].get_text()
                village_dist["name"] = village_name
                village_dist["parent"] = parent
                village_dist["children"] = []
                childList.append(village_dist)
            return childList

        #In city page
        city_tables = soup.find_all("table", {"class", "citytable"})
        if len(city_tables)>0:
            city_table = city_tables[0]
            city_tr_list = city_table.find_all("tr", {"class", "citytr"})
            for city_tr in city_tr_list:
                city_dist = {}
                city_a = city_tr.find_all("a")[-1]
                city_dist["name"] = city_a.get_text()
                city_dist["parent"] = parent
                city_dist["children"] = self.processDataRecursively(city_a.get("href"), city_dist["name"])
                childList.append(city_dist)
            return childList

        #In county page
        county_tables = soup.find_all("table", {"class", "countytable"})
        if len(county_tables)>0:
            county_table = county_tables[0]
            county_tr_list = county_table.find_all("tr", {"class", "countytr"})
            #mention SXQ
            for county_tr in county_tr_list[1:]:
                county_dist = {}
                county_a = county_tr.find_all("a")[-1]
                county_dist["name"] = county_a.get_text()
                county_dist["parent"] = parent
                county_dist["children"] = self.processDataRecursively(county_a.get("href"), county_dist["name"])
                childList.append(county_dist)
            return childList

        #In town page
        town_tables = soup.find_all("table", {"class", "towntable"})
        if len(town_tables)>0:
            town_table = town_tables[0]
            town_tr_list = town_table.find_all("tr", {"class", "towntr"})
            for town_tr in town_tr_list:
                town_dist = {}
                town_a = town_tr.find_all("a")[-1]
                town_dist["name"] = town_a.get_text()
                town_dist["parent"] = parent
                town_dist["children"] = self.processDataRecursively(town_a.get("href"), town_dist["name"])
                childList.append(town_dist)
            return childList

        return childList