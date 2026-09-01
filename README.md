# Seattle Public Transit API

A REST API that serves Seattle public transit schedule data from a PostgreSQL database, built to explore backend development with real-world GTFS transit data.

## Tech Stack
- Python
- FastAPI
- PostgreSQL
- psycopg

## Data
Uses GTFS static data from King County Metro (Seattle), covering ~2.1M stop-time records across stops, routes, trips, and stop-times. The dataset is not included in this repository due to size — download the GTFS feed separately and load it into PostgreSQL.

## Setup
1. Install PostgreSQL and create a database named `transit`
2. Download the King County Metro GTFS feed and load the `.txt` files into tables (stops, routes, trips, stop_times)
3. Install dependencies:

pip install fastapi uvicorn "psycopg[binary]"

4. Run the server:

uvicorn main:app --reload


## Endpoints
- `GET /stops/{stop_id}` — returns a stop's name and details
- `GET /stops/{stop_id}/arrivals` — returns scheduled arrivals for a stop, joined with route and headsign data

## Example
`GET /stops/100/arrivals` returns scheduled arrivals at 1st Ave & Spring St, with route names and headsigns.
