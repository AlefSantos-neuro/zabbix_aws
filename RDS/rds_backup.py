#!/usr/bin/python
from datetime import date
import sys
from optparse import OptionParser
import boto3


# {$REGION},"-a",{$KEY},"-s",{$SECRET},"-i",{HOST.HOST}
print(sys.argv)
region = sys.argv[1]
rds_name = sys.argv[2]

if (region == None):
    region = 'us-east-1'

if (rds_name == None):
    rds_name = 'ENDEREÇO DO BANCO'

# rds = boto3.client('rds', 
#                       aws_access_key_id='*********************', 
#                       aws_secret_access_key='*********************', 
#                       region_name='us-east-1'
#                       )
#region = 'sa-east-1'
rds = boto3.client('rds', region_name = region)


rds_name = rds_name
b = rds.describe_db_snapshots(DBInstanceIdentifier=rds_name)


snap_data = []

for i in b['DBSnapshots']:
    snap_date = i['SnapshotCreateTime'].date()
    today = date.today()
    if snap_date == today:
        b = 3
        snap_status = "1" if i['Status'] == 'available' else "0"
        date_time = i['SnapshotCreateTime'].strftime("%d/%m/%Y %H:%M:%S")
        snap_data.append({ "{#SNAPDATE}":date_time,"{#SNAPSTATUS}":snap_status  })
a = 2


data = """{ 
    "data":"""+str(snap_data).replace('\'','\"')+"""
}"""

print(data)
