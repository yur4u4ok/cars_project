def check_for_bad_words(data):
    list_of_bad_words = ['fuck', 'suck', 'dick', 'pussy', 'anos', 'shit', 'ass']

    car_description_space_split = data['description'].lower().split()
    car_description_comma_split = data['description'].lower().split(",")

    for i in list_of_bad_words:
        if (i in car_description_space_split) or (i in car_description_comma_split):
            return True

    return False
