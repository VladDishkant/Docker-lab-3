import math
import string
import random as rnd
import numpy as np
import pandas as pd
from typing import List
from hurry.filesize import size, alternative
from datetime import datetime, timezone, timedelta
from pymongo import MongoClient
from pymongo import errors


NAMES_CSV = 'uk_names.csv'
SURNAMES_CSV = 'uk_surnames.csv'
REVIEWS_CSV = 'uk_taxi_reviews.csv'


def open_connection(
        host: str = 'localhost',
        port: int = 37017,
        user: str = 'admin',
        pwd: str = 'secret'
) -> MongoClient:
    try:
        if len(user):
            conn_str = f"mongodb://{user}:{pwd}@{host}:{port}"
        else:
            conn_str = f"mongodb://{host}:{port}"
        res = MongoClient(conn_str)
        res.server_info()
        return res
    except errors.ServerSelectionTimeoutError as e:
        print(e)
        exit(1)


def random_full_name(df_names: np.ndarray, df_surnames: np.ndarray) -> str:
    i = rnd.randint(0, len(df_names) - 1)
    j = rnd.randint(0, len(df_surnames) - 1)

    return f"{df_names[i][0]} {df_surnames[j][0]}"


def random_color() -> str:
    colors = np.array(['white', 'black', 'gray', 'silver',
                       'red', 'blue', 'brown', 'green',
                       'beige', 'orange', 'gold', 'yellow', 'purple'])
    i = rnd.randint(0, len(colors) - 1)

    return colors[i]


def random_car() -> str:
    cars = np.array(['Acura', 'Alfa Romeo', 'Audi', 'BMW', 'Bentley',
                     'Buick', 'Cadillac', 'Chevrolet', 'Chrysler',
                     'Dodge', 'Fiat', 'Ford', 'GMC', 'Genesis', 'Honda',
                     'Hyundai', 'Infiniti', 'Jaguar', 'Jeep', 'Kia', 'Land Rover',
                     'Lexus', 'Lincoln', 'Lotus', 'Lucid', 'Maserati', 'Mazda',
                     'Mercedes-Benz', 'Mercury', 'Mini', 'Mitsubishi', 'Nissan',
                     'Polestar', 'Pontiac', 'Porsche', 'Ram', 'Rivian', 'Rolls-Royce',
                     'Saab', 'Saturn', 'Scion', 'Smart', 'Subaru', 'Suzuki', 'Tesla',
                     'Toyota', 'Volkswagen', 'Volvo'])
    i = rnd.randint(0, len(cars) - 1)

    return cars[i]


def random_registration_plate() -> str:
    registration_plate = "L"
    registration_plate += rnd.choice(string.ascii_uppercase)
    registration_plate += str(rnd.randint(0, 5))
    registration_plate += str(rnd.randint(0, 9))

    for i in range(0, 3):
        registration_plate += rnd.choice(string.ascii_uppercase)

    return registration_plate


def random_mobile_phone_number() -> str:
    mobile_phone_number = "+44"
    mobile_phone_number += str(rnd.randint(70, 79))

    for i in range(0, 4):
        mobile_phone_number += str(rnd.randint(10, 99))

    return mobile_phone_number


def random_date(start_year: int, end_year: int) -> str:
    year = rnd.randint(start_year, end_year)
    months = []

    for i in range(1, 13):
        if i < 10:
            months = np.append(months, "0" + str(i))
        else:
            months = np.append(months, str(i))

    month = months[rnd.randint(0, 11)]

    if month in np.array(['04', '06', '09', '11']):
        day = rnd.randint(1, 30)
    elif month in np.array(['02']):
        if year % 4 == 0:
            day = rnd.randint(1, 29)
        else:
            day = rnd.randint(1, 28)
    else:
        day = rnd.randint(1, 31)

    if day < 10:
        day = "0" + str(day)

    return f"{year}-{month}-{day}"


def random_email(full_name: str, date_of_birth: str = None) -> str:
    domains = np.array(["gmail.com", "yahoo.com", "hotmail.com", "aol.com"])
    domain = domains[rnd.randint(0, len(domains) - 1)]
    email_format = rnd.randint(1, 4)

    if email_format == 1:
        return full_name.replace(" ", "_").lower() + "@" + domain
    elif email_format == 2:
        return full_name.split(" ")[0].lower() + "@" + domain
    elif email_format == 3:
        res = full_name.replace(" ", "_").lower()
        if date_of_birth is not None:
            res += date_of_birth.split("-")[0]
        res += "@" + domain
        return res
    elif email_format == 4:
        res = full_name.split(" ")[0].lower()
        if date_of_birth is not None:
            res += "_" + date_of_birth.split("-")[0]
        res += "@" + domain
        return res


def random_rating() -> int:
    return rnd.randint(1, 5)


def random_client_feedback() -> List[str]:
    categories = ['On Time', 'Driver', 'Journey', 'Discount',
                  'Music', 'Talk', 'Nationality', 'Speed',
                  'Air Conditioner', 'Purity']
    return list([categories[i] for i in range(rnd.randint(1, 4), rnd.randint(5, len(categories) - 1))])


def random_client_comment(lib: np.ndarray, rating: int = None) -> str:
    if rating is not None:
        res = [lib[i][1] for i in np.where(lib[:, 0] == rating)[0]]
    else:
        res = [lib[i][1] for i in range(0, len(lib))]
    return res[rnd.randint(0, len(res) - 1)]


def random_driver_feedback() -> List[str]:
    categories = ['Tips', 'Greedy', 'Kind', 'Drunk',
                  'Religion', 'Politics', 'Appearance',
                  'Demanding', 'Strange', 'Scandalous']
    return list([categories[i] for i in range(rnd.randint(1, 4), rnd.randint(5, len(categories) - 1))])


def calculate_cost(distance: float, ride_time: float) -> float:
    return round(2.3 * distance + 0.5 * ride_time, 2)


def calculate_ride_time(distance: float, start_time: str) -> float:
    tm_h = datetime.fromisoformat(start_time).time().hour
    tm_m = datetime.fromisoformat(start_time).time().minute
    tm = tm_h * 60 * 60 + tm_m * 60
    if 27000 <= tm <= 32400 or 61200 <= tm <= 68400:
        speed = 20  # rush_hour_speed (07:30 - 09:00 and 17:00 - 19:00)
    elif tm >= 82800 or tm <= 21600:
        speed = 48  # night_time_speed (23:00 - 06:00)
    else:
        speed = 40  # day_time_speed
    return round(distance / speed, 2) * 60


def calculate_distance(
        lat_1: float,
        lon_1: float,
        alt_1: float,
        lat_2: float,
        lon_2: float,
        alt_2: float
) -> float:
    r = 6376.5 * 1000
    lat_1 = lat_1 * (math.pi / 180)
    lon_1 = lon_1 * (math.pi / 180)
    lat_2 = lat_2 * (math.pi / 180)
    lon_2 = lon_2 * (math.pi / 180)
    x_1 = (r + alt_1) * math.cos(lat_1) * math.sin(lon_1)
    y_1 = (r + alt_1) * math.sin(lat_1)
    z_1 = (r + alt_1) * math.cos(lat_1) * math.cos(lon_1)
    x_2 = (r + alt_2) * math.cos(lat_2) * math.sin(lon_2)
    y_2 = (r + alt_2) * math.sin(lat_2)
    z_2 = (r + alt_2) * math.cos(lat_2) * math.cos(lon_2)

    return round(math.sqrt((x_2 - x_1) ** 2 + (y_2 - y_1) ** 2 + (z_2 - z_1) ** 2) / 1000, 3)


def open_route(driver_id: list, client_id: list = None) -> str:
    current_time = datetime.now(timezone.utc).isoformat()
    ct = datetime.fromisoformat(current_time)
    connection = open_connection()
    driver = list(connection.london.drivers.find({'_id': driver_id}))[0]
    start_location = list(connection.london.postcodes.find({'_id': driver['Location']}))[0]
    if client_id:
        client = list(connection.london.clients.find({'_id': client_id}))[0]
        end_location = list(connection.london.postcodes.find({'_id': client['Location']}))[0]
    else:
        end_location = list(connection.london.postcodes.aggregate([{
            '$match': {'District': start_location['District']},
        }, {
            '$sample': {'size': 1}
        }]))[0]
    connection.close()

    reviews = pd.read_csv(REVIEWS_CSV).to_numpy()

    lat_start = start_location['Latitude']
    lon_start = start_location['Longitude']
    alt_start = start_location['Altitude']

    lat_end = end_location['Latitude']
    lon_end = end_location['Longitude']
    alt_end = end_location['Altitude']

    driver_id = driver['_id']

    start_time = ct.isoformat()
    dist = calculate_distance(
        lat_1=lat_start,
        lon_1=lon_start,
        alt_1=alt_start,
        lat_2=lat_end,
        lon_2=lon_end,
        alt_2=alt_end
    )
    rt = calculate_ride_time(dist, start_time)
    end_time = (datetime.fromisoformat(start_time) + timedelta(seconds=rt * 60)).isoformat()

    cost = 0
    driver_rating = None
    client_feedback = None
    client_comment = None
    client_rating = None
    driver_feedback = None

    if client_id:
        cost = calculate_cost(dist, rt)
        driver_rating = random_rating()
        client_feedback = random_client_feedback()
        client_comment = random_client_comment(reviews, driver_rating)
        client_rating = random_rating()
        driver_feedback = random_driver_feedback()

    connection = open_connection()
    result = connection.london.routes.insert_one({
        'LatitudeStart': lat_start,
        'LongitudeStart': lon_start,
        'AltitudeStart': alt_start,
        'LatitudeEnd': lat_end,
        'LongitudeEnd': lon_end,
        'AltitudeEnd': alt_end,
        'StartTime': start_time,
        'EndTime': end_time,
        'Driver': driver_id,
        'Client': client_id,
        'Cost': cost,
        'Currency': 'GBP',
        'DriverRating': driver_rating,
        'ClientFeedback': client_feedback,
        'ClientComment': client_comment,
        'ClientRating': client_rating,
        'DriverFeedback': driver_feedback
    })

    connection.london.drivers.update_one({
        '_id': driver_id
    }, {
        '$set': {
            'Route': result.inserted_id,
            'EndTime': end_time,
            'Location': end_location['_id']
        }
    }, upsert=False)

    if client_id:
        connection.london.clients.update_one({
            '_id': client_id
        }, {
            '$set': {
                'Location': None
            }
        }, upsert=False)

    connection.close()

    return result.inserted_id


def close_route(route_id: int):
    connection = open_connection()
    route = list(connection.london.routes.find({'_id': route_id}))[0]

    connection.london.drivers.update_one({
        '_id': route['Driver']
    }, {
        '$set': {
            'Route': None,
            'EndTime': None
        }
    }, upsert=False)

    if route['Client']:
        location = list(connection.london.postcodes.aggregate([{
            '$sample': {'size': 1}
        }]))[0]
        connection.london.clients.update_one({
            '_id': route['Client']
        }, {
            '$set': {
                'Location': location['_id']
            }
        }, upsert=False)

    connection.close()


def progress(entity: string, count: int, completed: int, current: int) -> int:
    labels = 25
    percent = round((current / count) * 100, 2)
    chunk = 100 / labels
    chunks = 0

    if (percent - ((completed / count) * 100)) < chunk:
        return completed
    else:
        print(f"{datetime.now(timezone.utc).isoformat()}\t[", end='')
        for i in range(0, labels):
            if chunks < percent:
                print("#", end='')
            else:
                print(".", end='')
            chunks += chunk

        print(f"]\t{entity}\t{current}/{count}\t({percent}%)")
        return current


def generate_drivers(count: int) -> None:
    names = pd.read_csv(NAMES_CSV).to_numpy()[0:500]
    surnames = pd.read_csv(SURNAMES_CSV).to_numpy()[0:500]
    connection = open_connection()
    locations = list(connection.london.postcodes.aggregate([{'$sample': {'size': count}}]))
    connection.close()

    drivers = []
    processed = 0
    for i in range(0, count):
        full_name = random_full_name(names, surnames)
        car = random_car()
        registration_plate = random_registration_plate()
        color = random_color()
        mobile_phone_number = random_mobile_phone_number()

        if i % 2 == 0:
            date_of_birth = ''
        else:
            date_of_birth = random_date(1950, 1991)

        if i % 4 == 0:
            email = ''
        else:
            email = random_email(full_name, date_of_birth)

        drivers.append([full_name, car, registration_plate,
                        color, mobile_phone_number, date_of_birth, email, locations[i]['_id'], ''])
        processed = progress('london.drivers', count, processed, i)

    df = pd.DataFrame(
        drivers,
        columns=['FullName', 'Car', 'RegistrationPlate',
                 'Color', 'MobilePhoneNumber',
                 'DateOfBirth', 'Email', 'Location', 'EndTime']
    )
    connection = open_connection()
    connection.london.drivers.drop()
    connection.london.drivers.insert_many(df.apply(lambda x: x.to_dict(), axis=1).to_list())
    connection.close()


def generate_clients(count: int) -> None:
    names = pd.read_csv(NAMES_CSV).to_numpy()[500:1000]
    surnames = pd.read_csv(SURNAMES_CSV).to_numpy()[500:1000]
    connection = open_connection()
    locations = list(connection.london.postcodes.aggregate([{'$sample': {'size': count}}]))
    connection.close()

    clients = []
    processed = 0

    for i in range(0, count):
        full_name = random_full_name(names, surnames)
        mobile_phone_number = random_mobile_phone_number()

        if i % 7 == 0:
            date_of_birth = ''
        else:
            date_of_birth = random_date(1950, 1991)

        if i % 9 == 0:
            email = ''
        else:
            email = random_email(full_name, date_of_birth)

        if i % 2 == 0:
            location = None
        else:
            location = locations[i]['_id']

        clients.append([full_name, mobile_phone_number, date_of_birth, email, location])
        processed = progress('london.clients', count, processed, i)

    df = pd.DataFrame(clients, columns=['FullName', 'MobilePhoneNumber', 'DateOfBirth', 'Email', 'Location'])
    connection = open_connection()
    connection.london.clients.drop()
    connection.london.clients.insert_many(df.apply(lambda x: x.to_dict(), axis=1).to_list())
    connection.close()


def generate_routes(min_size: int, intensity: int) -> None:
    min_size = int(min_size * math.pow(1024, 3))
    current_time = datetime.now(timezone.utc).isoformat()
    ct = datetime.fromisoformat(current_time)

    curr_size = 0
    while curr_size <= min_size:
        ct += timedelta(seconds=intensity)
        connection = open_connection()
        drivers = list(connection.london.drivers.find({}, {
            'Location': 1,
            'EndTime': 1,
            'Route': 1
        }))
        clients = list(connection.london.clients.find({
            'Location': {'$ne': None}
        }, {
            'Location': 1
        }))
        connection.close()
        for n in range(0, len(drivers)):
            end_time = drivers[n]['EndTime']
            if not end_time:
                if len(clients):
                    client_id = clients.pop()['_id']
                else:
                    client_id = None
                open_route(driver_id=drivers[n]['_id'], client_id=client_id)
            elif ct > datetime.fromisoformat(end_time):
                close_route(drivers[n]['Route'])

        connection = open_connection()
        curr_size = connection.london.command("collstats", "routes")['totalsize']
        print(size(curr_size, system=alternative))
        connection.close()


if __name__ == '__main__':
    print("\nGenerate drivers:\n")
    generate_drivers(count=3000)
    print("\nGenerate clients:\n")
    generate_clients(count=5000)
    print("\nGenerate routes:\n")
    generate_routes(min_size=10, intensity=600)
