import pandas as pd

def csv_to_xlsx_pd():
	csv = pd.read_csv('1.csv', encoding='utf-8', sep='\t')
	csv.to_excel('1.xlsx', sheet_name='data')


if __name__ == '__main__':
	csv_to_xlsx_pd()
