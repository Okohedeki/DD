import numpy as np 
import pandas as pd
import win32com.client as win32
import xlrd
import os



active_drug_package_path = r'C:\Users\okohe\OneDrive\Desktop\DD\src\Backend\RawData\ActiveDrugs\package.xls'
active_drug_package_path_x = r'C:\Users\okohe\OneDrive\Desktop\DD\src\Backend\RawData\ActiveDrugs\package.xlsx'


active_drug_product_path = r'C:\Users\okohe\OneDrive\Desktop\DD\src\Backend\RawData\ActiveDrugs\product.xls'

if os.path.exists(active_drug_package_path_x):
    os.remove(active_drug_package_path_x)

fname = active_drug_package_path
excel = win32.gencache.EnsureDispatch('Excel.Application')
wb = excel.Workbooks.Open(fname)

wb.SaveAs(fname+"x", FileFormat = 51)    #FileFormat = 51 is for .xlsx extension
wb.Close()                               #FileFormat = 56 is for .xls extension
excel.Application.Quit()

active_drug_packaging_df = pd.read_excel(active_drug_package_path_x)
#active_drug_packaging_df = pd.read_excel(active_drug_product_path,  engine = 'openpyxl')

print(active_drug_packaging_df.head(5))