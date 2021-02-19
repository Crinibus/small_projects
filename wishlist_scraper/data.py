import json
import requests


class Data:
    def __init__(self, filename: str) -> None:
        self.filename = filename
        self.data = Data.read_json(filename)
        self.categories = []
        self.format_data()

    @staticmethod
    def read_json(filename: str) -> dict:
        with open(filename, 'r') as json_file:
            data = json.load(json_file)
        return data
    
    def format_data(self):
        # for category in self.data.keys():
        #     self.categories.update({category: []})
        
        #     for sub_category in self.data[category]:
        #         self.categories[category].append(SubCategory(sub_category, self.data[category][sub_category]))
        
        for category in self.data.keys():
            self.add_category(category, self.data[category])

    def add_category(self, name: str, info: dict):
        new_category = SuperCategory(name, info)
        self.categories.append(new_category)


class SuperCategory:
    def __init__(self, name: str, info: dict) -> None:
        self.name = name
        self.info = info
        self.sub_categories = []
        self.format_info()
    
    def format_info(self):
        for sub_cat in self.info:
            self.add_sub_category(sub_cat, self.info[sub_cat])
    
    def add_sub_category(self, name: str, info: dict):
        new_sub_category = SubCategory(name, info)
        self.sub_categories.append(new_sub_category)

class SubCategory:
    def __init__(self, name: str, info: dict) -> None:
        self.name = name
        self.info = info
        self.products = []
        self.format_info()

    def format_info(self):
        for link in self.info:
            self.add_product(link)

    def add_product(self, link: str):
        new_product = Product(link)
        self.products.append(new_product)
    
    def __str__(self) -> str:
        return f"SubCategory(category_name={self.name}, category_info={self.info}"


class Product:
    def __init__(self, link: str) -> None:
        self.link = link

    def get_info_link(self):
        pass

