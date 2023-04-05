import psycopg2

class MyDatabase():
    def __init__(self, db="mydb", user="postgres"):
        self.conn = psycopg2.connect(dbname=db, user=user)
        self.cur = self.conn.cursor()

    def query(self, query):
        self.cur.execute(query)

    def close(self):
        self.cur.close()
        self.conn.close()

db = MyDatabase()
db.query("SELECT * FROM table;")
db.close()

https://clinicaltrials.gov/ct2/results?cond=Prophylactic+Herpes+Simplex+Virus-2&term=&cntry=&state=&city=&dist=