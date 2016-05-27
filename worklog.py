import os
import re
import csv

from datetime import datetime
from workentry import WorkEntry


class WorkLog:
    def __init__(self):
        self.warning = ""
        self.entries = []
        self.filtered_entries = []

        self.begin()

    def begin(self):
        while True:
            WorkLog.clear_screen()
            print(self.warning)
            self.warning = ""
            print()
            print("-Menu-")
            print("1. Add a new entry")
            print("2. Look up previous entries")
            print("3. Quit")
            print()

            option = input("Please pick an action: ")
            if option == '1':
                self.add_new_entry()
            elif option == '2':
                self.look_up()
            elif option == '3':
                WorkLog.clear_screen()
                break
            else:
                self.warning = "Your input is invalid, please try again!"
                continue

    def add_new_entry(self):
        while True:
            WorkLog.clear_screen()
            print(self.warning)
            self.warning = ""
            print()
            print("-Add new entry-")
            print()

            try:
                task_name = str(input("Task name : "))
                working_minutes = float(input('Working time (minutes): '))
                notes = str(input("General Notes: "))
            except TypeError:
                self.warning = "Your input value is in wrong type, please try again!"
                continue
            except ValueError:
                self.warning = "Your input is in wrong value, please try again!"
                continue

            new_entry = WorkEntry(task_name, working_minutes, notes)
            print(new_entry.get_summary())
            print()

            respond = input("Add this entry? (Y)/n : ").lower()
            if respond != 'n':
                self.entries.append(new_entry)

                # save to CSV
                with open('worklog.csv', 'a', newline='') as fp:
                    a = csv.writer(fp, delimiter=',')
                    data = [task_name, working_minutes, notes]
                    a.writerow(data)

                print("This entry has been saved successfully!")
                print()

            print()
            print("1. Add another new entry")
            print("2. Back to menu")
            if input("Please pick an action: ") == '2':
                break

    def edit_entry(self, entry):
        while True:
            WorkLog.clear_screen()
            print(self.warning)
            self.warning = ""
            print()
            print("-Edit entry-")
            print(entry.get_summary())

            try:
                task_name = str(input("New task name : "))
                working_minutes = float(input('New working time (minutes): '))
                notes = str(input("New general Notes: "))
            except TypeError:
                self.warning = "Your input value is in wrong type, please try again!"
                continue
            except ValueError:
                self.warning = "Your input is in wrong value, please try again!"
                continue

            new_entry = WorkEntry(task_name, working_minutes, notes)
            print(new_entry.get_summary())
            print()

            respond = input("Edit to this entry? (Y)/n : ").lower()
            if respond != 'n':
                self.update_entry(entry, new_entry)
                self.warning = "Modification has been saved successfully!"
                return new_entry

            print("1. Edit again")
            print("2. Back to menu")
            if input("Please pick an action: ") == '2':
                return entry

    def look_up(self):
        while True:
            WorkLog.clear_screen()
            print(self.warning)
            self.warning = ""
            print()
            print("-Look up-")
            print("1. By date")
            print("2. By keyword search")
            print("3. By pattern")
            print("4. By working time")
            print("5. Back to menu")
            print()

            option = input("Please pick an action: ")
            if option == '1':
                self.look_up_by_date()
                break
            elif option == '2':
                self.look_up_by_search()
                break
            elif option == '3':
                self.look_up_by_pattern()
                break
            elif option == '4':
                self.look_up_by_time()
                break
            elif option == '5':
                break
            else:
                self.warning = "Your input is invalid, please try again!"
                continue

    def look_up_by_date(self):
        while True:
            WorkLog.clear_screen()
            print(self.warning)
            self.warning = ""
            print()
            print("-Look up by date-")
            print("Example 1. day search DD/MM/YYYY: 26/01/2015")
            print("Example 2. range search DD/MM/YYYY: 26/01/2015 - 29/01/2015")
            print()

            option = str(input("Please pick the day(s) or '0' to quit: "))
            if option == '0':
                break
            if not option.__contains__('-'):
                option = "{} - {}".format(option, option)
                print(option)

            # Range of days search
            dates = re.findall('\d+/\d+/\d+', option)

            if len(dates) != 2:
                self.warning = "Bad dates range input, please try again!"
                continue
            try:
                start_date = datetime.strptime(dates[0], "%d/%m/%Y")
                end_date = datetime.strptime(dates[1], "%d/%m/%Y")
            except ValueError:
                self.warning = "Invalid dates range input, please try again!"
                continue
            if end_date.timestamp() - start_date.timestamp() < 0:
                self.warning = "Start date must before end date, please try again!"
                continue

            if input("You want to do a search on {} to {}? (Y)/n: ".format(start_date.date(), end_date.date())).lower() != 'n':
                self.filtered_entries.clear()
                for entry in self.entries:
                    if entry.is_between_dates(start_date, end_date):
                        self.filtered_entries.append(entry)
                self.show_up_search_result()

            print()
            print("1. Continue date search")
            print("2. Back to menu")
            if input("Please pick an action: ") == '2':
                break

    def look_up_by_search(self):
        while True:
            WorkLog.clear_screen()
            print(self.warning)
            self.warning = ""
            print()
            print("-Look up by search-")
            print()

            keyword = str(input("Please give a keyword: "))

            self.filtered_entries.clear()
            for entry in self.entries:
                if entry.has_keyword(keyword):
                    self.filtered_entries.append(entry)
            self.show_up_search_result()

            print()
            print("1. Continue keyword search")
            print("2. Back to menu")
            if input("Please pick an action: ") == '2':
                break

    def look_up_by_pattern(self):
        while True:
            WorkLog.clear_screen()
            print(self.warning)
            self.warning = ""
            print()
            print("-Look up by pattern-")
            print()

            keyword = str(input("Please give a pattern: "))

            self.filtered_entries.clear()
            for entry in self.entries:
                if entry.has_pattern(keyword):
                    self.filtered_entries.append(entry)
            self.show_up_search_result()

            print()
            print("1. Continue pattern search")
            print("2. Back to menu")
            if input("Please pick an action: ") == '2':
                break

    def look_up_by_time(self):
        while True:
            WorkLog.clear_screen()
            print(self.warning)
            self.warning = ""
            print()
            print("-Look up by time spent-")
            print("Example 1. single time (minutes): 3")
            print("Example 2. range time (minutes): 3 - 5")

            option = str(input("Please give a time range: "))

            if not option.__contains__('-'):
                option = "{} - {}".format(option, option)
                print(option)

            # Range of days search
            time_range = re.findall('\d+', option)
            if len(time_range) != 2:
                self.warning = "Bad dates range input, please try again!"
                continue
            try:
                lower_time = float(time_range[0])
                upper_time = float(time_range[1])
            except ValueError:
                self.warning = "Invalid dates range input, please try again!"
                continue
            except TypeError:
                self.warning = "Invalid dates range input, please try again!"
                continue
            if upper_time - lower_time < 0:
                self.warning = "The previous time should be equal or smaller to the next time, please try again!"
                continue

            if input("You want to do a search on {} to {} working time? (Y)/n: ".format(lower_time, upper_time)).lower() != 'n':
                self.filtered_entries.clear()
                for entry in self.entries:
                    if entry.is_between_work_time(lower_time, upper_time):
                        self.filtered_entries.append(entry)
                self.show_up_search_result()

            print()
            print("1. Continue time search")
            print("2. Back to menu")
            if input("Please pick an action: ") == '2':
                break

    def show_up_search_result(self):
        entries = self.filtered_entries
        while True:
            WorkLog.clear_screen()
            print(self.warning)
            self.warning = ""
            print()
            print("-Search result-")
            if len(entries) == 0:
                print("There is no matching result!")
            for i in range(len(entries)):
                print("{}. {}".format(i + 1, entries[i].task_name))

            print()
            try:
                option = int(input("Please pick an entry, 0 to back: "))
            except:
                self.warning = "Bad input, please try again!"
                continue

            if option == 0:
                break
            elif 0 < option <= len(entries):
                self.show_up_search_result_entry(entries[option - 1])
            else:
                self.warning = "Your input is invalid, please try again!"
                continue

    def show_up_search_result_entry(self, entry):
        while True:
            WorkLog.clear_screen()
            print(self.warning)
            self.warning = ""
            print()
            print("-Entry detail-")
            print(entry.get_summary())

            print()
            print("1. Edit entry")
            print("2. Delete entry")
            print("3. Back")
            option = input("Please pick an action: ")
            if option == '1':
                entry = self.edit_entry(entry)
                continue
            elif option == '2':
                self.remove_entry(entry)
                self.warning = "Entry has been deleted!"
                break
            elif option == '3':
                break
            else:
                self.warning = "Your input is invalid, please try again!"
                continue

    def remove_entry(self, entry):
        self.entries.remove(entry)
        self.filtered_entries.remove(entry)

    def update_entry(self, entry, new_entry):
        i1 = self.entries.index(entry)
        i2 = self.filtered_entries.index(entry)

        self.entries[i1] = new_entry
        self.filtered_entries[i2] = new_entry

    @staticmethod
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')
