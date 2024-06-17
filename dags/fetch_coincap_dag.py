import requests
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.mysql.hooks.mysql import MySqlHook
from airflow.providers.mysql.operators.mysql import MySqlOperator
from airflow.utils.dates import days_ago
from datetime import datetime
import json
import os

def fetch_and_store_crypto_data():
    url = 'https://api.coincap.io/v2/assets'
    response = requests.get(url)
    data = response.json()['data']
    
    file_path = '/tmp/data.json'
    with open(file_path, 'w') as f:
        json.dump(data, f)
    
    # ตรวจสอบว่าไฟล์ถูกสร้างและเขียนข้อมูลสำเร็จ
    if os.path.exists(file_path):
        print(f"File {file_path} created successfully.")
    else:
        print(f"Failed to create file {file_path}.")
    
    return data

def save_data_into_db():
    mysql_hook = MySqlHook(mysql_conn_id='mysql_conn')
    conn = mysql_hook.get_conn()
    cursor = conn.cursor()

    file_path = '/tmp/data.json'
    with open(file_path) as f:
        data = json.load(f)
        
        insert = """
            INSERT INTO crypto_prices (
                timestamp,
                asset_id,
                rank,
                symbol,
                name,
                supply,
                max_supply,
                market_cap_usd,
                volume_usd_24_hr,
                price_usd,
                change_percent_24_hr,
                vwap_24_hr)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        
        timestamp = datetime.now()
        
        for asset in data:
            cursor.execute(insert, (
                timestamp,
                asset['id'],
                int(asset['rank']),
                asset['symbol'],
                asset['name'],
                float(asset['supply']),
                float(asset['maxSupply']) if asset['maxSupply'] else None,
                float(asset['marketCapUsd']),
                float(asset['volumeUsd24Hr']),
                float(asset['priceUsd']),
                float(asset['changePercent24Hr']),
                float(asset['vwap24Hr']) if asset['vwap24Hr'] else None
            ))
    
    conn.commit()
    conn.close()

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 6, 16),
    'retries': 1,
}

with DAG('fetch_coincap_dag', description='A simple data pipeline for Crypto Price', default_args=default_args, schedule_interval='@daily', catchup=False) as dag:

    create_table = MySqlOperator(
        task_id='create_crypto_prices_table',
        mysql_conn_id='mysql_conn',
        sql="""
            CREATE TABLE IF NOT EXISTS crypto_prices (
                id INT AUTO_INCREMENT PRIMARY KEY,
                timestamp DATETIME,
                asset_id VARCHAR(255),
                rank INT,
                symbol VARCHAR(50),
                name VARCHAR(255),
                supply DOUBLE,
                max_supply DOUBLE,
                market_cap_usd DOUBLE,
                volume_usd_24_hr DOUBLE,
                price_usd DOUBLE,
                change_percent_24_hr DOUBLE,
                vwap_24_hr DOUBLE
            );
        """,
    )
    
    fetch_crypto = PythonOperator(
        task_id='fetch_and_store_crypto_data',
        python_callable=fetch_and_store_crypto_data
    )
    
    save_crypto = PythonOperator(
        task_id='save_data_into_db',
        python_callable=save_data_into_db
    )
    
    create_table >> fetch_crypto >> save_crypto
