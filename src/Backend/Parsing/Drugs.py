import requests 
import numpy 
import os
import requests
import shutil
import win32com.client as win32
import glob 

date = '3192023'

active_drug_url = 'https://www.accessdata.fda.gov/cder/ndcxls.zip'
unfinished_drug_url = 'https://www.accessdata.fda.gov/cder/ndc_unfinished.zip'
compound_drug_url = 'https://www.accessdata.fda.gov/cder/compounders_ndc_directory.zip'
excluded_drug_url = 'https://www.accessdata.fda.gov/cder/compounders_ndc_directory.zip'

def download_file(url, filename, date, ext = '.zip'):
    local_filename = filename+date+ext
    file_save_path = "..\\RawData\{}".format(local_filename)

    if os.path.exists(file_save_path):
        os.remove(file_save_path)

    with requests.get(url, stream=True) as r:
        with open(local_filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
    shutil.move(local_filename, "..\\RawData\{}".format(local_filename))
    shutil.unpack_archive(file_save_path, "..\\RawData\{}\\".format(filename))
    #print("..\\RawData\{}\\".format(filename))
    full_path = os.path.abspath("..\\RawData\{}\\".format(filename)) + '\\*'
    for zip_filename in glob.glob(full_path):
        if zip_filename.split('.')[-1] == 'xls':
            zip_filename_check = zip_filename[:-3] + 'xlsx'
            convertToXLS(zip_filename,zip_filename_check)


    return file_save_path

def convertToXLS(old_filepath, new_filepath):

    if os.path.exists(new_filepath):
        os.remove(new_filepath)

    fname = old_filepath
    excel = win32.gencache.EnsureDispatch('Excel.Application')
    wb = excel.Workbooks.Open(fname)

    wb.SaveAs(fname+"x", FileFormat = 51)    #FileFormat = 51 is for .xlsx extension
    wb.Close()                               #FileFormat = 56 is for .xls extension
    excel.Application.Quit()


active_drug_filepath = download_file(active_drug_url, 'ActiveDrugs', date)
unfinshed_drug_filepath = download_file(unfinished_drug_url, 'UnfinishedDrugs', date)
compound_drug_filepath = download_file(compound_drug_url, 'CompoundDrugs', date)
excluded_drug_filepath = download_file(excluded_drug_url, 'ExcludedDrugs', date)

# print(active_drug_filepath)

# print(unfinshed_drug_filepath)

# print(compound_drug_filepath)

# print(excluded_drug_filepath)