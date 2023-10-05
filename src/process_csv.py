import os
import pandas as pd
import redis
from typing import Tuple


def main():
    filename_raw, raw_csv = read_csv_from_redis()  # Provide the filename of the CSV to aggregate

    aggregate_csv(filename_raw, raw_csv)

def aggregate_csv(filename_raw: str, df: pd.DataFrame) -> None:
    # Aggregate sales data
    aggregated_data = df.groupby('item_id')['quantity_sold'].sum().reset_index()

    # Create the 'processed' directory if it doesn't exist
    processed_directory = os.path.join(os.path.dirname(__file__), '..', 'data/processed')
    if not os.path.exists(processed_directory):
        os.makedirs(processed_directory)

    # Write aggregated sales data to a CSV file
    output_filename = os.path.join(processed_directory, f"{filename_raw.split('.')[0]}_aggregated_sales.csv")
    aggregated_data.to_csv(output_filename, index=False)

    print(f"Aggregated sales data has been written to '{output_filename}'.")

def read_csv_from_redis() -> Tuple[str, pd.DataFrame]:
    redis_host = os.getenv("REDIS_HOST")
    redis_list = os.getenv("REDIS_LIST")
    
    if not redis_host or not redis_list:
        print(f"Either REDIS_HOST and/or REDIS_LIST environment variable is not set. REDIS_HOST: {redis_host}, REDIS_LIST: {redis_list}")
        exit()
    
    redis_client = redis.Redis(host=redis_host, port=6379, db=0)
    last_csv_name = redis_client.rpop(redis_list)
    
    if not last_csv_name:
        print("No csvs to process on the redis queue, quit program")
        exit()
        
    last_csv_name = last_csv_name.decode("utf-8")
    
    # Read the csv
    full_filename = os.path.join(os.path.dirname(__file__), "..", "data/raw", last_csv_name)
    df = pd.read_csv(full_filename)
    
    return last_csv_name, df


if __name__ == '__main__':
    main()
