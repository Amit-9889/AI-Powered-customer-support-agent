import psycopg2
from psycopg2.extras import RealDictCursor

class PostgresDB:

    def __init__(self,dsn:dict):
        self.dsn = dsn

    def fetch_one(self,sql_query:str,params=None):
        with psycopg2.connect(**self.dsn) as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as curr:
                curr.execute(sql_query,params)
                # print("Fetching many results",curr.fetchmany(3))
                return curr.fetchmany(3)



