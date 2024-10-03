""" Writen by Rafael Rayes, Tangly will help you transforming
a list into a table.
USAGE:


>>> import tangly

>>> people = [["Name", "Last Name", 'Age', "Number"],
	   ["Nath", "Dezem", '20', '137'],
	   ["Rafa", "Rayes",'19', '4976'],
       ['Johny', 'Dias', '22', '1234']]

>>> tangly.print_table(my_list)


┌───────┬──────────────────────────┐
│ Name  │ Last Name   Age   Number │
├───────┼──────────────────────────┤
│ Nath  │ Dezem       20    137    │
│ Rafa  │ Rayes       19    4976   │
│ Johny │ Dias        22    1234   │
└───────┴──────────────────────────┘
"""
def make_table(your_list, separators=[[0], [0]]):
    num_columns = len(your_list[0])
    columns_lengths = [max(len(str(x)) for x in col) for col in zip(*your_list)]
    separators_horizontals = separators[0]
    separators_verticals = separators[1]

    row_template = '│'  # Begin the row with the left border
    for i in range(num_columns):
        row_template += f" {{:<{columns_lengths[i]}}} "  # Add the column placeholder
        if i in separators_verticals:  # Add a separator if it's in the specified vertical indices
            row_template += '│'
        else:
            row_template += ' '  # Add a space if it's not a separator
    row_template = row_template[:-1] + '│'  # Replace the last space with the right border
    
    # define the separator rows
    separator_list = ['─'*(length) for length in columns_lengths]
    

    # define the top and bottom of the table
    top = row_template.format(*separator_list)
    top = top.replace('│', '┌', 1).replace('│', '┬', len(separators_verticals)).replace('│', '┐').replace(' ', '─')
    bottom = top.replace('┌', '└').replace('┬', '┴').replace('┐', '┘')
    
    separator_row = top.replace('┌', '├').replace('┬', '┼').replace('┐', '┤')


    printable_rows = []
    printable_rows.append(top)
    for i , row in enumerate(your_list):
        if len(row) != num_columns:
            raise ValueError('All rows must have the same number of columns')
        printable_rows.append(row_template.format(*row))
        if i in separators_horizontals: # Add a separator if needed
            printable_rows.append(separator_row)
    printable_rows.append(bottom)
    table = '\n'.join(printable_rows)
    return table
def print_table(your_list, separators=[[0], [0]]):
    table = make_table(your_list, separators)
    print(table)
def make_table(your_list, separators=[[0], [0]]):
    print_table(your_list, separators)
name = 'Tangly'
version = '2.1.4'
