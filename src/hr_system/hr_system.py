import sys
import pyfiglet
import pandas as pd
import numpy as np
from tabulate import tabulate
import dateutil
import datetime

result = pyfiglet.figlet_format("h r  s y s t e m", font="slant")
strStatus = ""

class UserSelection:
    """Handles User Selection Logic"""

    def switch(self, strChoice):
        """Builds a function name based off user choice and triggers the actions"""

        default = "Incorrect Selection"
        return getattr(self, "case_" + str(strChoice), lambda: default)()

    def case_1(self):
        """User selected print a list of all employees"""
        IO.print_all_employees(IO.get_employee_db())
        pass

    def case_2(self):
        """User selected Print a list of employees currently employed"""
        IO.print_all_employees_employed(IO.get_employee_db())
        pass

    def case_3(self):
        """User selected Print a list of employees who have left in the past month"""
        IO.print_employees_departures(IO.get_employee_db())

        pass

    def case_4(self):
        """User selected Display a reminder to schedule annual review"""
        IO.print_review_reminders(IO.get_employee_db())
        pass

    def case_5(self):
        """User selected Capture employee information"""

        employeeID, \
        firstName, \
        lastName, \
        fullName, \
        address,\
        ssn,\
        dateOfBirth,\
        jobTitle,\
        startDate,\
        endDate,\
        = IO.capture_employee_data(IO.get_employee_db())

        Processor.append_row(
            IO.get_employee_db(),
            employeeID, \
            firstName, \
            lastName, \
            fullName, \
            address, \
            ssn, \
            dateOfBirth, \
            jobTitle, \
            startDate, \
            endDate, \
            )

        pass

    def case_6(self):
        """User selected Delete record"""
        fullName = IO.input_name_to_delete()
        Processor.delete_record(IO.get_employee_db(), fullName)
        pass

    def case_7(self):
        """User selected Exit"""

        print("Goodbye ")

        sys.exit()

class Processor:
    """  Performs Processing tasks """

    @staticmethod
    def delete_record(dframe, name):
        """Generates a new DataFrame Filtering Out the record corresponding to the name to delete
        :param dframe: (Pandas DataFrame) DataFrame containing employee information
        :param name: (String) String representing the name to delete
        :return: nothing
        """
        df = dframe[(dframe.FullName != name)]

        newdf = df.copy()

        Processor.update_csv(newdf)

    @staticmethod
    def update_csv(dframe):
        """Writes the filtered DataFrame to a csv file
        :param dframe: (Pandas DataFrame) DataFrame containing employee information
        :return: nothing
        """

        dframe.to_csv('EmployeeData.csv', index=False)

    @staticmethod
    def generate_employee_id(dframe):
        """Generates unique employee id
        :param dframe: (Pandas DataFrame) DataFrame containing employee information
        :return next_id: (Integer) Next ID to be used for an employee record
        """
        max_id = dframe['EmployeeID'].max()
        next_id = max_id + 1

        return next_id

    @staticmethod
    def append_row(dframe, id, first, last, full, address, ssn, dob, job, startDate, endDate):
        """Generates unique employee id
        :param dframe: (Pandas DataFrame) DataFrame containing employee information
        :return next_id: (Integer) Next ID to be used for an employee record
        """
        print(id, first, last, full, address, ssn, dob, job, startDate, endDate)

class IO:
    """Performs Input and Output tasks"""

    @staticmethod
    def get_menu(argument):
        """Uses dictionaries to display options to the user
        :param argument: (Integer) None
        :return: (String) the value of the switcher dictionary
        """

        def one():
            return "1) Print a list of all employees"

        def two():
            return "2) Print a list of employees currently employed"

        def three():
            return "3) Print a list of employees who have left in the past month"

        def four():
            return "4) Display reminder to schedule annual review"

        def five():
            return "5) Capture employee information"

        def six():
            return "6) Delete record"

        def seven():
            return "7) Exit"

        switcher = {
            1: one(),
            2: two(),
            3: three(),
            4: four(),
            5: five(),
            6: six(),
            7: seven(),
        }
        return switcher.get(argument, "Invalid Selection")

    @staticmethod
    def input_menu_choice():
        """Gets the menu choice from a user
        :param: None
        :return: string
        """

        while True:
            try:
                choice = str(
                    input("Which option would you like to perform? [1 to 7] - ")
                ).strip()
                if choice not in ["1", "2", "3", "4", "5", "6", "7"]:
                    raise ValueError("Choice not an option, enter 1, 2, 3, 4, 5, 6, 7")
            except ValueError as e:
                print(e)
            else:
                break
        print()  # Add an extra line for looks

        return choice

    @staticmethod
    def input_press_to_continue(optional_message=""):
        """Pause program and show a message before continuing
        :param optional_message:  An optional message you want to display
        :return: nothing
        """
        print(optional_message)
        input("Press the [Enter] key to continue.")


    @staticmethod
    def print_all_employees(dframe):
        """Shows the current Donors
        :param donor_db: (Dictionary) dictionary of dictionaries containing all donors info
        :return: nothing
        """
        print(tabulate(dframe, headers='keys', tablefmt='psql', showindex=False))

    @staticmethod
    def get_employee_db():
        """Reads the csv and puts it in a pandas dataframe
        :param: None
        :return df: (Data Frame) a pandas dataframe
        """

        df = pd.read_csv('EmployeeData.csv')

        return df

    @staticmethod
    def print_all_employees_employed(dframe):
        """Shows the current Donors
        :param donor_db: (Dictionary) dictionary of dictionaries containing all donors info
        :return: nothing
        """

        newdf = dframe[(dframe.EndDate == 'None')]

        print(tabulate(newdf, headers='keys', tablefmt='psql', showindex=False))

    @staticmethod
    def print_employees_departures(dframe):
        """Displays a list of employees that have left the company in the past 30 days
        :param dframe: (Pandas DataFrame) A DataFrame that contains employee information
        :return: nothing
        """

        df = dframe[(dframe.EndDate != 'None')]

        newdf=df.copy()

        newdf["EndDate"] = pd.to_datetime(newdf["EndDate"])

        date = datetime.datetime.today().replace(microsecond=0)

        df_filter = newdf[newdf.EndDate > date - pd.to_timedelta("30day")]

        print(tabulate(df_filter, headers='keys', tablefmt='psql', showindex=False))

    @staticmethod
    def print_review_reminders(dframe):
        """Displays a list of employees that have left the company in the past 30 days
        :param dframe: (Pandas DataFrame) A DataFrame that contains employee information
        :return: nothing
        """

        df = dframe[(dframe.EndDate == 'None')]

        newdf=df.copy()

        newdf["StartDate"] = pd.to_datetime(newdf["StartDate"])

        date = datetime.datetime.today().replace(microsecond=0)

        df_filter = newdf[newdf.StartDate > date - pd.to_timedelta("365day")]

        print(tabulate(df_filter, headers='keys', tablefmt='psql', showindex=False))

    @staticmethod
    def input_name_to_delete():
        """Pause program and show a message before continuing
        :param optional_message:  An optional message you want to display
        :return: nothing
        """

        while True:
            try:
                strName = str(input('Enter Full Name: ')).strip()
                if strName.isnumeric():
                    raise ValueError("Name is Numeric. Enter a valid name: ")
                elif strName == "":
                    raise ValueError("Name is empty. Enter a valid Name: ")
            except ValueError as e:
                print(e)
            else:
                break

        return strName

    @staticmethod
    def capture_employee_data(dframe):
        """Pause program and show a message before continuing
        :param optional_message:  An optional message you want to display
        :return: nothing
        """
        employeeID = Processor.generate_employee_id(dframe)
        firstName = IO.capture_first_name()
        lastName = IO.capture_last_name()
        fullName = firstName + ' ' + lastName
        address = IO.capture_address()
        ssn = IO.capture_ssn()
        dateOfBirth = IO.capture_date_of_birth()
        jobTitle = IO.capture_job_title()
        startDate = IO.capture_start_date()
        endDate = IO.capture_end_date()

        return employeeID, firstName, lastName, fullName, address, ssn, dateOfBirth, jobTitle, startDate, endDate

    @staticmethod
    def capture_first_name():
        """Pause program and show a message before continuing
        :param optional_message:  An optional message you want to display
        :return: nothing
        """
        while True:
            try:
                strText = str(input('Enter First Name: ')).strip()
                if strText.isnumeric():
                    raise ValueError("First Name is Numeric. Enter a valid First Name: ")
                elif strText == "":
                    raise ValueError("First Name is empty. Enter a valid First Name: ")
            except ValueError as e:
                print(e)
            else:
                break

        return strText

    @staticmethod
    def capture_last_name():
        """Pause program and show a message before continuing
        :param optional_message:  An optional message you want to display
        :return: nothing
        """
        while True:
            try:
                strText = str(input('Enter Last Name: ')).strip()
                if strText.isnumeric():
                    raise ValueError("Last Name is Numeric. Enter a valid Last name: ")
                elif strText == "":
                    raise ValueError("Last Name is empty. Enter a valid Last Name: ")
            except ValueError as e:
                print(e)
            else:
                break

        return strText

    @staticmethod
    def capture_address():
        """Pause program and show a message before continuing
        :param optional_message:  An optional message you want to display
        :return: nothing
        """
        while True:
            try:
                strText = str(input('Enter Address: ')).strip()
                if strText.isnumeric():
                    raise ValueError("Address is Numeric. Enter a valid address: ")
                elif strText == "":
                    raise ValueError("Address is empty. Enter a valid address: ")
            except ValueError as e:
                print(e)
            else:
                break

        return strText

    @staticmethod
    def capture_ssn():
        """Pause program and show a message before continuing
        :param optional_message:  An optional message you want to display
        :return: nothing
        """
        while True:
            try:
                strText = str(input('Enter ssn: ')).strip()
                if strText.isalpha():
                    raise ValueError("ssn is alpha. Enter a valid ssn: ")
                elif strText == "":
                    raise ValueError("ssn is empty. Enter a valid ssn: ")
            except ValueError as e:
                print(e)
            else:
                break

        return strText

    @staticmethod
    def capture_date_of_birth():
        """Pause program and show a message before continuing
        :param optional_message:  An optional message you want to display
        :return: nothing
        """
        while True:
            try:
                strText = str(input('Enter Date of Birth: ')).strip()
                if strText.isalpha():
                    raise ValueError("Date of Birth is alpha. Enter a valid date of birth: ")
                elif strText == "":
                    raise ValueError("Date of Birth is empty. Enter a valid date of birth: ")
            except ValueError as e:
                print(e)
            else:
                break

        return strText

    @staticmethod
    def capture_job_title():
        """Captures Job Title
        :param optional_message:  An optional message you want to display
        :return strText: (String) A string containing the Job Title
        """
        while True:
            try:
                strText = str(input('Enter Job Title: ')).strip()
                if strText.isnumeric():
                    raise ValueError("Job Title is Numeric. Enter a valid Job Title: ")
                elif strText== "":
                    raise ValueError("Job Title is empty. Enter a valid Job Title: ")
            except ValueError as e:
                print(e)
            else:
                break

        return strText

    @staticmethod
    def capture_start_date():
        """Pause program and show a message before continuing
        :param optional_message:  An optional message you want to display
        :return: nothing
        """
        while True:
            try:
                strText = str(input('Enter Start Date: ')).strip()
                if strText.isalpha():
                    raise ValueError("Start Date is alpha. Enter a valid start date: ")
                elif strText == "":
                    raise ValueError("Start Date is empty. Enter a valid start date: ")
            except ValueError as e:
                print(e)
            else:
                break

        return strText

    @staticmethod
    def capture_end_date():
        """Pause program and show a message before continuing
        :param optional_message:  An optional message you want to display
        :return: nothing
        """
        while True:
            try:
                strText = str(input('Enter End Date: ')).strip()
                if strText.isalpha():
                    raise ValueError("End date is alpha. Enter a valid end date: ")
                elif strText == "":
                    raise ValueError("End date is empty. Enter a valid end date: ")
            except ValueError as e:
                print(e)
            else:
                break

        return strText

# Main Body of Script  ------------------------------------------------------ #

if __name__ == "__main__":

    while True:

    # reminder for annual review can be a separate class

        print(result)
        print("Menu of Options")
        print(IO.get_menu(1))
        print(IO.get_menu(2))
        print(IO.get_menu(3))
        print(IO.get_menu(4))
        print(IO.get_menu(5))
        print(IO.get_menu(6))
        print(IO.get_menu(7))

        # menu printed

        strChoice = IO.input_menu_choice()  # Get menu option

        s = UserSelection()
        s.switch(
            strChoice
        )  # Calls the UserSelection class to handle the tasks in the menu

        IO.input_press_to_continue(strStatus)
        continue  # to show the menu
