from fastapi import FastAPI
import psycopg

app = FastAPI()

@app.get("/")
def read_root():
    return{"hello": "world"}

@app.get("/stops/{stop_id}")
def get_stops(stop_id: str):
    with psycopg.connect("dbname=transit") as conn:
        with conn.cursor() as  cur:
            cur.execute("SELECT stop_id, stop_name FROM stops WHERE stop_id = %s", (stop_id,))
            row = cur.fetchone()
    return  {"stop_id":  row[0], "stop_name": row[1]}