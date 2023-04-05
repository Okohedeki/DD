import numpy as np 
import pandas as pd
import win32com.client as win32
import xlrd
import os



active_drug_package_path_x = r'C:\Users\okohe\OneDrive\Desktop\DD\src\Backend\RawData\ActiveDrugs\package.xlsx'
active_drug_product_path_x = r'C:\Users\okohe\OneDrive\Desktop\DD\src\Backend\RawData\ActiveDrugs\product.xlsx'
compound_drug_path_x = r'C:\Users\okohe\OneDrive\Desktop\DD\src\Backend\RawData\CompoundDrugs\compounders_ndc_directory.xlsx'
excluded_drug_package_path_x = r'C:\Users\okohe\OneDrive\Desktop\DD\src\Backend\RawData\ExcludedDrugs\Packages_excluded.xlsx'
excluded_drug_product_path_x = r'C:\Users\okohe\OneDrive\Desktop\DD\src\Backend\RawData\ExcludedDrugs\Products_excluded.xlsx'
unfinished_drug_package_x = r'C:\Users\okohe\OneDrive\Desktop\DD\src\Backend\RawData\UnfinishedDrugs\unfinished_package.xlsx'
unfinished_drug_product_x = r'C:\Users\okohe\OneDrive\Desktop\DD\src\Backend\RawData\UnfinishedDrugs\unfinished_product.xlsx'


active_drug_product_df = pd.read_excel(active_drug_product_path_x)
active_drug_packaging_df = pd.read_excel(active_drug_package_path_x)

compound_drug_df = pd.read_excel(compound_drug_path_x)

excluded_drug_package_df = pd.read_excel(excluded_drug_package_path_x)
excluded_drug_product_df = pd.read_excel(excluded_drug_product_path_x)

unfinished_drug_package_df = pd.read_excel(unfinished_drug_package_x)
unfinished_drug_product_df = pd.read_excel(unfinished_drug_product_x)



#active_drug_packaging_df = pd.read_excel(active_drug_product_path,  engine = 'openpyxl')

def dateCleanUp(df, datecolumnOld, datecolumnNew):
    #returns a new df. Need to do this differently. Also convert to tuple 

    df['Start_year'] = df[datecolumnOld].astype(str).str[0:4]
    df['Start_month'] = df[datecolumnOld].astype(str).str[4:6]
    df['Start_day'] = df[datecolumnOld].astype(str).str[6:]

    df[datecolumnNew] = df['Start_month'] + '/' + df['Start_day'] + '/' + df['Start_year']
    df.drop(columns=[datecolumnOld, 'Start_year', 'Start_month', 'Start_day'], inplace=True)

    return df 


df_active_product = dateCleanUp(active_drug_product_df, 'STARTMARKETINGDATE', 'Start_Marketing_date')
df_active_product = dateCleanUp(df_active_product, 'LISTING_RECORD_CERTIFIED_THROUGH', 'ListingDate')

df_active_package = dateCleanUp(active_drug_packaging_df, 'STARTMARKETINGDATE', 'Start_Marketing_date')
df_active_package = dateCleanUp(active_drug_packaging_df, 'ENDMARKETINGDATE', 'End_Marketing_date')

df_excluded_package = dateCleanUp(excluded_drug_package_df, 'STARTMARKETINGDATE', 'Start_Marketing_date')
df_excluded_package = dateCleanUp(excluded_drug_package_df, 'ENDMARKETINGDATE', 'End_Marketing_date')



# active_drug_product_df['Start_Marketing_year'] = active_drug_product_df['STARTMARKETINGDATE'].astype(str).str[0:4]
# active_drug_product_df['Start_Marketing_month'] = active_drug_product_df['STARTMARKETINGDATE'].astype(str).str[4:6]
# active_drug_product_df['Start_Marketing_day'] = active_drug_product_df['STARTMARKETINGDATE'].astype(str).str[6:]
# active_drug_product_df['Start_Marketing_date'] = active_drug_product_df['Start_Marketing_month'] + '/' + active_drug_product_df['Start_Marketing_day'] + '/' + active_drug_product_df['Start_Marketing_year']
