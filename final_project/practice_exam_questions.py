def get_dict_of_secured_files(prime_dict_from_path: dict, unsecured_dict_files: dict) -> dict:
    """
    This function gets Two dictionary:
    1- is the first dictionary that we are created, and contain all the details
    2  - is dictionary that contain only unsecured files.
    purpose of the function is to return secured dict
    :param prime_dict_from_path:
    :param unsecured_dict_files:
    :raise TypeError
    :return:  return secured dict
    """

    # Make sure the given parameters from dictionary type
    if type(prime_dict_from_path) != dict or type(unsecured_dict_files) != dict:
        raise TypeError("there is problem with the given dictionaries")

    # new dict:
    dict_only_secured_file = {}

    for key, value in prime_dict_from_path.items():

        # if key is not exist in unsecured dict that means the files has been removed from the dictionary
        # so we can know for sure the file is secured, and we can add it to the new list
        if key not in unsecured_dict_files:
            dict_only_secured_file[key] = value

    # Update the value of secured to true.
    # because when we copy the values from the dictionary, the values of ['secured'] is false
    # And we want dictionary that contain value of ['secured'] == true
    for value in dict_only_secured_file.values():
        value['secured'] = True

    return dict_only_secured_file


def get_total_size_files(dict_contain_file: dict) -> int:
    """
    This function get a dictionary and calculate the total size of secured files
    :param dict_contain_file:
    :raise TypeError
    :raise KeyError
    :return: total size
    """
    if type(dict_contain_file) != dict:
        raise TypeError

    totalsize = 0

    try:
        for value in dict_contain_file.values():
            if value['secured'] == True:
                totalsize += value['size_Bytes']
    except KeyError:
        raise KeyError(f"There is a problem with the key")

    return totalsize * (10 ** -6)  # 1 Byte = 0.000001 MB (in decimal)


def get_setlist_contain_values(dict_contain_file: dict, value_name_add_to_list: str) -> list:
    """
    This function get a dictionary that contain all the info about the files,
    and gets a value name. the function return the list that contain all the values
    that fit to variable from parameter(value_name_add_to_list)
    :param dict_contain_file:
    :param value_name_add_to_list:
    :return: list with all values from dictionary
    """

    if type(dict_contain_file) != dict:
        raise TypeError

    if type(value_name_add_to_list) != str:
        raise TypeError
    list_suffix = []

    try:
        for value in dict_contain_file.values():
            list_suffix.append(value[value_name_add_to_list])
    except KeyError:
        raise KeyError(f"{value_name_add_to_list} is not a real value")

    return list_suffix


def total_number_of_each_suffix(dict_contain_file: dict) -> dict:
    """
    This function return list that contain the unsecured suffix of file
    and how many times this suffix appears in the directory
    for example: [ {'.txt':3} , {'.com':4 ....} ]
    :param dict_contain_file:
    :return:
    """
    if type(dict_contain_file) != dict:
        raise TypeError

    suffix_list = (get_setlist_contain_values(dict_contain_file, 'suffix'))
    if len(suffix_list) == 0:
        raise ValueError

    final_dict = {}

    for eachSuffix in suffix_list:
        final_dict[eachSuffix] = suffix_list.count(eachSuffix)

    return final_dict
