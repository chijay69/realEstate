file = "app/countries.csv"


def convert(my_list):
    return tuple(my_list)


def get_country_dict():
    with open(file, "r") as f:
        contents = f.readlines()
        countries = [convert((''.join(item).strip('\n')).split(',')) for item in contents]
        print(countries)
        return countries


get_country_dict()
