import requests 
import numpy 
import requests
import shutil

date = '3192023'

active_drug_url = 'https://www.accessdata.fda.gov/cder/ndcxls.zip'
unfinished_drug_url = 'https://www.accessdata.fda.gov/cder/ndc_unfinished.zip'
compound_drug_url = 'https://www.accessdata.fda.gov/cder/compounders_ndc_directory.zip'
excluded_drug_url = 'https://www.accessdata.fda.gov/cder/compounders_ndc_directory.zip'

def download_file(url, filename, date, ext = '.zip'):
    local_filename = filename+date+ext
    file_save_path = "..\\RawData\{}".format(local_filename)
    with requests.get(url, stream=True) as r:
        with open(local_filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
    shutil.move(local_filename, "..\\RawData\{}".format(local_filename))
    shutil.unpack_archive(file_save_path, "..\\RawData\{}\\".format(filename))


    return local_filename

download_file(active_drug_url, 'ActiveDrugs', date)
download_file(unfinished_drug_url, 'UnfinishedDrugs', date)
download_file(compound_drug_url, 'CompoundDrugs', date)
download_file(excluded_drug_url, 'ExcludedDrugs', date)