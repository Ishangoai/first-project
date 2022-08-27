""" Scrpes https://ev-database.org/#sort:path~type~order=.rank~number~desc|range-slider-range:prev~next=0~1200|range-slider-acceleration:prev~next=2~23|range-slider-topspeed:prev~next=110~450|range-slider-battery:prev~next=10~200|range-slider-towweight:prev~next=0~2500|range-slider-fastcharge:prev~next=0~1500|paging:currentPage=0|paging:number=all
for car specifications """
import requests
from bs4 import BeautifulSoup as bs
import bs4
from typing import List, Tuple
import pandas as pd


class WebParser:
    def __init__(self, url: str) -> None:
        self.url = url

    def _web_parser(self) -> bs4.element.ResultSet:
        """ returns beautiful object """
        web_page = requests.get(self.url)
        soup = bs(web_page.content, 'html.parser')

        return soup

    @property
    def get_web_parser(self):
        """ a public fxn for _web_parser"""
        return self._web_parser()

    @staticmethod
    def _read_tags(soup_parser: bs4.element.ResultSet) -> bs4.element.ResultSet:
        """
        Parameter:
            soup_parser : bs4.element.ResultSet

        Reads 'div' tag with 'class:list-item, for each car data

        Return:
            cars_info : bs4.element.ResultSet
        """
        cars_info = soup_parser.find_all("div", {"class": "list-item"})
        return cars_info

    def get_single_car_info(self, single_car_info: bs4.element.ResultSet) -> List:
        """
        Parameter:
        single_car_info: (bs4.element.ResultSet) 
        A single car information

        Reads the following information of a single car and converts to a DataFrame:
        car_img_url, car_name,car_battery ,towWeight, mktSeg, nosSeat, acceleration, 
        topSpeed, range, efficiency, fastcharge, de_price, nl_price, uk_price

        Return:
        single_car_info_df :(pd.DataFrame)
        """
        car_img_url = self.get_car_img(single_car_info)
        car_name,car_battery = self.get_car_name_battery(single_car_info)
        towWeight, mktSeg, nosSeat, drive_type= self.get_towWeight_mktSeg_nosSeat_drive_type(
            single_car_info)
        acceleration, topSpeed, range, efficiency, fastcharge = self.get_car_specs(
            single_car_info)
        de_price, nl_price, uk_price = self.get_car_price(single_car_info)
        single_car_info = [car_img_url, car_name, car_battery, towWeight, mktSeg, nosSeat, drive_type, acceleration,
                           topSpeed, range, efficiency, fastcharge, de_price, nl_price, uk_price]
        single_car_info_df = self.list2dframe(single_car_info)
        return single_car_info_df
    @staticmethod
    def list2dframe(list_obj):
        """
        Parameter:
        list_obj : (list)
        converts a list object to dataframe

        Return:
        df : pd.DataFame
        """
        df = pd.DataFrame(columns=["Car_img_url", "Name", "Battery","Tow_Weight", 
        "Market_Segment", "Number_of_Seat","DriveTrain" ,"Acceleration","Speed", "Range", "Efficiency", 
        "Fastcharge", "Germany_price", "Netherland_price", "Uk_price"])
        df.at[1,:] = list_obj
        return df

    @staticmethod
    def get_car_img(car_info: bs4.element.ResultSet) -> str:
        """
        Parameter:
            car_info : bs4.element.ResultSet
            
        reads img tag and returns link to car image

        """
        meta_data = car_info.find("div", {"class": "img"})
        car_img = meta_data.find(href=True)
        car_img = "https://ev-database.org"+str(car_img['href'])
        return car_img

    @classmethod
    def get_car_name_battery(cls,car_info) -> Tuple[str, str]:
        """
        Parameter:
        car_info: (bs4.element.ResultSet) 
        A single car information

        finds tags that store data on the following of a single car:
        1. Car Name -> car_name (str)
        2. Car Battery -> car_battery (str)

        Return :
        car_name, car_battery : Tuple(str, str)
        """
        meta_data = car_info.find("div", {"class": "title-wrap"})
        car_name = cls.get_car_name(meta_data)
        car_battery = cls.get_car_battery(meta_data)
        return car_name, car_battery

    @staticmethod
    def get_car_name(meta_data : bs4.element.Tag)-> str:
        """ gets name of a car """
        meta_data_car_name = meta_data.find_all("span")
        meta_data_car_name = meta_data_car_name[:2]
        car_name =  f"{meta_data_car_name[0].text} {meta_data_car_name[1].text}"
        return car_name
    @staticmethod
    def get_car_battery(meta_data : bs4.element.Tag)-> str:
        """ gets battery capacity of a car"""
        meta_battery = meta_data.find("div", {"class": "subtitle"})
        meta_battery = meta_battery.text.strip()
        meta_battery = meta_battery.replace("\n", '')
        meta_battery = meta_battery.replace("\t", '')
        car_battery = meta_battery.replace("*", '')
        return car_battery

    @staticmethod
    def get_towWeight_mktSeg_nosSeat_drive_type(car_info: bs4.element.ResultSet) -> Tuple[str, str, str]:
        """
        Parameter:
        car_info: (bs4.element.ResultSet) 
        A single car information

        finds tags that store data on the following of a single car:
        1. Tow Weight in Kg -> towWeight (str)
        2. Market Segment -> mktSeg (str)
        3. Number of Seats -> nosSeat (str)

        Return :
        towWeight, mktSeg, nosSeat : Tuple(str,str,str)
        """
        meta_data = car_info.find("div", {"class": "icons"})
        towWeight = meta_data.find("span", {"class": "towweight"})
        towWeight = towWeight.text
        mktSeg = meta_data.find("span", {"title": "Market Segment"})
        mktSeg = mktSeg.text
        nosSeat = meta_data.find_all("span", {"title": "Number of seats"})
        nosSeat = nosSeat[1].text
        drive_type = None
        if meta_data.find("span",{"title":"All Wheel Drive"}):
            drive_type = "All Wheel Drive"
        elif meta_data.find("span",{"title":"Rear Wheel Drive"}):
            drive_type = "Rear Wheel Drive"
        elif meta_data.find("span",{"title":"Front Wheel Drive"}):
            drive_type = "Front Wheel Drive"

        return towWeight, mktSeg, nosSeat , drive_type

    @staticmethod
    def get_car_specs(car_info: bs4.element.ResultSet) -> Tuple[str, str, str, str, str]:
        """
        Parameter:
        car_info: (bs4.element.ResultSet) 
        A single car information

        finds tags that stores data on car specification:
        1. Acceleration -> acceleration (str)
        2. Speed -> topSpeed (str)
        3. Range -> range (str)
        4. Efficiency -> efficiency (str)
        5. Fastcharge -> fastcharge (str)

        Return:
        acceleration, topSpeed, range, efficiency, fastcharge : Tuple(str, str, str, str, str)
        """
        meta_data = car_info.find("div", {"class": "specs"})
        acceleration = meta_data.find("span", {"class": "acceleration"}).text
        topSpeed = meta_data.find("span", {"class": "topspeed"}).text
        range = meta_data.find("span", {"class": "erange_real"}).text
        efficiency = meta_data.find("span", {"class": "efficiency"}).text
        fastcharge = meta_data.find("span", {"class": "fastcharge_speed_print"}).text
        return acceleration, topSpeed, range, efficiency, fastcharge

    @staticmethod
    def get_car_price(car_info: bs4.element.ResultSet) -> Tuple[str, str, str]:
        """
        Parameter:
        car_info: (bs4.element.ResultSet) 
        A single car information

        finds price of car in Germany, Netherland, and UK

        Return:
        de_price, nl_price, uk_price : (Tuple) 
        de_price : price in Germany
        nl_price : price in Netherland
        uk_price : price in UK
        """
        meta_data = car_info.find("div", {"class": "pricing align-right"})
        de_price = meta_data.find("span", {"class": "country_de"}).text
        nl_price = meta_data.find("span", {"class": "country_nl"}).text
        uk_price = meta_data.find("span", {"class": "country_uk"}).text
        return de_price, nl_price, uk_price

    def get_cars_info(self) -> pd.DataFrame:
        """ 
        Reads all website data for list-item tags and selects data of interest for each car,
        and merges all data into a single Dataframe.
        Return:
        all_cars_dframe : pd.DataFrame
        """
        soup = self._web_parser()
        cars_info = self._read_tags(soup)
        all_cars = []
        for car_info in cars_info:
            single_car_info_df = self.get_single_car_info(car_info)
            all_cars.append(single_car_info_df)

        all_cars_dframe = pd.concat(all_cars)
        return all_cars_dframe


if __name__ == "__main__":
    obj = WebParser("https://ev-database.org/#sort:path~type~order=.rank~number~desc|range-slider-range:prev~next=0~1200|range-slider-acceleration:prev~next=2~23|range-slider-topspeed:prev~next=110~450|range-slider-battery:prev~next=10~200|range-slider-towweight:prev~next=0~2500|range-slider-fastcharge:prev~next=0~1500|paging:currentPage=0|paging:number=all")
    evCarsdata = obj.get_cars_info()
    print(evCarsdata.head())
