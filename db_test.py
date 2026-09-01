import psycopg

with psycopg.connect("dbname=transit") as conn:
    with conn.cursor() as cur:
        cur.execute("SELECT stop_id, stop_name FROM stops WHERE stop_id = '100'")
        rows = cur.fetchall()
        print(rows)

