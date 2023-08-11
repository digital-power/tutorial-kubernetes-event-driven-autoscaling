import os
import csv
import random
from datetime import datetime, timedelta
import time
import redis

def generate_csv_files(start_date, end_date, directory):
    print("Starting generation of csv files")
    
    # Initialize redis connection
    redis_host = os.getenv("REDIS_HOST")
    redis_list = os.getenv("REDIS_LIST")
    redis_client = redis.Redis(host=redis_host, port=6379, db=0)
    
    if not redis_host or not redis_list:
        print(f"Either REDIS_HOST and/or REDIS_LIST environment variable is not set. REDIS_HOST: {redis_host}, REDIS_LIST: {redis_list}")
        exit()
    
    # Create the directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Iterate over each date within the range
    current_date = start_date
    while current_date < end_date:
        # Generate CSV file name with datetime format 'YYYYMMDD.csv'
        filename = current_date.strftime('%Y%m%d') + '.csv'

        # Generate data for the CSV
        data = []
        for _ in range(200):  # Generating 200 timestamps per day
            timestamp = current_date + timedelta(seconds=random.randint(0, 86400))
            item_id = random.randint(1, 5)  # Random item ID between 1 and 5
            quantity_sold = random.randint(1, 10)  # Random quantity between 1 and 10
            data.append([timestamp, item_id, quantity_sold])

        # Write data to the CSV file
        filepath = os.path.join(directory, filename)
        with open(filepath, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['timestamp', 'item_id', 'quantity_sold'])  # CSV header
            writer.writerows(data)

        # Put filename on the redis list
        redis_client.lpush(redis_list, filename)

        # Move to the next day
        current_date += timedelta(days=1)
        
        print("Finished generation of csv files")

if __name__ == '__main__':
    start_date = datetime(2020, 1, 1)
    end_date = datetime(2020, 6, 1)
    directory = os.path.join(os.path.dirname(__file__), '..', 'data/raw')

    generate_csv_files(start_date, end_date, directory)
