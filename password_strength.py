import sys
import getpass
import re
import os

def load_dictionary(filepath):
    if not os.path.exists(filepath):
        return None
    password_data = []
    with open(filepath, 'r') as password_dictionary:
        for line in password_dictionary:
            password_data.append(line.rstrip('\n'))
    return password_data


def contains_date_phones_nubmers(password):
    if re.search("(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}", #phone number
                                         password) is not None:
        return True
    if re.search("(?:[0-9]{1,3}\.){3}[0-9]{1,3}", password) is not None: #simple ip
        return True
    if re.search("(0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01])[- /.](19|20)\d\d", #mm.dd.yyyy
     password) is not None:
        return True
    if re.search("(0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.](19|20)\d\d" #dd-mm-yyyy
        , password) is not None:
        return True
    return False

def get_password_strength(password, path_to_dictionary = None):
    result_points = 0
    points = {
        "both_case"      : 2,
        "length_min"     : 1,
        "length_enough"  : 2,
        "digits"         : 1,
        "symbols"        : 2,
        "abbreviations"  : 1,
        "magic_numbers"  : 2,
        "out_magic_numb" : 1,
        "not_in_dict"    : 2
    }
    if password is None:
        return 0
    if path_to_dictionary is not None:
        password_dict = load_dictionary(path_to_dictionary)
        if password in password_dict:
            print("Use another password")
            return 0
        else:
            result_points += points["not_in_dict"]
    if password != password.lower():
        result_points +=points["both_case"]
    if (len(password) >=8) & (len(password) < 12) :
        result_points += points["length_min"]
    if len(password) >= 12:
        result_points += points["length_enough"]
    if re.search("[0-9]", password) is not None:
        result_points += points["digits"]
    if re.search("[^\w\d]", password) is not None:
        result_points += points["symbols"]
    if re.search("[A-Z]{2,4}", password) is not None:
        result_points -= points["abbreviations"]        
    if  not contains_date_phones_nubmers(password):
        result_points += points["out_magic_numb"]
    else:
        result_points -= points["magic_numbers"]
    return result_points

if __name__ == '__main__':
    password = getpass.getpass("Your password:\n")
    if len(sys.argv) == 2:
        print("The strength of your password is {}".format(get_password_strength(password, sys.argv[1])))
    else:
        print("The strength of your password is {}".format(get_password_strength(password)))