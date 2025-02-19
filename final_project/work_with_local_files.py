# LEON GITELMAN 49/3

import json
import os
import time


def get_list_of_files_from_input(directory_name_from_user: str) -> list:
    """
    This function get from the user directory name and return a list that contain all the files that exist in the directory
    Using the operator os.listdir =>
    This function used only for  get_dict_files_details!!!!
    :param directory_name_from_user:
    :return List that contain all file that exist in the directory
    :raise FileNotFoundError
    :raise PermissionError
    :raise TypeError
    """
    if type(directory_name_from_user) != str:
        raise TypeError(f"{directory_name_from_user} Must be a string!!!")

    try:
        return os.listdir(directory_name_from_user)
    except FileNotFoundError:
        raise FileNotFoundError(f"{directory_name_from_user} Does not exist")
    except PermissionError:
        raise PermissionError("Permission Denied")


def get_dict_files_details(directory_name_from_user: str) -> dict:
    """
    This function gets from the parameters list that contain all files names in the directory.
    And created a dictionary with the following details:
    1)key = file name
    2) values of each file name : size,suffix of the file, and if the file is secured
    :param directory_name_from_user:
    :return: dictionary with key file name and value (size,suffix....)
    :raise TypeError
    :raise ValueError

    """
    if type(directory_name_from_user) != str:
        raise TypeError(f"{directory_name_from_user} Must be a string!!!")

    list_contain_file_names = get_list_of_files_from_input(directory_name_from_user)

    if len(list_contain_file_names) == 0:
        raise ValueError(f"{directory_name_from_user} not contain any files")

    # create empty dict to save each file details
    dictionary_contain_files = {}

    # This loop create keys depends on the list length
    for eachFile in list_contain_file_names:
        dictionary_contain_files[eachFile] = {}

    # This loop created a dictionary that contain 4 keys: name,size,suffix and secured.
    # Also, the loop adding to each key values from the list of files that we got from the function
    for key, value in dictionary_contain_files.items():
        suffix_file = os.path.splitext(key)[1]
        value["suffix"] = suffix_file.replace(".", "")  # remove  the point before the suffix  .txt ....
        file_full_path = os.path.join(directory_name_from_user, key)  # used for know the full path for the file size
        value["size_Bytes"] = os.path.getsize(file_full_path)  # get the size of the file
        value["secured"] = False
        value["suspicious_level"] = 1

    return dictionary_contain_files


def create_dict_not_secured_files(prime_dict_before_sort: dict) -> dict:
    """
    This function return a dictionary that contain all files details. but
    only the non-secured files will appear!
    :param prime_dict_before_sort:
    :return: dictionary that contain files that not secured
    :raise TypeError
    """
    if type(prime_dict_before_sort) != dict:
        raise TypeError("Must be a dictionary")

    dict_files_not_secured = {}
    for key, value in prime_dict_before_sort.items():
        if value['secured'] == False:  # only is the file is unsecured add it to the new dict
            dict_files_not_secured[key] = value

    return dict_files_not_secured


def create_list_suspicious_objects(file_path: str) -> list:
    """
    This function help us to determinate the suspicious level by reading from file and return list
    This function return list that contain all the info that given from the file path,
    the file path is  file with suspicious objects that we need to determinate the suspicious level
    in this code this function will be called twice. once for the file with the suspicious names.
    and once for the file with the suspicious suffix.
    :param file_path:
    :raise TypeError:
    :raise PermissionError:
    :raise FileNotFoundError:
    :raise OSError:
    :return: list
    """

    # check the type
    if type(file_path) != str:
        raise TypeError("File path must be a string")

    try:
        # reading from the file and create a list that contain all the values
        with open(file_path, 'r') as suspicious_list:
            list_suspicious_obj = (suspicious_list.read().split())
            # created list with all the info from file
            return list_suspicious_obj

    except PermissionError:
        raise PermissionError("access denied")

    except FileNotFoundError:
        raise FileNotFoundError(f"{file_path} Not found")

    except OSError:
        raise OSError(f"{file_path} Invalid type")


def save_new_file_unix_time(dict_contain_files_detail: dict, file_attribute_check: str):
    """
    This function gets a dictionary that contain files details.
    And creates new file that contain only files with suspicious level.
    Using unix time stamp and salt to save the file
    :param file_attribute_check:
    :param dict_contain_files_detail:
    :return: None
    :raise TypeError
    """
    if type(dict_contain_files_detail) != dict:
        raise TypeError("File must be dictionary")

    unix_time = str(int(time.time()))  # create unix time stamp
    salt_64byte = os.urandom(64).hex() + ".log"  # create a salt suffix with 64 byte

    file_name = unix_time + salt_64byte  # combine unixTime with the salt and suffix

    sorted_dictionary_by_suspicious_level = {}

    try:
        # save all the files from dict into JSON file
        for key, value in dict_contain_files_detail.items():
            sorted_dictionary_by_suspicious_level[key] = value
        # saving the new dictionary
        with open(file_name, 'w') as f:
            f.write(json.dumps(sorted_dictionary_by_suspicious_level, indent=2))
    except KeyError:
        raise KeyError(f"{file_attribute_check} Must be an attribute inside file")
