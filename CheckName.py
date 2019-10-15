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


def api_lookup(url):
    return json.loads(requests.get(url).text)


def get_age(name):
    return api_lookup(base_urls['age_api'] + "?name=" + name)['age']


def get_gender(name):
    return api_lookup(base_urls['gender_api'] + "?name=" + name)['gender']


def get_nationalities(name):
    nationalities = api_lookup(base_urls['nat_api'] + "?name=" + name)
    country_ids = [country['country_id'] for country in nationalities['country']]
    country_names = api_lookup(base_urls['country_api'] + "?codes=" + ";".join(country_ids))

    return [country['name'] for country in country_names]


def get_names_days(name):
    names_day_countries = ["us", "cz", "sk", "pl", "fr", "hu", "hr", "se", "at", "it", "de", "es"]
    names_days = {}
    for name_country in names_day_countries:
        names_days_response = api_lookup(base_urls['namesday_api'] + f"?name={name}&calendar={name_country}")

        if names_days_response["results"]:
            country_response = api_lookup(base_urls['country_api'] + names_days_response['calendar'])

            country_name = country_response['name']
            day = names_days_response['results'][0]['day']
            month = names_days_response['results'][0]['month']
            names_days[country_name] = (day, month)
    return names_days


def main():
    name = input("Please enter your first name: ")
    age = get_age(name)
    print(f"I predict that you are {age} years old.")

    gender = get_gender(name)
    if gender is None:
        print("I can not predict your gender")
    else:
        print(f"My guess is that you are {gender}.")

    countries = get_nationalities(name)
    print(f"I predict that you are from one of {', '.join(countries)}")

    names_days = get_names_days(name)
    if len(names_days) == 0:
        print(f"Can't find any name day for {name}")
    else:
        print("You have names day in the following countries:")
        for country, date in names_days.items():
            day = date[0]
            month_name = calendar.month_name[date[1]]
            print(f"In {country}: {day} {month_name}")


if __name__ == '__main__':
    main()
