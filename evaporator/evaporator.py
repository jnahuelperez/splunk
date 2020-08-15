# USAGE:
    # python evaporator.py EPOCH_DATE {FROZEN_FOLDER}

import os
import time
import sys
import subprocess
from datetime import datetime

date = sys.argv[1]
path = sys.argv[2]
buckets_size = 0
content = os.listdir(path)
buckets = []
FNULL = open(os.devnull, 'w')
i=1

for bucket in content:
    if("db_" in bucket):
        data = bucket.split("_")
        # Bucket: db_1567418105_1567418105_28067
        # data[1]: 1567418105
        # data[2]: 1567418105
        if(data[2] < date or data[1] < date):
            buckets.append(bucket)
            buckets_size = buckets_size + os.path.getsize(path+"/"+bucket)

print("Buckets to be delete:\t" + str(len(buckets)) + "\t" +str(int(buckets_size/(1024.0)))+"MB")
answer = raw_input("Do you want to continue? [y/n]: ").lower().strip()
if(answer == "y"):
    print("Vaping....")
    print("++++++++++++++++++++++++++++++++++++++++++")
    print("FOLDER:\t"+path)
    for bucket in buckets:
        data = bucket.split("_")
        f_event = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(data[2])))
        l_event = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(data[1])))
        print("NUMBER="+str(i)+", BUCKET="+bucket+", FIRST_EVENT="+f_event+", LAST_EVENT="+l_event)
        process = subprocess.Popen(['rm', '-Rf',path+bucket], stdout=FNULL, stderr=subprocess.STDOUT, universal_newlines=True)
        process.wait()
        i+=1
else:
    exit()

print(str(len(buckets))+" buckets has been deleted.")
print("++++++++++++++++++++++++++++++++++++++++++")
exit()
