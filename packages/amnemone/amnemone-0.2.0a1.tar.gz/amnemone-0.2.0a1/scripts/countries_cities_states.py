from amnemone.data.countries_states_cities import Cities, Countries


def main():
    mn_cities = Cities()
    mn_cities_5 = mn_cities.random(5)
    print(mn_cities_5)

    mn_cities_lookup = mn_cities._decode(mn_cities_5)
    print(mn_cities_lookup)

    mn_countries = Countries(key='emoji')
    mn_countries_5 = mn_countries.random(5)
    print(mn_countries_5)
    mn_countries_lookup = mn_countries._decode(mn_countries_5)
    print(mn_countries_lookup)


if __name__ == '__main__':
    main()
