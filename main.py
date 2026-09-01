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

@app.get("/stops/{stop_id}/arrivals")
def get_arrivals(stop_id: str):
    with psycopg.connect("dbname=transit") as conn:
        with conn.cursor() as cur:
            cur.execute("""
                    SELECT s.stop_name, st.arrival_time, t.trip_headsign, r.route_short_name                        
                    FROM  stop_times st
                    JOIN stops s ON st.stop_id = s.stop_id
                    JOIN trips t on st.trip_id = t.trip_id
                    JOIN routes r on t.route_id = r.route_id
                    WHERE st.stop_id = %s
                    ORDER BY st.arrival_time
                    LIMIT 5
            """, (stop_id,))
            rows = cur.fetchall()
    return [
        {"stop_name": r[0], "arrival_time": r[1], "headsign": r[2], "route": r[3]}
        for r in rows
    ]