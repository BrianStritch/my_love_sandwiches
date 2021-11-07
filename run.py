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

def get_sales_data():
    """
    get sales figures input from the user
    """
    while True:
        print('Please enter sales data from the last market')
        print('Data should be six numbers, seperated by commas.')
        print('Example: 10,20,30,40,50,60\n')

        data_str = input('Enter your data here:\n')
       
        sales_data = data_str.split(',')
      
        if validate_data(sales_data):
            print('data is valid')
            break
    return sales_data

def validate_data(values):
    """
    inside the try, converts all string values to integers.
    Raises ValueError if strings cannot be converted into int,
    or if there arent exactly 6 values.
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f" Exactly 6 values required, You provided {len(values)}"
                )
        
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False

    return True

# def update_sales_worksheet(data):
#     """
#     update sales worksheet, add new row with the list data provided
#     """
#     print('Updating sales worksheet .....\n')
#     sales_worksheet = SHEET.worksheet('sales')
#     sales_worksheet.append_row(data)
#     print('Sales worksheet updated successfully.\n')

# def update_surplus_worksheet(data):
#     """
#     update surplus worksheet, add new row with the list data provided
#     """
#     print('Updating surplus worksheet .....\n')
#     surplus_worksheet = SHEET.worksheet('surplus')
#     surplus_worksheet.append_row(data)
#     print('Surplus worksheet updated successfully.\n')
#   function below update_worksheet is a refactored version of the two above

def update_worksheet(data, worksheet):
    """
    update relevant worksheet, add new row with the list data provided
    """
    print(f'Updating {worksheet} worksheet .....\n')
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f'{worksheet} worksheet updated successfully.\n')
    
def calculate_surplus_data(sales_row):
    """
    Compare sales with stock, and calculate the surplus for each data type.

    The surplus is defined as the sales figure subtracted from the stock.
    - Positive surplus indicates waste
    - Negative surplus indicates extra made when stock sold out
    """
    print('Calculating surplus data ....\n')
    stock = SHEET.worksheet('stock').get_all_values()
    stock_row = stock[-1]
    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    
    return surplus_data

def get_last_5_entries_sales():
    """
    collects columns of data from sales worksheet, collecting 
    the last 5 entries for each sandwich and returns the data
     as a list of lists
    """
    sales = SHEET.worksheet('sales')
    
    columns = []
    for ind in range(1,7):
        column = sales.col_values(ind)
        columns.append(column[-5:])  
    return columns      

def calculate_stock_data(data):
    """
    calculate the average stock for each item type, adding 10%
    """
    print('Calculating stock data ..... \n')
    new_stock_data = []
    
    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column) / len(int_column)
        stock_num = average * 1.1
        new_stock_data.append(round(stock_num))

    return new_stock_data



def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, 'sales')
    new_surplus_data = calculate_surplus_data(sales_data)    
    update_worksheet(new_surplus_data, 'surplus')
    sales_columns = get_last_5_entries_sales()
    stock_data = calculate_stock_data(sales_columns)
    update_worksheet(stock_data, 'stock')

print()

print("Welcome to Love Sandwiches data automation.\n")
stock_data = main()

# Write you code below this comment

def get_stock_values(data):
    """
    Function to display how many sandwiches to make for next market, determined by 
    stock_data values in stock worksheet
    """
    print('Make the following numbers of sandwiches for next market:\n')

    headings = SHEET.worksheet('stock').get_all_values()
    headings_names= headings[0]
    
    stock_values = SHEET.worksheet('stock').get_all_values()
    stock_row = stock_values[-1]
    
    remaining_stock = {}
    for heading, stock_value in zip(headings_names, stock_row):
        remaining_stock[heading] =  stock_value
    
    return remaining_stock 
    
stock_values = get_stock_values(stock_data)
print(stock_values)