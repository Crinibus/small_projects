import json
import questionary
import data as dt


def read_wishlist(filename: str) -> dict:
    with open(filename, 'r') as json_file:
        data = json.load(json_file)
    return data


def get_super_categories(data: dict) -> list:
    temp = []
    for super_cat in data.keys():
        temp.append(super_cat)
    return temp


def get_sub_categories(data: dict, super_category: str) -> list:
    temp = []
    for sub_cat in data[super_category]:
        temp.append(sub_cat)
    return temp


def get_links(data: dict, super_category: str, sub_category: str) -> list:
    temp = []
    for link in data[super_category][sub_category]:
        temp.append(link)
    return temp


# if __name__ == '__main__':
#     data = read_wishlist('wishlist.json')
#     super_cat = questionary.select("Select a category:", choices=get_super_categories(data)).ask()
#     sub_cat = questionary.select("Select a sub category:", choices=get_sub_categories(data, super_cat)).ask()
    
#     print()
#     for index, link in enumerate(get_links(data, super_cat, sub_cat)):
#         print(f"{index + 1} > {link}")

def show_all_data(data: dt.Data):
    for superCategory in data.categories:
        print(f"\nSuper category: {superCategory.name}")
        for subCategory in superCategory.sub_categories:
            print(f"\tSub category: {subCategory.name}")
            for product in subCategory.products:
                print(f"\t\t{product.link}")


def main():
    my_data = dt.Data('wishlist.json')

    show_all_data(my_data)    


if __name__ == '__main__':
    main()
