import hr_system.hr_system
import pandas as pd
from pandas._testing import assert_frame_equal


# next employee id testing


def test_next_id():
    df = pd.read_csv("src\hr_system\EmployeeData.csv")
    assert hr_system.hr_system.Processor.generate_employee_id(df) == 10000009


# pandas data frame testing


def test_pandas_dfs():
    id = 10000009
    first = "Mark"
    last = "Z"
    full = "Mark Z"
    address = "Menlo Park"
    ssn = "111-11-1115"
    dob = "01/01/1970"
    job = "Rich Man"
    startDate = "12/01/2020"
    endDate = "None"
    df = pd.read_csv("src\hr_system\EmployeeData.csv")

    dframe = hr_system.hr_system.Processor.append_row(
        df, id, first, last, full, address, ssn, dob, job, startDate, endDate
    )
    data_frame = pd.DataFrame(
        {
            "EmployeeID": [
                10000001,
                10000002,
                10000003,
                10000004,
                10000005,
                10000006,
                10000007,
                10000008,
                10000009,
            ],
            "FirstName": [
                "Pablo",
                "Beavis",
                "BHead",
                "Beatrix",
                "Butters",
                "Jeff",
                "Bill",
                "Bill",
                "Mark",
            ],
            "LastName": [
                "Marcel",
                "Judge",
                "Judge",
                "T",
                "S",
                "Bezos",
                "T",
                "Gates",
                "Z",
            ],
            "FullName": [
                "Pablo Marcel",
                "Beavis Judge",
                "BHead Judge",
                "Beatrix T",
                "Butters S",
                "Jeff Bezos",
                "Bill T",
                "Bill Gates",
                "Mark Z",
            ],
            "Address": [
                "Bothell",
                "Vegas",
                "Vegas",
                "L.A.",
                "Denver",
                "Seattle",
                "L.A.",
                "L.A.",
                "Menlo Park",
            ],
            "ssn": [
                "444-44-4444",
                "666-66-6666",
                "666-66-6667",
                "111-11-1111",
                "111-11-1112",
                "000-00-0000",
                "111-11-1113",
                "111-11-1114",
                "111-11-1115",
            ],
            "DateOfBirth": [
                "01/01/1901",
                "01/01/1980",
                "01/01/1980",
                "01/01/1970",
                "01/01/1970",
                "01/01/1900",
                "01/01/1970",
                "01/01/1970",
                "01/01/1970",
            ],
            "JobTitle": [
                "Rock Star",
                "General",
                "Judge",
                "Assasin",
                "Professor",
                "Boss",
                "Assasin",
                "Rich Man",
                "Rich Man",
            ],
            "StartDate": [
                "07/31/2020",
                "01/01/1995",
                "01/01/1995",
                "07/31/2020",
                "01/01/2000",
                "01/01/1950",
                "07/31/2020",
                "12/01/2020",
                "12/01/2020",
            ],
            "EndDate": [
                "None",
                "05/15/2021",
                "05/15/2021",
                "None",
                "01/01/2000",
                "01/01/2021",
                "None",
                "None",
                "None",
            ],
        }
    )

    assert_frame_equal(dframe, data_frame)
