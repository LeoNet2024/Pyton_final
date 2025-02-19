# LEON GITELMAN 49/3

from acts_on_dictionary import update_attribute_in_files
from menu_for_user import list_functions_user_choose
from work_with_local_files import *
from typing import Final

# NOT CHANGED WHILE THE CODE IS RUNNING ,SO ITS FINAL VARIABLES
FILE_PATH_SUFFIX: Final = "files_parts_of_project/suspicious_file_types.txt"
FILE_PATH_NAMES: Final = "files_parts_of_project/suspicious_file_names.txt"
FILE_SIZE_TO_CHECK: Final = 10


def main():
    try:
        # step 1 : asked the user directory path/name
        user_directory = input("Enter Directory Name:")
        # step 2: create first dict that contain all the details
        working_dict = get_dict_files_details(user_directory)
        # step 3 : calling the function to see the result(the first option)
        list_functions_user_choose(1, user_directory, working_dict, FILE_PATH_SUFFIX, FILE_PATH_NAMES,
                                   FILE_SIZE_TO_CHECK)

        # infinity loop (while true) that means the loop will work until the code throw false or execution
        while True:
            user_input = int(input("please chose a number between 1-6"))
            if user_input == 1:  # if the user want to scan other directory
                user_directory = input("Enter Directory Name:")
                # call for this function to switch directory and create new dict
                working_dict = get_dict_files_details(user_directory)  # -> set new dict from new path
            # if code came here the user want to continue work on current directory
            list_functions_user_choose(user_input, user_directory, working_dict, FILE_PATH_SUFFIX, FILE_PATH_NAMES,
                                       FILE_SIZE_TO_CHECK)
            working_dict = create_dict_not_secured_files(working_dict)  # Update the dictionary

    except BaseException as e:
        print(e)


if __name__ == "__main__":
    main()
