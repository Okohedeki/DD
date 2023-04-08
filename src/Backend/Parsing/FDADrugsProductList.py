import requests 
import numpy as np 
import pandas as pd
import win32com.client as win32
import xlrd
import os
import shutil
import glob 

class ParseDrugPackagingProduct:
    def __init__(self, path) -> None:
        self.path = path 

    def loadDataFrames(self):
        df = pd.read_excel(self.path)
        return df 
    
    @staticmethod
    def dateCleanUp(df, datecolumnOld, datecolumnNew):
        df['Start_year'] = df[datecolumnOld].astype(str).str[0:4]
        df['Start_month'] = df[datecolumnOld].astype(str).str[4:6]
        df['Start_day'] = df[datecolumnOld].astype(str).str[6:]

        df[datecolumnNew] = df['Start_month'] + '/' + df['Start_day'] + '/' + df['Start_year']
        df.drop(columns=[datecolumnOld, 'Start_year', 'Start_month', 'Start_day'], inplace=True)

        return df 

class FDADataDownloader:
    def __init__(self, date) -> None:
        self.date = date 
        self.active_drug_url = 'https://www.accessdata.fda.gov/cder/ndcxls.zip'
        self.unfinished_drug_url = 'https://www.accessdata.fda.gov/cder/ndc_unfinished.zip'
        self.compound_drug_url = 'https://www.accessdata.fda.gov/cder/compounders_ndc_directory.zip'
        self.excluded_drug_url = 'https://www.accessdata.fda.gov/cder/ndc_excluded.zip'

    def download_file(self, url, filename, ext='.zip'):
        local_filename = filename + self.date + ext
        file_save_path = "..\\RawData\{}".format(local_filename)

        if os.path.exists(file_save_path):
            os.remove(file_save_path)

        with requests.get(url, stream=True) as r:
            with open(local_filename, 'wb') as f:
                shutil.copyfileobj(r.raw, f)
        shutil.move(local_filename, "..\\RawData\{}".format(local_filename))
        shutil.unpack_archive(file_save_path, "..\\RawData\{}\\".format(filename))
        os.remove(file_save_path)

        full_path = os.path.abspath("..\\RawData\{}\\".format(filename)) + '\\*'
        for zip_filename in glob.glob(full_path):
            if zip_filename.split('.')[-1] == 'xls':
                zip_filename_check = zip_filename[:-3] + 'xlsx'
                self.convertToXLS(zip_filename, zip_filename_check)
            

        return file_save_path

    def convertToXLS(self, old_filepath, new_filepath):

        if os.path.exists(new_filepath):
            os.remove(new_filepath)

        fname = old_filepath
        excel = win32.gencache.EnsureDispatch('Excel.Application')
        wb = excel.Workbooks.Open(fname)

        wb.SaveAs(fname + "x", FileFormat=51)    # FileFormat = 51 is for .xlsx extension
        wb.Close()                               # FileFormat = 56 is for .xls extension
        excel.Application.Quit()

    def download_files(self):
        active_drug_filepath = self.download_file(self.active_drug_url, 'ActiveDrugs')
        unfinshed_drug_filepath = self.download_file(self.unfinished_drug_url, 'UnfinishedDrugs')
        compound_drug_filepath = self.download_file(self.compound_drug_url, 'CompoundDrugs')
        excluded_drug_filepath = self.download_file(self.excluded_drug_url, 'ExcludedDrugs')

        return active_drug_filepath, unfinshed_drug_filepath, compound_drug_filepath, excluded_drug_filepath


if __name__ == '__main__':
    downloader = FDADataDownloader('3192023')
    downloader.download_all_files()
    print(downloader.active_drug_filepath)
    print(downloader.unfinshed_drug_filepath)
    print(downloader.compound_drug_filepath)
    print(downloader.excluded_drug_filepath)
