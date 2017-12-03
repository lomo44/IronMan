from bs4 import BeautifulSoup
from urllib.request import Request,urlopen
from enum import Enum
import pprint
import json
class marvel_hero_name(Enum):
    eMarvel_Hero_Iron_Man = 0
    eMarvel_Hero_Captain_America = 1

def get_marvel_basic_info(hero_name:marvel_hero_name):
    marvel_url = ''
    if hero_name == marvel_hero_name.eMarvel_Hero_Iron_Man:
        marvel_url = "http://marvel.wikia.com/wiki/Anthony_Stark_(Earth-616)"
    elif hero_name == marvel_hero_name.eMarvel_Hero_Captain_America:
        marvel_url = "http://marvel.wikia.com/wiki/Steven_Rogers_(Earth-616)"
    return_dict = {}
    if marvel_url != '':
        hdr = {'User-Agent': 'Mozilla/5.0'}
        req = Request(marvel_url, headers=hdr)
        page = urlopen(req)
        soup = BeautifulSoup(page.read(),"html.parser")
        l2_f = soup.find_all('div', {'class': 'pi-item pi-data pi-item-spacing pi-border-color'})
        return_dict = {}
        for item in l2_f:
            label = item.find('h3', {'class': 'pi-data-label pi-secondary-font'}).text
            value = item.find('div', {'class': 'pi-data-value pi-font'})
            sub_tag = value.find_all('sup')
            for tag in sub_tag:
                tag.extract()
            if label not in return_dict:
                return_dict[label.strip()] = []
            return_dict[label.strip()] += list(map(lambda x:x.strip(),value.text.strip().split(',')))
    return return_dict


if __name__ == "__main__":
    iron_man_info = get_marvel_basic_info(marvel_hero_name.eMarvel_Hero_Captain_America)
    pprint.pprint(iron_man_info,indent=4)
    with open("data\Captain_America.json","w") as file:
        json.dump(iron_man_info,file, sort_keys=True, indent=4)
