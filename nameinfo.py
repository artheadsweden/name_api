import requests
import json
import calendar

base_urls = {
    "age_api": "https://api.agify.io",
    "gender_api": "https://api.genderize.io",
    "nat_api": "https://api.nationalize.io",
    "country_api": "https://restcountries.eu/rest/v2/alpha/",
    "namesday_api": "https://api.abalin.net/get/getdate"
}


class NameInfo:
    def __init__(self, name):
        self.__name = name
        self.__age = self.__get_age()
        self.__gender = self.__get_gender()
        self.__countries = self.__get_nationalities()
        self.__name_days = self.__get_name_days()

    @staticmethod
    def api_lookup(url):
        return json.loads(requests.get(url).text)

    def __get_age(self):
        return self.api_lookup(base_urls['age_api'] + "?name=" + self.__name)['age']

    def __get_gender(self):
        return self.api_lookup(base_urls['gender_api'] + "?name=" + self.__name)['gender']

    def __get_nationalities(self):
        nationalities = self.api_lookup(base_urls['nat_api'] + "?name=" + self.__name)
        country_ids = [country['country_id'] for country in nationalities['country']]
        country_names = self.api_lookup(base_urls['country_api'] + "?codes=" + ";".join(country_ids))

        return [country['name'] for country in country_names]

    def __get_name_days(self):
        names_day_countries = ["us", "cz", "sk", "pl", "fr", "hu", "hr", "se", "at", "it", "de", "es"]
        names_days = {}
        for name_country in names_day_countries:
            names_days_response = self.api_lookup(base_urls['namesday_api'] +
                                                  f"?name={self.__name}&calendar={name_country}")

            if names_days_response["results"]:
                country_response = self.api_lookup(base_urls['country_api'] + names_days_response['calendar'])

                country_name = country_response['name']
                day = names_days_response['results'][0]['day']
                month = names_days_response['results'][0]['month']
                names_days[country_name] = (day, month)
        return names_days

    def __str__(self):
        result_str = f"I predict that you are {self.__age} years old.\n"
        if self.__gender is None:
            result_str += "I can not predict your gender\n"
        else:
            result_str += f"My guess is that you are {self.__gender}.\n"
        result_str += f"I predict that you are from one of {', '.join(self.__countries)}\n"
        if len(self.__name_days) == 0:
            result_str += f"Can't find any name day for {self.__name}\n"
        else:
            result_str += "You have names day in the following countries:\n"
            for country, date in self.__name_days.items():
                day = date[0]
                month_name = calendar.month_name[date[1]]
                result_str += f"In {country}: {day} {month_name}\n"
        return result_str

    def get_predicted_age(self):
        return self.__age

    def get_predicted_gender(self):
        return self.__gender
