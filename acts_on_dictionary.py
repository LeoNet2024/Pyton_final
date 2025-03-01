# LEON GITELMAN 49/3

import sys

from work_with_local_files import *


def update_attribute_in_files(dict_contain_files_detail: dict, suspicious_suffix_path: str,
                              suspicious_file_name_path: str, attribute_to_update: str, file_size: int) -> None:
    """
    This function gets dictionary with the files details, and files path
    and which value to change
    This function update the suspicious level inside the dictionary.
    that means all the values inside the dictionary will change. what gonna to change is :
    file name { 'suspicious level: __change here !!___ }
    suspicious level will be changed according to 2 files, one of the files is list with suspicious file name,
    and the second file contain  suspicious suffix file

    :param file_size:
    :param dict_contain_files_detail:
    :param suspicious_suffix_path:
    :param suspicious_file_name_path:
    :param attribute_to_update:
    :raise TypeError
    :raise KeyError
    :return: None
    """
    if type(dict_contain_files_detail) != dict:
        raise TypeError("The parameter must be a dictionary")

    if type(attribute_to_update) != str:
        raise TypeError(f"{attribute_to_update} Must be a String")

    if type(file_size) != int:
        raise TypeError(f"{file_size} invalid, must be a number")

    # Created two list:
    # 1) One list contain all the file names that can be a suspicious
    # 2) Second list contain all the file suffix that can be a suspicious
    suspicious_file_name_list = create_list_suspicious_objects(suspicious_file_name_path)
    suspicious_suffix_list = create_list_suspicious_objects(suspicious_suffix_path)

    # Make sure that the lists not Empty
    # if the length of one of the list is equals to 0, that means the list are empty.
    # we cannot work with empty list, therefore we throw  ValueError executions
    if len(suspicious_file_name_list) == 0 or len(suspicious_suffix_list) == 0:
        raise ValueError("One of the files is empty")

    try:
        # This loop used for update the suspicious level for each file
        for key, values in dict_contain_files_detail.items():
            file_name = os.path.splitext(key)[0]  # file name without the point of suffix
            # In this step we used other function to find out the level of the suspicious
            suspicious_level = find_level_suspicious_file(values, suspicious_suffix_list,
                                                          file_size,
                                                          suspicious_file_name_list,
                                                          file_name)
            # update the suspicious_level :
            values[attribute_to_update] = suspicious_level

    except KeyError:
        raise KeyError(f"{attribute_to_update} Not exist")


def find_level_suspicious_file(file_from_dictionary: dict,
                               suspicious_suffix_list: list,
                               file_size: int, suspicious_file_name_list: list, file_name: str) -> int:
    """
    This function get part from dictionary and return for this file the level of suspicious
    The function used in collect 'points' of dangerous level, using 3 categories:
    ____________________________________________________________________________
    1) if file size must be bigger than given param -> + 1 point
    2 ) if the file name exist inside the given list name - > +1 point
    3) if the suffix of the file exist inside the given suffix list -> +1 point
    ____________________________________________________________________________
    the total sum of point cannot be bigger than 3 and cannot be less than 1

    :param file_name:
    :param suspicious_file_name_list:
    :param file_size:
    :param file_from_dictionary:
    :param suspicious_suffix_list:
    :raise TypeError
    :return: suspicious level
    """

    if type(file_size) != int:
        raise TypeError(f"{file_size} Must be a number")

    suspicious_level = 0  # used to sum the 'points'

    if file_name in suspicious_file_name_list:
        suspicious_level += 1  # find if the file name exist into  list

    if file_from_dictionary['suffix'] in suspicious_suffix_list:
        suspicious_level += 1  # find if the suffix exist into  list

    if file_from_dictionary['size_Bytes'] > file_size:
        suspicious_level += 1  # find if file size bigger then the variable that given from user

    if suspicious_level == 0:  # cannot be smaller than 1
        return 1
    return suspicious_level


def marks_files_as_secured(file_name_to_mark: str, dictionary_files_details: dict, directory_path: str) -> None:
    """
    This function get from the user file name and marks the file as secured, if the file exist.
    memory img before : {file_name : {'secured : false '}}
    memory img After : {file_name : {['secured : True ']}}


    :param file_name_to_mark:
    :param dictionary_files_details:
    :param directory_path:
    :raise TypeError
    :raise FileNotFoundError
    :return: None
    """
    # check the types
    if type(file_name_to_mark) != str or type(directory_path) != str:
        raise TypeError(f"{file_name_to_mark} must be string")

    # check the types
    if type(dictionary_files_details) != dict:
        raise TypeError(f" cannot be {type(dictionary_files_details)}")

    # check if the file name exist inside the dict
    if file_name_to_mark not in get_list_of_files_from_input(directory_path):
        raise FileNotFoundError(f"{file_name_to_mark} Not found !!")

    try:
        # update the value of secured to true
        dictionary_files_details[file_name_to_mark]['secured'] = True
    except FileNotFoundError:
        raise FileNotFoundError(f"{directory_path} Not found")
    except KeyError:
        raise KeyError("Attribute of the file not found")


def show_all_directory_stats(dict_contain_all_files: dict):
    """
    This function used to observ the user all the stats in the directory,
    the function gets dict that contain files, and checking the follow params:
    _______________________________________________

    1)  the total number of the suspicious files
    2)  Number of files with different suffix
    3) smallest files name
    4) heaviest files name
    _______________________________________________

    :param dict_contain_all_files:
    :raise TypeError
    :return: None
    """
    if type(dict_contain_all_files) != dict:
        raise TypeError(f" cannot be {type(dict_contain_all_files)}")

    total_suspicious_file = 0  # count all the suspicious files
    set_suffix_file = []  # count the suffix by list
    max_size = 0  # find the max size
    min_size = sys.maxsize  # Max size of int
    heaviest_file_name = None
    smallest_file_name = None

    try:
        # this loop wrote for find all the above parameters:
        for key, value in dict_contain_all_files.items():
            if not value['secured']:  # count the unsecured  files
                total_suspicious_file += 1
            set_suffix_file.append(value['suffix'])  # Adding all suffix to list
            if value['size_Bytes'] > max_size:  # find out the heaviest file
                max_size = value['size_Bytes']
                heaviest_file_name = key
            elif value['size_Bytes'] < min_size:  # find out the smallest file
                max_size = value['size_Bytes']
                smallest_file_name = key
    except KeyError:
        raise KeyError(f"invalid key")

    print("_________________________________________________________________________")
    print("The number of  files with different suffix:  ", len(set(set_suffix_file)))
    print("Total number of files in directory: ", len(dict_contain_all_files))
    print("Number of suspicious file  :", total_suspicious_file)
    print("The heaviest file is: ", heaviest_file_name)
    print("The smallest file is", smallest_file_name)
    print("_________________________________________________________________________")


def remove_all_suspicious_files(suspicious_files_dict: dict, directory_path: str) -> None:
    """
    This function allowed to the user to remove all suspicious files from dictionary
    using   os.remove and  os.path.exists
    :param suspicious_files_dict:
    :param directory_path:
    :raise ValueError
    :raise PermissionError
    :return: None
    """
    warning_before_remove = input("Are you sure that you want remove? Y/N")

    # The answer must be or y or n
    if warning_before_remove.lower() != 'n' and warning_before_remove.lower() != 'y':
        raise ValueError(f"{warning_before_remove.lower()} is invalid, only N/Y answers are valid ")

    # return from the function if the user insert n (no)
    if warning_before_remove.lower() == 'n':
        return

    # else remove all the files from this directory
    elif warning_before_remove.lower() == 'y':
        try:
            # remove all suspicious files from dictionary
            for key, value in suspicious_files_dict.items():
                if value['secured'] == False:
                    if os.path.exists(f"{directory_path}/{key}"):  # check if the files exist into the directory
                        file_name = key  # saved the file name
                        os.remove(f"{directory_path}/{key}")  # remove the file
                        print(f"{os.getcwd()}/{file_name} removed from your PC")  # print message to user
                    else:
                        raise FileNotFoundError(f"{key} not found in the directory")
        except PermissionError:
            raise PermissionError(f"Permission dined")


def print_nice_dict_for_user(files_dict: dict) -> None:
    """
    This function used to print  the dictionary nicely
    :param files_dict:
    :raise TypeError:
    :return:None
    """
    if type(files_dict) != dict:
        raise TypeError("Must be a dictionary")

    for key, value in files_dict.items():
        print(f"____________________________ \n"
              f"File name : "
              f"{key}  "
              f"\n "
              f"{value} \n"
              f"___________________________"
              )
