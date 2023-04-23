import requests 
import numpy as np 
import pandas as pd
import win32com.client as win32
import xlrd
import os
import shutil
import glob 

class ParseDrugPackagingProduct:
    def __init__(self, path):
        self.path = path 
        self.df = self.loadDataFrames()

    def loadDataFrames(self):
        df = pd.read_excel(self.path)
        return df 
    
    def ColumnAdjustment(self, datecolumnsOld, datecolumnsNew, iter):            

        #Need to convert to timestamp

        for i in range(iter):
            datacolumnOld = datecolumnsOld[i]
            datacolumnNew = datecolumnsNew[i]
            

            self.df['Start_year'] = self.df[datacolumnOld].astype(str).str[0:4]
            self.df['Start_month'] = self.df[datacolumnOld].astype(str).str[4:6]
            self.df['Start_day'] = self.df[datacolumnOld].astype(str).str[6:]

            self.df[datacolumnNew] = self.df['Start_month'] + '/' + self.df['Start_day'] + '/' + self.df['Start_year']
            self.df.drop(columns=[datacolumnOld, 'Start_year', 'Start_month', 'Start_day'], inplace=True)
            pd.to_datetime(self.df[datacolumnNew], errors='coerce')
        self.df.columns= self.df.columns.str.lower()

        return self.df
        
class FDADataDownloader:
    def __init__(self, date) -> None:
        self.date = date 
        self.active_drug_url = 'https://www.accessdata.fda.gov/cder/ndcxls.zip'
        self.unfinished_drug_url = 'https://www.accessdata.fda.gov/cder/ndc_unfinished.zip'
        self.compound_drug_url = 'https://www.accessdata.fda.gov/cder/compounders_ndc_directory.zip'
        self.excluded_drug_url = 'https://www.accessdata.fda.gov/cder/ndc_excluded.zip'


    def download_file(self, url, filename, ext='.zip'):
        files = []

        local_filename = filename + self.date + ext
        file_save_path = "..\\RawData\{}".format(local_filename)
        absolute_filepath = os.path.abspath(file_save_path)


        if os.path.exists(file_save_path):
            os.remove(file_save_path)

        with requests.get(url, stream=True) as r:
            with open(local_filename, 'wb') as f:
                shutil.copyfileobj(r.raw, f)
        shutil.move(local_filename, "..\\RawData\{}".format(local_filename))
        shutil.unpack_archive(file_save_path, "..\\RawData\{}\\".format(filename))


        full_path = os.path.abspath("..\\RawData\{}\\".format(filename)) + '\\*'
        for zip_filename in glob.glob(full_path):
            if zip_filename.split('.')[-1] == 'xls':
                zip_filename_check = zip_filename[:-3] + 'xlsx'
                self.convertToXLS(zip_filename, zip_filename_check)
                files.append(os.path.abspath(zip_filename_check))
        os.remove(absolute_filepath)    

        return files

    @staticmethod
    def convertToXLS(old_filepath, new_filepath):

        if os.path.exists(new_filepath):
            os.remove(new_filepath)

        fname = old_filepath
        excel = win32.gencache.EnsureDispatch('Excel.Application')
        wb = excel.Workbooks.Open(fname)

        wb.SaveAs(fname + "x", FileFormat=51)    # FileFormat = 51 is for .xlsx extension
        wb.Close()                               # FileFormat = 56 is for .xls extension
        excel.Application.Quit()         

    def download_files(self):
        

        self.active_drug_filepath = self.download_file(self.active_drug_url, 'ActiveDrugs')
        self.unfinshed_drug_filepath = self.download_file(self.unfinished_drug_url, 'UnfinishedDrugs')
        self.compound_drug_filepath = self.download_file(self.compound_drug_url, 'CompoundDrugs')
        self.excluded_drug_filepath = self.download_file(self.excluded_drug_url, 'ExcludedDrugs')



        return self.active_drug_filepath, self.unfinshed_drug_filepath, self.compound_drug_filepath,  self.excluded_drug_filepath


if __name__ == '__main__':
    active_drug_file, unfinished_drug_file, compound_drug_file, excluded_drug_file  = FDADataDownloader('04082023').download_files()
    
    active_package_file = active_drug_file[0]
    active_product_file = active_drug_file[1]

    unfinished_package_file = unfinished_drug_file[0]
    unfinished_product_file =unfinished_drug_file[1]

    compound_drug_file = compound_drug_file[0]

    excluded_package_df = excluded_drug_file[0]
    excluded_package_df = excluded_drug_file[1]

    print(active_package_file)


    parser_active_df = ParseDrugPackagingProduct(active_package_file)
    active_df = parser_active_df.ColumnAdjustment(['STARTMARKETINGDATE', 'ENDMARKETINGDATE'], ['startmarketingdate', 'endmarketingdate'], 2)
    
    print(active_df.head(2))

    #https://www.freecodecamp.org/news/install-apache-airflow-on-windows-without-docker/