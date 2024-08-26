
import math


file1 = 'Average_N50_NSC250.csv'
SCALING_VALUE = 0.415463553
PEAK_GRAPH_VAL = 20000


#write a function to seprate columns from a line of csv file
def parse_csv_line(line):
    return line.strip().split(',')


def replace_commas_and_newlines_chars_from_line(line):
    columns = parse_csv_line(line)
    sentence=''
    for item in columns:
        if item == '' or item == '\n':
            break
        else:
            sentence = sentence + item + ','
    
    sentence = sentence[0:-1]
    #sentence = sentence + '\n'
    return sentence


def parse_date_to_get_month(line):
    columns = line.strip().split('-')
    return columns[1]



def read_and_process_csv(f1): # f1 = file1
    last_month="undefined"
    signal_val=0
    last_three_ratios=0
    agrigating_for=1
    with open(f1, 'r') as fd1, open('output.csv', 'w') as output_file:
        for line in fd1:
            line = replace_commas_and_newlines_chars_from_line(line)
            #print(f" read : {line} ")
            columns = parse_csv_line(line.strip())
            if columns[0] == 'Date':
                
                line = line + ',' + 'signal\n'
                output_file.write(line)
                continue
            else:
                cmonth=parse_date_to_get_month(columns[0])
                if cmonth != last_month:
                    ratio = int(eval(columns[4]))
                    not_of_signal_val = not signal_val
                    if ratio == not_of_signal_val:
                        last_three_ratios = last_three_ratios + 1
                    else:
                        last_three_ratios =0

                    if last_three_ratios >=3:
                        signal_val= not signal_val
                        last_three_ratios=0

                    if  signal_val == 0:
                        line = line + ',' + '0' + '\n'
                    else:
                        line = line + ',' + '1' + '\n'
                    output_file.write(line)
                    last_month=cmonth


            

#read_csv('Pattu_Sir_Small Cap Ratio.csv')
#read_and_process_csv(file1)


def writefirsttwolines_10MMA(line_num,line250,line50,output_file,NSC250_sliding_window_10MMA,N50_sliding_window_100MMA):
    scaleling_value=0
    if line_num == 1:
        out_line = "Date" + "," + "NSC250TRI" + "," + "N50TRI" + "," + "ScaledN50TRI" + "," + \
                   "10MMA_SC250" + "," + "10MMA_N50" + "," + "Ratio(SC250/ScaledN50)" + "\n"
        output_file.write(out_line)
    elif line_num == 2:
        columns250 = parse_csv_line(line250.strip())
        columns50 = parse_csv_line(line50.strip())
        NC250_int = float(columns250[2])
        N50_int = float(columns50[2])
        scaleling_value=NC250_int/N50_int
        out_line = columns250[1] + "," + columns250[2] + "," + columns50[2] + "," + columns250[2] + "," + \
                   "0" + "," + "0" + "," + "1" + "\n"
        NSC250_sliding_window_10MMA[0]=NC250_int
        N50_sliding_window_100MMA[0]=NC250_int
        output_file.write(out_line)
    
    return scaleling_value
	

def writefirsttwolines_ratio(line_num,line250,line50,output_file):
    scaleling_value=0
    if line_num == 1:
        out_line = "Date" + "," + "NSC250TRI" + "," + "N50TRI" + "," + "Ratio" + "," + "Signal_sell_smallcap" + "\n"
        output_file.write(out_line)
    elif line_num == 2:
        columns250 = parse_csv_line(line250.strip())
        columns50 = parse_csv_line(line50.strip())
        NC250_int = float(columns250[2])
        N50_int = float(columns50[2])
        scaleling_value=NC250_int/N50_int
        out_line = columns250[1] + "," + columns250[2] + "," + columns250[2] + "," + "1" + "," + "0" + "\n"
        output_file.write(out_line)
    
    return scaleling_value


def calculate_signal_ratio(indicies_ratio,last_three_ratios_g,last_three_ratios_l,signal_val):
    #signal caculations
    if indicies_ratio> 1.3: 
        last_three_ratios_g=last_three_ratios_g+1
        last_three_ratios_l=0
        if last_three_ratios_g >= 3:
            if signal_val==0: #till now we are buying SC
                signal_val=1  #sell small cap now
            else: # sell is already triggered, nothing to do
                pass
        else: #greater value has come for less than 3 months so nothing to be done
            pass
    else:   #ratio has become less so, we need to buy
        last_three_ratios_l=last_three_ratios_l+1
        last_three_ratios_g=0
        if last_three_ratios_l >= 3:
            if signal_val==1: #till now we are selling SC
                signal_val=0  #buy small cap now
            else: # buy is already triggered, nothing to do
                pass
        else: #less value has come for less than 3 months so nothing to be done
            pass
    
    return last_three_ratios_g,last_three_ratios_l,signal_val





def process_orignal_files_NSC250_N50_Ratio_buy_Sell(NSC250_CSV_File,N50_CSV_File):
    with open(NSC250_CSV_File, 'r') as fd1, open(N50_CSV_File, 'r') as fd2, open('NSC250_N50_Ratio_buy_Sell.csv', 'w') as output_file:
        line_num=0 
        scaleling_value = 0
        last_month="undefined"
        signal_val=0
        last_three_ratios_g=0
        last_three_ratios_l=0
        for line250, line50 in zip(fd1, fd2):
            line_num = line_num + 1
            if line_num < 3:
                scaleling_value=writefirsttwolines_ratio(line_num,line250,line50,output_file)
            else:
                columns250 = parse_csv_line(line250.strip())
                columns50 = parse_csv_line(line50.strip())
                cmonth=parse_date_to_get_month(columns250[1])
                if cmonth != last_month:
                    scaled_N50=scaleling_value*float(columns50[2])
                    indicies_ratio=float(columns250[2])/scaled_N50
                    #Find Signal
                    last_three_ratios_g,last_three_ratios_l,signal_val = calculate_signal_ratio(indicies_ratio=indicies_ratio,
                                              last_three_ratios_g=last_three_ratios_g,
                                              last_three_ratios_l=last_three_ratios_l,
                                              signal_val=signal_val)
                    out_line = columns250[1] + "," + columns250[2] + "," + str(scaled_N50) + "," + str(indicies_ratio) + "," + str(signal_val*PEAK_GRAPH_VAL) + "\n"
                    output_file.write(out_line)
                    last_month=cmonth




def process_orignal_files_NSC250_N50_10MMA_buy_Sell(NSC250_CSV_File,N50_CSV_File,OnlyMonthlyValues=False):
    with open(NSC250_CSV_File, 'r') as fd1, open(N50_CSV_File, 'r') as fd2, open('NSC250_N50_10MMA_buy_Sell.csv', 'w') as output_file:
        #Format :: "Date, NSC250TRI, N50TRI, ScaledN50TRI, 10MMA_SC250, 10MMA_N50, Ratio(SC250/ScaledN50)"
        line_num = scaleling_value = MMA10_SC250 = MMA10_N50 = SUM_SC250_10MMA = SUM_N50_10MMA = 0
        MMA12_SC250 = MMA12_N50 = SUM_SC250_12MMA = SUM_N50_12MMA = 0
        MMA6_SC250 = MMA6_N50 = SUM_SC250_6MMA = SUM_N50_6MMA = 0
        lenght_of_sliding_window_10mma=220
        lenght_of_sliding_window_12mma=310
        lenght_of_sliding_window_6mma=155
        out_line=""
        cmonth=lmonth="undefined"
        N50_sliding_window_100MMA=[0.0]*(lenght_of_sliding_window_10mma+10)
        SC250_sliding_window_10MMA=[0.0]*(lenght_of_sliding_window_10mma+10)
        for line250, line50 in zip(fd1, fd2):
            line_num = line_num + 1
            if line_num < 3:
                scaleling_value=writefirsttwolines_10MMA(line_num,line250,line50,output_file,SC250_sliding_window_10MMA,N50_sliding_window_100MMA)
                SUM_SC250_10MMA+=SC250_sliding_window_10MMA[0]
                SUM_N50_10MMA+=N50_sliding_window_100MMA[0]
                continue
            else:
                columns250 = parse_csv_line(line250.strip())
                columns50 = parse_csv_line(line50.strip())
                scaled_N50=scaleling_value*float(columns50[2])
                indicies_ratio=float(columns250[2])/scaled_N50
                cmonth=parse_date_to_get_month(columns250[1])
                if line_num-2 >= lenght_of_sliding_window_10mma:
                    MMA10_SC250=math.ceil(SUM_SC250_10MMA/lenght_of_sliding_window_10mma)
                    MMA10_N50=math.ceil(SUM_N50_10MMA/lenght_of_sliding_window_10mma)
                    out_line = columns250[1] + "," + columns250[2] + "," + columns50[2] + "," + \
                               str(scaled_N50) + "," + str(MMA10_SC250) + "," + str(MMA10_N50) + \
                               "," + str(indicies_ratio) + "\n"
                    ID_at_work=(line_num-2-lenght_of_sliding_window_10mma) % lenght_of_sliding_window_10mma
                    SUM_N50_10MMA=(SUM_N50_10MMA-N50_sliding_window_100MMA[ID_at_work])+scaled_N50
                    SUM_SC250_10MMA=(SUM_SC250_10MMA-SC250_sliding_window_10MMA[ID_at_work])+float(columns250[2])
                    SC250_sliding_window_10MMA[ID_at_work]=float(columns250[2])
                    N50_sliding_window_100MMA[ID_at_work]=scaled_N50
                else:
                    ID_at_work=line_num-2
                    N50_sliding_window_100MMA[ID_at_work]=scaled_N50
                    SC250_sliding_window_10MMA[ID_at_work]=float(columns250[2])
                    SUM_SC250_10MMA+=SC250_sliding_window_10MMA[ID_at_work]
                    SUM_N50_10MMA+=N50_sliding_window_100MMA[ID_at_work]
                    out_line = columns250[1] + "," + columns250[2] + "," + columns50[2] + "," + \
                               str(scaled_N50) + "," + "0" + "," + "0" + "," + str(indicies_ratio) + "\n"
            if OnlyMonthlyValues == True:
                if lmonth != cmonth:
                    output_file.write(out_line)
                    lmonth=cmonth
            else:
                output_file.write(out_line)






def main():
    
    #if we want to process historical data at once then
    # Pass NSC250 and N50 csv file with data {format :  "IndexName","Date","Total Returns Index"}
    # Result will be a file with NSC250 orignal and N50 Scaled values and Signal column {format : Date,Smallcap 250 TRI,NIfty 50 TRI,Ratio,Signal }
    #
    file1 = "N50_TRI_Historical_TR_01042005to22082024.csv"
    file2 = "NSC250_Historical_TR_01042005to22082024.csv"
    process_orignal_files_NSC250_N50_Ratio_buy_Sell(file2,file1)
    process_orignal_files_NSC250_N50_10MMA_buy_Sell(file2,file1,True)


    
    #if we want to process already signal generated data then
    # Pass result file with data {{format : Date,Smallcap 250 TRI,NIfty 50 TRI,Ratio,Signal }
    # and the rowid from which new data has been added. 
    #
    #process_target_file(file1,start_rowid, scaling_value)


if __name__ == "__main__":
    main()