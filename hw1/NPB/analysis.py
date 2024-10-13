import os
import re
import json

#get arguments from command line
import sys
args = sys.argv
folder_path = '/home/Students/sqp17/hpc_homework/hw1/NPB/result'
exp_path = args[1]
path = os.path.join(folder_path, exp_path)
log_files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]


results = []

pattern_threads = re.compile(r"Threads\s*=\s*(\d+)")
pattern_time = re.compile(r"Time in seconds\s*=\s*([\d.]+)")
pattern_mops = re.compile(r"Mop/s total\s*=\s*([\d.]+)")
pattern_verification = re.compile(r"Verification\s*=\s*(SUCCESSFUL|UNSUCCESSFUL)")


for log_file in log_files:
    file_path = os.path.join(folder_path, exp_path, log_file)
    with open(file_path, 'r') as f:
        content = f.read()
        
        
        threads = pattern_threads.search(content)
        time_in_seconds = pattern_time.search(content)
        mops_total = pattern_mops.search(content)
        
        if threads and time_in_seconds and mops_total:
            results.append({
                "Flag": log_file.replace('.log', '').split('-')[0],
                "Threads": int(threads.group(1)),
                "Time in seconds": float(time_in_seconds.group(1)),
                "Mop/s total": float(mops_total.group(1)),
                "Ver": pattern_verification.search(content).group(1)
            })
            

print("Flag\tThreads\tTime/s\tMop/s\tVer")

for result in results:
    print(f"{result['Flag']}\t{result['Threads']}\t{result['Time in seconds']}\t{result['Mop/s total']}\t{result['Ver']}")
