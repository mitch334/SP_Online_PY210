#!/usr/bin/env python3
import tempfile
import time
import sys


donors = {
    "STEVE JOBS":
        {"name": "Steve Jobs", "total_don": 1002.40, "donations": 2, "avg": 501.20},
    "JEFF BEZOS":
        {"name": "Jeff Bezos", "total_don": 877.33, "donations": 1, "avg": 877.33},
    "BILL GATES":
        {"name": "Bill Gates", "total_don": 653784.49, "donations": 2, "avg": 326892.24},
    "MARK ZUCKERBERG":
        {"name": "Mark Zuckerberg", "total_don": 16396.10, "donations": 3, "avg": 5465.37},
    "PAUL ALLEN":
        {"name": "Paul Allen", "total_don": 708.42, "donations": 3, "avg": 236.14}
}


def menu_input():
    return input(
        "\nSelect an option number:"
        "\n1. Send a Thank You"
        "\n2. Create a Report"
        "\n3. Send letters to all donors"
        "\n4. Quit\n"
    )


def thank_you():
    thank_you_options = {
        "MENU": False,
        "LIST": list_donors
    }
    while True:
        user_selection = (
            input("\nPlease provide a full name to send thank you note to (options 'list' and 'menu'): ")
        )
        action = thank_you_options.get(user_selection.upper())
        if action is False:
            break
        elif action is None:  # Write letter to user selection if an action option wasn't selected
            write_letter(user_selection)
        else:
            action()


def list_donors():
    for name in donors:
        print(name)


def write_letter(person):
    if person.upper() in donors:
        current_donor = donors[person.upper()]
    else:
        current_donor = add_donor(person)
    while True:  # Loop until a valid amount is provided
        donation_amount = input("\nHow much did {} donate?: ".format(person))
        try:
            donation_amount = round(float(donation_amount), 2)
        except ValueError:
            print("Please provide a valid amount")
        else:
            break
    add_donation(current_donor, donation_amount)
    print("Thank you {}, for your generous donation of ${:.2f}!".format(current_donor["name"], donation_amount))


def add_donor(new_name):
    donors[new_name.upper()] = {"name": new_name, "total_don": 0, "donations": 0, "avg": 0}
    return donors[new_name.upper()]


def add_donation(donor, donation_value):
    donor["donations"] += 1
    donor["total_don"] = round(donor["total_don"] + float(donation_value), 2)
    donor["avg"] = round(donor["total_don"]/donor["donations"], 2)


def print_report():
    header = ["Donor Name", "Total Given", "Num Gifts", "Average Gift"]
    header_string = "{0:<{w1}} | {1:>{w2}} | {2:>{w3}} | {3:>{w4}}"
    data_string = "{0:<{w1}}  ${1:>{w2}}   {2:>{w3}}  ${3:>{w4}}"
    width_dict = donors.copy()  # width dictionary is used only to find column widths
    width_dict["HEADER"] = {
        "name": "Donor Name", "total_don": "Total Given", "donations": "Num Gifts", "avg": "Average Gift"
    }
    width_list = [v2 for k, v in width_dict.items() for k2, v2 in v.items()]
    width_list = [width_list[i * 4:(i + 1) * 4] for i in range((len(width_list) + 4 - 1) // 4)]  # list of lists
    w = find_widths(width_list)
    header_to_print = print_line(header_string, header, w)
    print(header_to_print)
    print('-' * len(header_to_print))
    for key, value in sorted(donors.items(), reverse=True, key=lambda x: x[1]['total_don']):
        print(print_line(data_string, value.values(), w))


def find_widths(seq):
    return [max(len(str(row[i])) for row in seq) for i in range(len(seq[0]))]


def print_line(line_format, info, width):
    row_string = (line_format.format(*info, w1=width[0], w2=width[1], w3=width[2], w4=width[3]))
    return row_string


def print_all():
    file_location = tempfile.gettempdir()
    print("letters stored at: " + file_location)
    for key, value in donors.items():
        file_name = "{}{}{}{}{}".format(file_location, "\\", value["name"], time.strftime("%Y%m%d-%H%M%S"), ".txt")
        with open(file_name, "w") as file:
            file.write("Dear {name},"
                       "\n\nThank you for your very kind donations totaling ${total_don:.2f}."
                       "\nIt will be put to very good use."
                       "\n\nSincerely,"
                       "\n-The Team".format(**value))


def main():
    menu_switch = {
        "1": thank_you,
        "2": print_report,
        "3": print_all,
        "4": sys.exit
    }
    while True:
        user_selection = menu_input()
        action = menu_switch.get(user_selection)
        try:
            action()
        except TypeError:
            print("Please provide a valid option \n")


if __name__ == '__main__':
    main()
