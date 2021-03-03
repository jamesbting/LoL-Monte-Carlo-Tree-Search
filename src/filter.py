import csv

def clean_data(file_name, output_file_name, desired_columns):
    valid_length = 1150
    output_file = open(output_file_name, "w")
    with open(file_name, "r") as input_file:
        reader = csv.reader(input_file, delimiter = ',')
        first_row = True
        selected_columns = []
        i = 0
        for row in reader:
            #read first line from csv to obtain the indexes to obtain
            #store the length of the title line
            if first_row:
                selected_columns = get_selected_columns_indexes(row, desired_columns)
                print('The selected indexes are:', selected_columns)
                first_row = False
                output_file.write(','.join(get_selected_columns(row,selected_columns)))
            #read each line and write it to a seperate file
            #verify the length of the line is correct, if incorrect then next
            elif len(row) == valid_length:
                output_file.write('\n')
                output_file.write(','.join(get_selected_columns(row,selected_columns)))
                i += 1
        print('Cleaned', i, 'matches')
    output_file.close()
    print('Done filtering data.')
       
def get_selected_columns_indexes(row, desired_columns):
    selected_columns = []
    for i in range(len(row)):
        col = row[i]
        if col in desired_columns:
            selected_columns.append(i)
    return selected_columns

def get_selected_columns(row, selected_columns):
    result = []
    for i in range(len(row)):
        if i in selected_columns:
            result.append(row[i])
    head = result.pop(0)
    if(head == 'Win'):
        result.append('1')
    elif(head == 'Fail'):
        result.append('0')
    return result
