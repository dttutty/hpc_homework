import os
import re
import json

#get arguments from command line
import sys
args = sys.argv
folder_path = '/home/Students/sqp17/hpc_homework/hw1/NPB/result'
exp_path = args[1]
path = os.path.join(folder_path, exp_path,'0')
log_files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]


results = []

pattern_threads = re.compile(r"Threads\s*=\s*(\d+)")
pattern_time = re.compile(r"Time in seconds\s*=\s*([\d.]+)")
pattern_mops = re.compile(r"Mop/s total\s*=\s*([\d.]+)")
pattern_verification = re.compile(r"Verification\s*=\s*(SUCCESSFUL|UNSUCCESSFUL)")


for log_file in log_files:
    
    time_in_seconds_array = []
    mops_total_array = []
    for i in range(0, 2):
        file_path = os.path.join(folder_path, exp_path, str(i) , log_file)
        with open(file_path, 'r') as f:
            content = f.read()
            flag = log_file.replace('.log', '').split('-')[0]
            threads = int(pattern_threads.search(content).group(1))
            ver =  pattern_verification.search(content).group(1)
            
            time_in_seconds_array.append(float(pattern_time.search(content).group(1)))
            mops_total_array.append(float(pattern_mops.search(content).group(1)))
                

    time_in_seconds_mean = sum(time_in_seconds_array) / len(time_in_seconds_array)
    mops_total_mean = sum(mops_total_array) / len(mops_total_array)
    time_in_seconds_std = (sum([(x - time_in_seconds_mean) ** 2 for x in time_in_seconds_array]) / len(time_in_seconds_array)) ** 0.5
    mops_total_std = (sum([(x - mops_total_mean) ** 2 for x in mops_total_array]) / len(mops_total_array)) ** 0.5   
    
    results.append({
        "Flag": flag,
        "Threads": threads,
        "Time in ms": time_in_seconds_mean*1000,
        "Time in ms std": time_in_seconds_std*1000,   
        "Mop/s total": mops_total_mean,
        "Mop/s total std": mops_total_std,
        "Ver": ver
    })


print("Flag\tThreads\tMop/s\tMop/s std\tVer")

for result in results:
    # print(f"{result['Flag']}\t{result['Threads']}\t{result['Time in ms']:.0f}\t{result['Time in ms std']:.0f}\t{result['Mop/s total']:.2f}\t{result['Mop/s total std']:.2f}\t{result['Ver']}")
    print(
        f"{result['Flag']}\t{result['Threads']}\t"
        f"{result['Mop/s total']:.2f}\t"
        f"{result['Mop/s total std']:.2f}\t"
        f"{result['Ver']}"
    )
