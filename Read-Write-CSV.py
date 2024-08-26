


#write a function to seprate columns from a line of csv file
def parse_csv_line(line):
    return line.strip().split(',')


#write a function to read a csv file and print the contents
def read_csv(file_name):
    with open(file_name, 'r') as file:
        for line in file:
            print(line)
            columns = parse_csv_line(line)
            print(f" First col = > {columns[0]}, last col = {columns[-1]} ")


file1 = 'Pattu_Sir_Small Cap Ratio.csv'
file2 = 'NIFTY SMALLCAP 250_Historical_PR_01042005to26032024.csv'

def read_and_process_csv(f1, f2): # f1 = file1, f2 = file2
    with open(f1, 'r') as fd1, open(f2, 'r') as fd2, open('output.csv', 'w') as output_file:
        for line in fd1:
            columns = parse_csv_line(line)
            if columns[0] == 'Date':
                #line = line + f',"","",SC250_From_NiftyFile'
                line = line.replace("\n",',"","",SC250_From_NiftyFile\n')
                output_file.write(line)
                continue
            else:
                found=False
                for line2 in fd2:
                    columns2 = parse_csv_line(line2)
                    if columns[0] == columns2[1]:
                        found=True
                        line = line.replace("\n",f',"","",{columns2[-1]}\n')
                        output_file.write(line)
                        break
                if not found:
                    print(f"Could not find {columns[0]} in {f2}")
                #fd2.seek(0)
            #columns = parse_csv_line(line)
            

#read_csv('Pattu_Sir_Small Cap Ratio.csv')
read_and_process_csv(file1,file2)



