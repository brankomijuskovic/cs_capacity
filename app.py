import time
import json
import datetime
import os
import sys
from cs import CloudStack
from influxdb import InfluxDBClient

sleep_time = os.environ['SLEEP']
influxdb_host = os.environ['INFLUXDB_HOST']

try:
    config = json.loads(os.environ['CONFIG'])
except Exception as err:
    print("No access parameters provided, exiting. {}".format(err))
    sys.exit(1)

while True:
    try:
        client = InfluxDBClient(influxdb_host, 8086, 'root', 'root', 'cs_capacity')
        client.create_database('cs_capacity')
        break
    except Exception as err:
        print("{} - Can't connect to InfluxDB, sleeping.".format(datetime.datetime.now()))
        print(err)
        time.sleep(5)

while True:
    for zone, params in config.items():
        try:
            cs = CloudStack(endpoint=params['api_url'], key=params['api_key'], secret=params['secret_key'])
            mem = cs.listCapacity(type=0)['capacity'][0]['percentused']
            cpu = cs.listCapacity(type=1)['capacity'][0]['percentused']
            client.write_points([{"measurement": zone+" - CPU", "fields": {"value": float(cpu)}}])
            client.write_points([{"measurement": zone + " - MEMORY", "fields": {"value": float(mem)}}])
        except Exception as err:
            print("{} - Something went wrong. {}".format(datetime.datetime.now(), err))
            time.sleep(5)

    time.sleep(int(sleep_time))
