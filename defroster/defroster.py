# USAGE:
    # python Unfreezebkts.py EPOCH_SINCE EPOCH_TO {INDEX} {INFOSEC_REQUEST_ID}

import os
import time
import sys
import subprocess
from datetime import datetime

p = '%m-%d-%Y'
from_date = sys.argv[1]
to_date = sys.argv[2]
path = '/splunk_data/'+sys.argv[3]+'/'
path_destination = '/splunk_data/'+sys.argv[4]+'/'
buckets_size = 0
content = os.listdir(path)
buckets = []
FNULL = open(os.devnull, 'w')
i=1

for bucket in content:
    if("db_" in bucket): # We don't want those .rbsentinel files
        data = bucket.split("_")
        if(data[1] <= to_date and data[2] >= from_date):
            buckets.append(bucket)
            buckets_size = buckets_size + os.path.getsize(path+"/"+bucket)
        elif(data[1] > to_date and data[2] > from_date and data[2] <= to_date):
            buckets.append(bucket)
            buckets_size = buckets_size + os.path.getsize(path+"/"+bucket)

print("Buckets to be restored:\t" + str(len(buckets)) + "\nCompressed Size:\t" + str(int(buckets_size/(1024.0)))+"MB")
print("First Bucket: \t" + buckets[0])
print("Last Bucket: \t" + buckets[len(buckets)-1])
answer = raw_input("\n\tDo you want to continue? [y/n]: ").lower().strip()
if(answer == "y"):
    print("Starting to copy and rebuilding the buckets...")
    for bucket in buckets:
        data = bucket.split("_")
        f_event = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(data[2])))
        l_event = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(data[1])))
        print("NUMBER="+str(i)+", BUCKET="+bucket+", FIRST_EVENT="+f_event+", LAST_EVENT="+l_event)
        process = subprocess.Popen(['cp', '-Rf',path+bucket,path_destination], stdout=FNULL, stderr=subprocess.STDOUT, universal_newlines=True)
        process.wait()
        process = subprocess.Popen(['/opt/splunk/bin/splunk', 'rebuild', path_destination+bucket], stdout=FNULL, stderr=subprocess.STDOUT, universal_newlines=True)
        process.wait()
        time.sleep(2)
	i=i+1
else:
    exit()

print(str(len(buckets))+" buckets has been restored.")
exit()