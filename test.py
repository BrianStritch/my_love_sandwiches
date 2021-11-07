def get_stock_values(data):
    print('Calculating  data ....\n')


    headings_names = SHEET.worksheet('stock').get_all_values()
    print('got past heading names lookup')
    headings = headings_names[0]
    print(headings)


    stock_values = SHEET.worksheet('stock').get_all_values()
    print('got past stock values lookup')
    stock_row = stock_values[-1]
    remaining_stock = []
    
    

    for heading, stock_value in zip(headings, stock_values):
        stock_value_dict = heading : stock_value
        remaining_stock.append(stock_value_dict)
    
    return remaining_stock