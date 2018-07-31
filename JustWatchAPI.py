from justwatch import JustWatch

def to_watch(movie_title, release_year):
    '''constract dict with one buy and rent offers for ituns, google play, amazon, and showtime is cinema'''

    just_watch = JustWatch(country='US')

    results_by_multiple = just_watch.search_for_item(query=movie_title,
                                                     monetization_types=['buy', 'rent', 'cinema'])

    #print(results_by_multiple)

    items = results_by_multiple['items']

    selected_items = list(filter(lambda x: x['title'].lower() == movie_title.lower()
                            and x['original_release_year'] == release_year, items))

    if len(selected_items) != 1:
        print(selected_items)
        return 'Too many result'
       
    my_movie = selected_items[0]
    title = my_movie['title']
    short_descr = my_movie['short_description']
    release_year = my_movie['original_release_year']
    runtime = my_movie['runtime']

    offers = my_movie['offers']

    check_dict = {'itunes_buy': False,
                 'itunes_rent': False,
                 'play_buy': False,
                 'play_rent': False,
                 'amz_buy': False,
                 'amz_rent': False,
                 'fandango': False}

    watch_dict = {'title': title, 
                  'short_descr': short_descr,
                  'release_year': release_year,
                  'runtime': runtime,
                  'buy': [], 'rent': [], 'cinema': None}

    for offer in offers:

        if offer['monetization_type'] == 'buy':
            if offer['provider_id'] == 2 and not check_dict['itunes_buy']:
                itunes_dict = {'provider': 'iTunes',
                                'price': offer['retail_price'],
                                'url': offer['urls']['standard_web']}
                watch_dict['buy'].append(itunes_dict)
                check_dict['itunes_buy'] = True

            elif offer['provider_id'] == 3 and not check_dict['play_buy']:
                play_dict = {'provider': 'Google Play',
                                'price': offer['retail_price'],
                                'url': offer['urls']['standard_web']}
                watch_dict['buy'].append(play_dict)
                check_dict['play_buy'] = True

            elif offer['provider_id'] == 10 and not check_dict['amz_buy']:
                amz_dict = {'provider': 'Amazon',
                                'price': offer['retail_price'],
                                'url': offer['urls']['standard_web']}
                watch_dict['buy'].append(amz_dict)
                check_dict['amz_buy'] = True

        elif offer['monetization_type'] == 'rent':
            if offer['provider_id'] == 2 and not check_dict['itunes_rent']:
                itunes_dict = {'provider': 'iTunes',
                                'price': offer['retail_price'],
                                'url': offer['urls']['standard_web']}
                watch_dict['rent'].append(itunes_dict)
                check_dict['itunes_rent'] = True

            elif offer['provider_id'] == 3 and not check_dict['play_rent']:
                play_dict = {'provider': 'Google Play',
                                'price': offer['retail_price'],
                                'url': offer['urls']['standard_web']}
                watch_dict['rent'].append(play_dict)
                check_dict['play_rent'] = True

            elif offer['provider_id'] == 10 and not check_dict['amz_rent']:
                amz_dict = {'provider': 'Amazon',
                                'price': offer['retail_price'],
                                'url': offer['urls']['standard_web']}
                watch_dict['rent'].append(amz_dict)
                check_dict['amz_rent'] = True
        elif offer['provider_id'] == 60 and not check_dict['fandango']:
            url = offer['urls']['standard_web']
            watch_dict['cinema'] = url
            check_dict['fandango'] = True

    watch_dict['buy'].sort(key= lambda y: y['price'])
    watch_dict['rent'].sort(key= lambda y: y['price'])
    
    return watch_dict
    
if __name__ == '__main__':
    print(to_watch('Red Sparrow', 2018))
    print(to_watch('Avatar', 2009))

