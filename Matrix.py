req_num = int(input())
matrix = open('input.txt', 'r')
print(type(matrix))
try:
    indexes = [[row_index, column_index] for row_index, row in enumerate(matrix)
               for column_index, num in enumerate(row.split(' '))
               if int(num) == req_num]

    row_i = sorted(set([i[0] for i in indexes]))
    col_i = sorted(set([i[1] for i in indexes]))

    print(f'Required number = {req_num}')
    print("Rows (index): ", end='')
    for i in row_i:
        print(i, end=" ")
    print("\nColumns (index): ", end='')
    for i in col_i:
        print(i, end=" ")
except:
    print("Something wrong")
finally:
    matrix.close()
