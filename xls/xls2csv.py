import pandas as pd
def xls_to_csv():
    data_xls=pd.read_excel('1.xlsx',index_col=0)
    data_xls.to_csv('1.csv',encoding='utf-8')

if __name__=='__main__':
    xls_to_csv()
