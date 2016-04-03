#################################
## 1. Load the external raw data
#################################

import pandas as pd
import numpy as np
import xlrd # read http://www.sitepoint.com/using-python-parse-spreadsheet-data/
import xlwt # write 
from sas7bdat import SAS7BDAT
from math import log10

path_output = 'D:\\Gavin\\output\\'

def load_raw_data(path   = 'D:\\Gavin\\data\\'
                 ,infile = 'document.txt'
				 ,sep = ','
				 ,**parameters):
    """
    Load the external data
    The data format could be *.txt/csv/xlsx/sas7bdat
    """
    # (1) .txt / .csv 
    if infile.rfind('.txt') > 0 or infile.rfind('.csv') > 0 :
        try:
            data = pd.read_csv(path + infile, sep=sep)    
            return data
        except OSError:
            print('OSError: ', path, infile, 'does not exist')
        except UnicodeDecodeError:
            print('UnicodeDecodeError: ', 'please save your data as UTF-8 file')
    elif infile.rfind('.xlsx') > 0 or infile.rfind('.xls') > 0 :		
    # (2) .xlsx 
        try:	
            workbook = xlrd.open_workbook(path + infile)
            sheet = workbook.sheet_by_name(**parameters)
            #worksheet = workbook.sheet_by_index(0)
            table = {}
            for col in range(sheet.ncols):
                values = []
                for row in range(sheet.nrows):
                    values.append(sheet.cell(row, col).value)
                table[col] = values

            tmp = pd.DataFrame(table)
            data = tmp.loc[1:, :]
            data.columns = tmp.loc[0, :]
            return data
        except FileNotFoundError:
            print('FileNotFoundError: ', 'file does not exist.')
    elif infile.rfind('.sas7bdat') > 0:
    # (3) .sas7dat
        try: 
            data = SAS7BDAT(path + infile).to_data_frame()
            return data 
        except FileNotFoundError:
            print('FileNotFoundError:', 'The file does not exist.')
    else:
        print('WARNING: The function does not support the data format for the data', infile)
        pass 
		
#data = load_raw_data(infile = "kuake_dectree_v2.csv")    
#data = load_raw_data(infile = "fd_sample.txt", sep='\t')    
#data = load_raw_data(infile = "test1.xlsx", sheet_name = 'Sheet1')    
#data = load_raw_data(infile = "raw_woe_train.sas7bdat") 
data = load_raw_data(infile = "BJ_DATA1.xls", sheet_name = 'no_deal')  # 3523, 25


def var_profile_miss_rate(indata = ''):
    """
    Missing rate for both category & numeric variables 
    """
    cnt_miss = indata.isnull().sum() 	
    nan_rate_fnl = pd.DataFrame({ 'var':       [x for x in cnt_miss.index]
	                             ,'cnt_miss':  [x for x in cnt_miss]
                                 ,'miss_rate': [x / indata.shape[0] * 100 for x in cnt_miss]
								 ,'var_type':  ['character' if str(x) == 'object' else 'numeric' for x in indata.dtypes]
	                            })
    nan_rate_fnl['total'] = indata.shape[0]
    nan_rate_fnl = nan_rate_fnl.sort_values(by='miss_rate', ascending=False)  # sort the data by miss_rate desc 
    return(nan_rate_fnl[['var', 'var_type', 'total', 'cnt_miss', 'miss_rate']])   

var_profile_miss_rate(data)
		
		
		
def write_to_xls(sheet='', outdata=''):
    for row in range(outdata.shape[0] + 1):
        for col in range(outdata.shape[1] + 1):
            if row == 0 and col == 0:
                sheet.write(row, col, '')
            elif row == 0:
                sheet.write(row, col, outdata.columns[col - 1])
            elif row > 0 and col == 0:
                sheet.write(row, col, outdata.index[row - 1])
            else:
                sheet.write(row, col, outdata.iloc[row - 1, col - 1])
				
				
def var_profile_freq_dist(indata = ''):
    """
    1. Frequency for category variables 
    2. Distribution for numeric variables 
    """
    dattr = pd.DataFrame({'variable': [x for x in indata.columns]
	                     ,'type':     ['character' if str(x) == 'object' else 'numeric' for x in indata.dtypes]
						 })
    cate_lgc = dattr['type'] == 'character'
    var_cate, var_num = [x for x in dattr.loc[ cate_lgc, 'variable']], [x for x in dattr.loc[-cate_lgc, 'variable']]
	  
    """	
	1. Frequency for category variables
       Output 4 columns: var/ value/ count/ pct 
    """	
    res_cate = pd.DataFrame() 	
    for i in range(len(var_cate)):
        freq = pd.DataFrame(indata[var_cate[i]].value_counts()).astype('float64')
        freq['value'] = freq.index
        freq['var']   = var_cate[i]		
        freq.columns  = ['count', 'value', 'var']
        freq['pct']   = [x / indata.shape[0] for x in freq['count']] 
		
        res_cate = pd.concat([res_cate, freq])
		
    res_cate.index = [str(i) for i in range(res_cate.shape[0])]
    res_cate = res_cate[['var', 'value', 'count', 'pct']]	
			
    """
    2. Distribution for numeric variables 
    """ 
    #tmp = indata[var_num].describe()        	
    res_num = pd.DataFrame(np.percentile(indata[var_num], [0, 5, 25, 50, 75, 95, 99, 100], axis=0)
                          ,columns = var_num
                          ,index   = ['min', 'P5', 'P25', 'P50', 'P75', 'P95', 'P99', 'max']).transpose()
    	
    
	
    ## Output the final results: res_cate & res_num 
    #res_cate.to_excel(path_output + 'result_category_numeric.xlsx', sheet_name='Category')
    #res_num.to_excel(path_output  + 'result_category_numeric.xlsx', sheet_name='Numeric')    
    workbook = xlwt.Workbook()
    sheet_cate = workbook.add_sheet('Category')
    write_to_xls(sheet=sheet_cate, outdata=res_cate)
	
    sheet_num = workbook.add_sheet('Numeric')
    write_to_xls(sheet=sheet_num, outdata=res_num)
	
    workbook.save(path_output + 'result_category_numeric_freq_and_dist.xls')
	
	
def var_profile(indata=''):
    """
    Output the variable profile, including the the parts below:
    (1) Data type & missing rate 
    (2) Freq for category, Distribution for numeric 	
	(3) Variable profile with avg(target), note the numeric variables shoud be binned
    """
	

	
    
	
def woe_collapse(indata='', target='target', threshold=0.01):
    """
    Bin the variable using WOE method 
    # target: Y variable 
    # threshold: The threshold to combine two groups 
    """
    """
    1. Category variable 
    """ 
    tab = indata.groupby(['education', 'flag']).education.count().unstack()
    tab.columns = ['good', 'bad']
	grp_sum = pd.DataFrame(tab.sum()).transpose()
	
    tab_pct = pd.DataFrame({'group': [x for x in tab.index]
                           ,'good' : [x /grp_sum.iloc[0, 0] for x in tab['good']]
                           ,'bad'  : [x /grp_sum.iloc[0, 1] for x in tab['bad']]  				   
    })
    tab_pct = tab_pct[['group', 'good', 'bad']]
	tab_pct['IV'] = [(x - y)*log10(x/y) for x, y in zip(tab_pct['good'], tab_pct['bad'])] 		
	
	
    """
    2. Numeric variable 
    """ 
   	

























    
	
	
	

## 2. Data Processing & Feature construction)
2.1 Delete the variables 
    - (1) The variables with 90% missing rate 
    - (2) The variable is to concentration (Freq for category variable，Percentile for numeric) 
2.2 Missing imputation 
    - (1) Category variables: do nothing 
	- (2) Numeric variables: Median/Mean/Based on the variable profile?
2.3 Capping-Floor
    - (1) Numeric variables: 5%-95% percentile
2.4 Feature Construction
2.4.1 Other derived variables based on the data/business understanding 
2.4.2 Traditional methods：
    - (1) Numeric variables: (power transform) SQRT/LN/SQUARE/(1/X)  
	- (2) Norminal variables：Python cannot cope with category variables，so the category var should be converted into dummy variables 
	- (3) Ordinal variables：replace with the sequence numbers? or 
	- (4) Regroup the category variables: by Freq; by T Test 
	- (5) Spline/Partial denpendency 
2.4.3 For ScoreCard:
	- (1) WOE 
2.4.4 Generic feature construction methods：
	- (1) Clustering
	- (2) Baisc linear transformation: PCA/SVD/LDA
	- (3) Sophisticated linear transformation: Fourier/Hadamard, etc.	

## 3. Feature Selection:
## reference：http://dataunion.org/14072.html?utm_source=tuicool&utm_medium=referral
3.1 Filters: caret module/package 
    - (1) Pearson Correlation/Distance Correlation/Gain info/IV/VIF, etc. 
3.2 Wrappers: 
    - (1) Forward/Backward/Stepwise
	- (2) 用随机数构造K个变量并加入候选集，用forward/backward/stepwise做选择，一旦随机变量进入则停止
    - (3) AIC & BIC 
	- (4) single LR/SVM/Tree/Random Forest/GBDT, etc.
	
3.3 Enbedded: The learning algorithm has the feature selection process

## 4. Model Building and Parameter tuning 
4.1 LR model 
4.2 ML models 
4.3 Output the model result and key KPIs 		
		
