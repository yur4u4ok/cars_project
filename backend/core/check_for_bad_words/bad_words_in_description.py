def check_for_bad_words(data):
    list_of_bad_words = ['fuck', 'suck', 'dick', 'pussy', 'anos', 'shit', 'ass', 'fucking']

    try:
        desc = data.get('description', False)
    except AttributeError:
        for i in list_of_bad_words:
            if i in data.lower().replace(",", "").split():
                return True
        return False

    if not desc:
        return False

    car_description_space_split = data['description'].lower().replace(",", "").split()

    for i in list_of_bad_words:
        if i in car_description_space_split:
            return True

    return False
