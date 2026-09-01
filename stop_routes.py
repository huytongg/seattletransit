import zipfile
import datetime
import pandas as pd

currTime = datetime.datetime.now().time()
currTimeSeconds = ((currTime.hour * 60 * 60) + (currTime.minute * 60) + currTime.second)

print(currTime)

with zipfile.ZipFile("google_transit.zip", "r") as zip_file:
    stop_times = pd.read_csv(
    zip_file.open("stop_times.txt"),
    usecols=[
        "trip_id",
        "arrival_time",
        "departure_time",
        "stop_id",
        "stop_sequence"
    ],
    low_memory=False
    )
    
    trips = pd.read_csv(
        zip_file.open("trips.txt")
    )

    routes = pd.read_csv(
        zip_file.open("routes.txt")
    )

    stops = pd.read_csv(
        zip_file.open("stops.txt"),
        usecols=[
            "stop_id",
            "stop_name"
        ]
    )


def get_stop_schedule(stop_id):
    #checks for all the rows inside stop_times that have a matching stop id, then saves them into the dataframe.
    stop_times_for_stop = stop_times[stop_times["stop_id"] == stop_id]
    
    #merge the two different dataframes together using a common column that they have
    #need to create a new dataframe that you will use the combined one for.
    result = stop_times_for_stop.merge(
    trips,
    on="trip_id"
    )

    #same thing but we used the old merged dataframe and put it into a new one.
    result2 = result.merge(
    routes,
    on="route_id"
    )

    result3 = result2.merge(
    stops,
    on="stop_id"
    )

    return result3

#take in user input for what stop they need using input()
userStop = input("What is your stop id?: ")
#convert string to int using int()
userStop = int(userStop)

schedule = get_stop_schedule(userStop)

#create an array to store the list of arrivals that are upcoming
upcomingArrivals = []
#for each row in schedule, look at the whole row
for index, row in schedule.iterrows():
    #split up arrival time into hours minutes and seconds
    arrivalParts = row["arrival_time"].split(":")
    #calculate everything into seconds
    arrivalSeconds = (int(arrivalParts[0]) * 60 * 60) + (int(arrivalParts[1]) * 60) + int(arrivalParts[2])
    #if the arrival time is greater then the current time, add that row into the list
    if arrivalSeconds > currTimeSeconds:
        #adds to the end of the list
        upcomingArrivals.append(row)


#Convert upcoming arrivals into a pandas dataframe.
upcomingSchedule = pd.DataFrame(upcomingArrivals)
#Check for upcoming arrival times.
if upcomingSchedule.empty:
    print("No upcoming arrivals found.")
    exit()
#sort the schedule by arrival times.
upcomingSchedule = upcomingSchedule.sort_values(by=["arrival_time"])
#calls the first 5 in the list.
upcomingSchedule = upcomingSchedule.head(5)

for index, row in upcomingSchedule.iterrows():
    arrivalParts = row["arrival_time"].split(":")
    period = ""
    #check time to see if it is AM or PM
    originalTime = int(arrivalParts[0])
    if  12 <= originalTime < 24:
        period = "PM"
    
    else:
        period ="AM"
    if int(arrivalParts[0]) >= 24: 
        #convert into int for conversion
        arrivalParts[0] = int(arrivalParts[0]) - 24
        #convert back into string to join
        arrivalParts[0] = str(arrivalParts[0])

        # converts 24 hour time to 12 hour time
    if int(arrivalParts[0]) > 12:
        arrivalParts[0] = int(arrivalParts[0]) - 12
        arrivalParts[0] = str(arrivalParts[0])
        #converts 0:xx AM times to 12:xx AM times.
    if int(arrivalParts[0]) == 0:
        arrivalParts[0] = int(arrivalParts[0]) + 12
        arrivalParts[0] = str(arrivalParts[0])
    

    formattedArrival = (":").join(arrivalParts)
    #.loc access a specific row and column
    #we use index to choose that row, and the second variable to access which specific column.
    #in this case we accessed upcomingSchedules specific "index" row and arrival time column.
    #that was the reason we used index instead of some variable i, to understand why we are using index.
    upcomingSchedule.loc[index, "arrival_time"] = formattedArrival + " " + period
            

print(upcomingSchedule[["stop_name","arrival_time","trip_headsign","route_short_name"]])




    