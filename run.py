import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('my_love_sandwiches')

"""the following lines of code are to check that
 the API is working and is not needed after that purpose.
""" 
# sales = SHEET.worksheet('sales')

# data = sales.get_all_values()

# print(data)

def get_sales_data():
    """
    get sales figures input from the user 
    """
    print('Please enter sales data from the last market')
    print('Data should be six numbers, seperated by commas.')
    print('Example: 10,20,30,40,50,60\n')

    data_str = input('Enter your data here: ')
    """
    # this is to check the input data from the user and is not required.
    # print(f"The data provided is {data_str}")
    """
    sales_data = data_str.split(',')
    """
    # print(sales_data) # this is to check the variable sales_data
    # splits the data_str variable
    """
    validate_data(sales_data)

def validate_data(values):
    """
    inside the try, converts all string values to integers.
    Raises ValueError if strings cannot be converted into int,
    or if there arent exactly 6 values.
    """
    """print statement below to check that values are passed 
    to validate_data function
    print(values)   
    """
    
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f" Exactly 6 values required, You provided {len(values)}"
                )
        
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        
    


get_sales_data()