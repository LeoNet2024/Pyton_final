# LEON GITELMAN 49/3

from acts_on_dictionary import *
from practice_exam_questions import *
from work_with_local_files import *


def print_user_menu(directory_path: str) -> None:
    """
    This function print nice menu for the user
    :return: None
    """

    print(f"1) Enter new Directory and Scan the Directory:' \n"
          f"2) create log files \n"
          f"3) Marks files as secured \n"
          f"4) show all the stats for:  '{directory_path}' \n"
          f"5) remove all the unsecured files from:  '{directory_path}' \n"
          f"6) quit from the program \n")


def list_functions_user_choose(user_choose: int, user_directory: str,
                               dict_unsecured_files_from_main, file_path_suffix: str, file_path_names: str,
                               file_size: int) -> None:
    """
    This function allowed to user interact with the menu by inserts number between 1-6.
    each number from 1-6 calling to different functions.
    this function called many times from the main, depends on user chose
    :param file_size:
    :param file_path_names:
    :param file_path_suffix:
    :param dict_unsecured_files_from_main:
    :param user_directory:
    :param user_choose:
    :return: None
    """

    directory_after_change = {}  # this directory used to save all the changed that users decide to make

    if user_choose == 6:
        # if the code get here that mean the user want to quit from the program,
        # but in the main we're using infinity loop (while true),
        # so good way to stop the code and quit from the loop is to throw custom exception
        raise Exception("User decide to quit")

    # make sure that the range is valid from the user
    if user_choose < 1 or user_choose > 6:
        raise ValueError(f"Must be a number between 1-6")

    # print nice the result of the dict
    if user_choose == 1:
        # step 1: scan and update the suspicious_level
        update_attribute_in_files(dict_unsecured_files_from_main, file_path_suffix, file_path_names, 'suspicious_level',
                                  file_size)
        # step 2 : display the result to the user
        print_nice_dict_for_user(dict_unsecured_files_from_main)
        # step 3 : display menu
        print_user_menu(user_directory)

    # create a JSON file with all the details
    elif user_choose == 2:
        save_new_file_unix_time(dict_unsecured_files_from_main, 'suspicious_level')
        print("File has been created!")
        print_user_menu(user_directory)

    # allowed to user marks files as secured file
    elif user_choose == 3:
        file_name_to_mark = input("Enter file name to mark as secured :")
        marks_files_as_secured(file_name_to_mark, dict_unsecured_files_from_main, user_directory)
        print_user_menu(user_directory)

    # allowed to user see all the stats from this directory
    elif user_choose == 4:
        show_all_directory_stats(dict_unsecured_files_from_main)
        print_user_menu(user_directory)

    # allowed to user remove/clean the unsecured files
    elif user_choose == 5:
        remove_all_suspicious_files(dict_unsecured_files_from_main, user_directory)
        print_user_menu(user_directory)
