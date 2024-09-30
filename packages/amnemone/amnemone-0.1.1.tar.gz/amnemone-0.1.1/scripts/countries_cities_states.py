from amnemone.data.countries_states_cities import Cities, Countries


def main():
    mn_cities = Cities()
    mn_cities_5 = mn_cities.random(5)
    print(mn_cities_5)

    mn_cities_lookup = mn_cities._decode(mn_cities_5)
    print(mn_cities_lookup)

    mn_countries = Countries(key='emoji')
    print(mn_countries.radix)
    print(mn_countries.random(5))


if __name__ == '__main__':
    main()
