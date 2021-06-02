import sys
import pyfiglet
import pandas as pd
import numpy as np
from tabulate import tabulate
import dateutil
import datetime
import re

result = pyfiglet.figlet_format("h r  s y s t e m", font="slant")
strStatus = ""


class UserSelection:
    """Handles User Selection Logic
    the class is used to implement a case-switch construct in python
    """

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

        (
            employeeID,
            firstName,
            lastName,
            fullName,
            address,
            ssn,
            dateOfBirth,
            jobTitle,
            startDate,
            endDate,
        ) = IO.capture_employee_data(IO.get_employee_db())

        df = Processor.append_row(
            IO.get_employee_db(),
            employeeID,
            firstName,
            lastName,
            fullName,
            address,
            ssn,
            dateOfBirth,
            jobTitle,
            startDate,
            endDate,
        )

        Processor.append_to_csv(df)

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
    """Performs Processing tasks"""

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
        """Writes the filtered DataFrame to a csv file.
        This method is used when the user decides to delete record
        :param dframe: (Pandas DataFrame) DataFrame containing employee information
        :return: nothing
        """

        dframe.to_csv("EmployeeData.csv", index=False)

    @staticmethod
    def generate_employee_id(dframe):
        """Generates unique employee id for the next employee to be added
        :param dframe: (Pandas DataFrame) DataFrame containing employee information
        :return next_id: (Integer) Next ID to be used for an employee record
        """
        max_id = dframe["EmployeeID"].max()
        next_id = max_id + 1

        return next_id

    @staticmethod
    def append_row(
        df, id, first, last, full, address, ssn, dob, job, startDate, endDate
    ):
        """Generates a row of data to be appended to a pandas DataFrame
        :param dframe: (Pandas DataFrame) DataFrame containing employee information
        :param id: (Integer) Next ID to be used for an employee record
        :param first: (String) First Name to be used for an employee record
        :param last: (String) Last Name to be used for an employee record
        :param full: (String) Full Name to be used for an employee record
        :param address: (String) Address to be used for an employee record
        :param ssn: (String) Social Security Number to be used for an employee record
        :param dob: (String) Date of Birth to be used for an employee record
        :param job: (String) Job Title to be used for an employee record
        :param startDate: (String) Start Date to be used for an employee record
        :param endDate: (String) End Date to be used for an employee record
        :return df: (Pandas DataFrame) a new Pandas DataFrame to be written to a csv
        """

        new_row = {
            "EmployeeID": id,
            "FirstName": first,
            "LastName": last,
            "FullName": full,
            "Address": address,
            "ssn": ssn,
            "DateOfBirth": dob,
            "JobTitle": job,
            "StartDate": startDate,
            "EndDate": endDate,
        }

        # append row to the dataframe

        df = df.append(new_row, ignore_index=True)

        return df

    @staticmethod
    def append_to_csv(df):
        """Writes a new DataFarme to the csv file.
        This method is used when the user decides to add a new record to the csv
        :param df: (Pandas DataFrame) DataFrame containing employee information
        :return: nothing
        """

        df.to_csv("EmployeeData.csv", index=False)

    @staticmethod
    def isValidSSN(str):
        """Validates the social security format
        :param str: (String) string that represents the social security number
        :return: (Boolean)
        """
        # This code is contributed by avanitrachhadiya2155
        # Regex to check valid
        # SSN (Social Security Number).
        regex = "^(?!666|000|9\\d{2})\\d{3}-(?!00)\\d{2}-(?!0{4})\\d{4}$"

        # Compile the ReGex
        p = re.compile(regex)

        # If the string is empty
        # return false
        if str == None:
            return False

        # Return if the string
        # matched the ReGex
        if re.search(p, str):
            return True
        else:
            return False


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
        """Displays all employees
        :param dframe: (Pandas DataFrame) a Pandas DataFrame containing all employee info.
        :return: nothing
        """
        IO.print_header()
        print("List of all employees: ")
        IO.print_footer()

        df = dframe.copy()

        df["StartDate"] = pd.to_datetime(df["StartDate"])

        print(tabulate(df, headers="keys", tablefmt="psql", showindex=False))

    @staticmethod
    def get_employee_db():
        """Reads the csv and puts it in a pandas dataframe
        :param: None
        :return df: (Data Frame) a pandas dataframe
        """

        df = pd.read_csv("EmployeeData.csv")

        return df

    @staticmethod
    def print_all_employees_employed(dframe):
        """Displays the employees currently employed at the company
        :param dframe: (Pandas DataFrame) DataFrame containing employee information
        :return: nothing
        """
        # Filter out those employees who have left.
        # That is, the ones that have a real 'EndDate'
        # The employees currently employed have EndDate = None

        newdf = dframe[(dframe.EndDate == "NONE")]
        df = newdf.copy()
        df["StartDate"] = pd.to_datetime(df["StartDate"])

        IO.print_header()
        print("List of all employees currently employed: ")
        IO.print_footer()
        print(tabulate(df, headers="keys", tablefmt="psql", showindex=False))

    @staticmethod
    def print_employees_departures(dframe):
        """Displays a list of employees that have left the company in the past 30 days
        :param dframe: (Pandas DataFrame) A DataFrame that contains employee information
        :return: nothing
        """

        # Filter out those employees who have NOT left.
        # That is, the ones that have EndDate = None
        # The employees who have left have EndDate = xx/xx/xxxx

        df = dframe[(dframe.EndDate != "NONE")]

        newdf = df.copy()

        newdf["EndDate"] = pd.to_datetime(newdf["EndDate"])

        date = datetime.datetime.today().replace(microsecond=0)

        df_filter = newdf[newdf.EndDate > date - pd.to_timedelta("30day")]

        IO.print_header()
        print("List of all employees who have left the company in the past 30 days: ")
        IO.print_footer()
        print(tabulate(df_filter, headers="keys", tablefmt="psql", showindex=False))

    @staticmethod
    def print_review_reminders(dframe):
        """Displays a list of employees that have left the company in the past 30 days
        :param dframe: (Pandas DataFrame) A DataFrame that contains employee information
        :return: nothing
        """

        df = dframe[(dframe.EndDate == "NONE")]

        newdf = df.copy()

        date = datetime.datetime.today().replace(microsecond=0)

        newdf["StartDate"] = pd.to_datetime(newdf["StartDate"])

        newdf['Month'] = pd.DatetimeIndex(newdf['StartDate']).month

        newdf['Day'] = pd.DatetimeIndex(newdf['StartDate']).day

        newdf['CalendarYear'] = date.year

        newdf['DateForReview'] = pd.to_datetime((newdf.CalendarYear * 10000 + newdf.Month * 100 + newdf.Day).apply(str),
                                                format='%Y%m%d')

        df_filter = newdf[(newdf.DateForReview - pd.to_timedelta("90days") < date) & (newdf.DateForReview >= date)]

        df_df = df_filter.drop(['Month', 'Day', 'CalendarYear'], axis=1)

        IO.print_header()

        print('FRIENDLY REMINDER! Anual Reviews are coming up for the following employees: ')

        IO.print_footer()

        print(tabulate(df_df, headers="keys", tablefmt="psql", showindex=False))

    @staticmethod
    def input_name_to_delete():
        """Captures the name of the employee to delete
        :param:  None
        :return strName: (String) String containing the full name of the person
        """

        while True:
            try:
                strName = str(input("Enter Full Name: ")).strip()
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
        """Captures employee data for new record
        :param dframe: (Pandas DataFrame) a DataFrame with employee info
        :return employeeID: (Integer) Unique Employee ID
        :return firstName: (String) First Name
        :return lastName: (String) Last Name
        :return fullName: (String) Full Name
        :return address: (String) Address
        :return ssn: (String) Social Security Number
        :return dateOfBirth: (String) Date of Birth
        :return jobTitle: (String) Job Title
        :return startDate: (String) Start Date
        :return endDate: (String) End Date
        """
        employeeID = Processor.generate_employee_id(dframe)
        firstName = IO.capture_first_name()
        lastName = IO.capture_last_name()
        fullName = firstName + " " + lastName
        address = IO.capture_address()
        ssn = IO.capture_ssn()
        dateOfBirth = IO.capture_date_of_birth()
        jobTitle = IO.capture_job_title()
        startDate = IO.capture_start_date()
        endDate = IO.capture_end_date()

        return (
            employeeID,
            firstName,
            lastName,
            fullName,
            address,
            ssn,
            dateOfBirth,
            jobTitle,
            startDate,
            endDate,
        )

    @staticmethod
    def capture_first_name():
        """Captures First Name
        :param:  None
        :return: Nothing
        """
        while True:
            try:
                strText = str(input("Enter First Name: ")).strip()
                if strText.isnumeric():
                    raise ValueError(
                        "First Name is Numeric. Enter a valid First Name: "
                    )
                elif strText == "":
                    raise ValueError("First Name is empty. Enter a valid First Name: ")
            except ValueError as e:
                print(e)
            else:
                break

        return strText

    @staticmethod
    def capture_last_name():
        """Captures Last Name
        :param:  None
        :return: Nothing
        """
        while True:
            try:
                strText = str(input("Enter Last Name: ")).strip()
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
        """Captures Address
        :param:  None
        :return: Nothing
        """
        while True:
            try:
                strText = str(input("Enter Address: ")).strip()
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
        """Captures Social Security Number
        :param:  None
        :return: Nothing
        """
        while True:
            try:
                strText = str(input("Enter ssn (000-00-0000): ")).strip()
                if Processor.isValidSSN(strText) == False:
                    raise ValueError(
                        "ssn is not in the proper format. Enter a valid ssn: "
                    )
                elif strText == "":
                    raise ValueError("ssn is empty. Enter a valid ssn: ")
            except ValueError as e:
                print(e)
            else:
                break

        return strText

    @staticmethod
    def capture_date_of_birth():
        """Captures Date of Birth
        :param:  None
        :return: Nothing
        """
        formt = "%m/%d/%Y"
        while True:
            try:
                strText = str(
                    input("Enter Date of Birth, MM/DD/YYYY (%m/%d/%Y): ")
                ).strip()
                res = bool(datetime.datetime.strptime(strText, formt))

            except ValueError as e:
                print(e)

            else:
                break

        return strText

    @staticmethod
    def capture_job_title():
        """Captures Job Title
        :param:  None
        :return: Nothing
        """
        while True:
            try:
                strText = str(input("Enter Job Title: ")).strip()
                if strText.isnumeric():
                    raise ValueError("Job Title is Numeric. Enter a valid Job Title: ")
                elif strText == "":
                    raise ValueError("Job Title is empty. Enter a valid Job Title: ")
            except ValueError as e:
                print(e)
            else:
                break

        return strText

    @staticmethod
    def capture_start_date():
        """Captures Start Date
        :param:  None
        :return: Nothing
        """
        formt = "%m/%d/%Y"
        while True:
            try:
                strText = str(
                    input("Enter Start Date, MM/DD/YYYY (%m/%d/%Y): ")
                ).strip()
                res = bool(datetime.datetime.strptime(strText, formt))

            except ValueError as e:
                print(e)

            else:
                break

        return strText

    @staticmethod
    def capture_end_date():
        """Captures End Date
        :param:  None
        :return: Nothing
        """
        formt = "%m/%d/%Y"

        while True:

            strText = (
                str(input("Enter End Date, MM/DD/YYYY (%m/%d/%Y): ")).strip().upper()
            )

            if strText != "NONE":
                try:

                    res = bool(datetime.datetime.strptime(strText, formt))

                except ValueError as e:
                    print(e)

                else:
                    break
            else:
                break

        return strText

    @staticmethod
    def activate_reminders(dframe):
        """Activate the reminders
        :param:  None
        :return: Nothing
        """

        IO.print_review_reminders(dframe)

    @staticmethod
    def print_header():
        """Prints the header of the report
        :param: None
        :return: nothing
        """
        print(
            "+--------------+-------------+------------+--------------"
            "+-----------+-------------+---------------+------------"
            "+---------------------+-----------+"
        )

    @staticmethod
    def print_footer():
        """Prints the footer of the report
        :param: None
        :return: nothing
        """

        print(
            "+--------------+-------------+------------+--------------"
            "+-----------+-------------+---------------+------------"
            "+---------------------+-----------+"
        )


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

        IO.activate_reminders(IO.get_employee_db())

        # menu printed

        strChoice = IO.input_menu_choice()  # Get menu option

        s = UserSelection()
        s.switch(
            strChoice
        )  # Calls the UserSelection class to handle the tasks in the menu

        IO.input_press_to_continue(strStatus)
        continue  # to show the menu
