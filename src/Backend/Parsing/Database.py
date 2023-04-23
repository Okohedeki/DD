import psycopg2
from sqlalchemy import create_engine
from FDADrugsProductList import ParseDrugPackagingProduct, FDADataDownloader
import pandas as pd

class DrugDatabase:
    def __init__(self):
        self.host = 'drugvirtualassistant.cfqehvcudm3s.us-east-1.rds.amazonaws.com'
        self.database = 'DrugData'
        self.user = 'okohedeki'
        self.password = 'MenalisA124$'
        self.schema = 'Parsing'
        self.port = 5432
        self.schema = "Parsing"
        self.engine = create_engine(f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}")


    def connect(self):
        try:
            conn = psycopg2.connect(dbname=self.database, user=self.user, password=self.password, host=self.host, port=self.port)
            # self.engine = create_engine(f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.dbname}")
            return conn
        except Exception as e:
            print(f"Unable to connect to database: {e}")

    def close(self, conn):
        conn.close()
        print("Closed connection to database")
        return None 

    def insert_into_product(self, product_df, type):
        product_df['drugtype'] = type 
        product_df.to_sql("product", self.engine, if_exists="replace", index=False,  schema = self.schema)

    def insert_into_packaging(self, packaging_df, type):
        packaging_df['package_type'] = type
        packaging_df.to_sql("package", self.engine, if_exists="replace", index=False, schema = self.schema)

    def insert_into_compound(self, compound_df):
        compound_df.to_sql("compound", self.engine, if_exists="replace", index=False,  schema = self.schema)
        
if __name__ == "__main__":

    active_drug_file, unfinished_drug_file, compound_drug_file, excluded_drug_file  = FDADataDownloader('04082023').download_files()
    active_package_file = active_drug_file[0]
    active_product_file = active_drug_file[1]

    unfinished_package_file = unfinished_drug_file[0]
    unfinished_product_file =unfinished_drug_file[1]

    compound_drug_file = compound_drug_file[0]

    excluded_package_df = excluded_drug_file[0]
    excluded_package_df = excluded_drug_file[1]

    parser_active_package_df = ParseDrugPackagingProduct(active_package_file)
    parser_active_product_df = ParseDrugPackagingProduct(active_product_file)

    active_package_df = parser_active_package_df.ColumnAdjustment(['STARTMARKETINGDATE', 'ENDMARKETINGDATE'], ['startmarketingdate', 'endmarketingdate'], 2)
    active_product_df = parser_active_product_df.ColumnAdjustment(['STARTMARKETINGDATE', 'ENDMARKETINGDATE'], ['startmarketingdate', 'endmarketingdate'], 2)


    db = DrugDatabase()
    conn = db.connect()

    print(active_package_df.columns)
    print(active_product_df.columns)

    db.insert_into_packaging(active_package_df, 'Active')
    db.insert_into_product(active_product_df, 'Active')

    db.close(conn)