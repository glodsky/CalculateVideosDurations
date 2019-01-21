
import argparse
import datetime
import re
import subprocess 
from time import sleep
import os
import sys
from os import listdir
from os.path import isfile, join ,splitext , basename

  
def get_output(file_name): 
    process = subprocess.Popen(
        ["ffmpeg", "-i", file_name], 
        stderr = subprocess.PIPE,
        close_fds = True
    ) 
    output = ""
    iterations = 0
    # ensure the output contains "Duration"
    while(not "start" in output and iterations < 100):
        buffer_read = str(process.stderr.read())
        iterations += 1
        if(buffer_read != "None"):
            output += buffer_read
        #print(iterations)
        sleep(.01)
    return output
 
def get_videofiles(rootdir):
    vfs = []
    for fpathe,dirs,fs in os.walk(rootdir):
      for f in fs:
        if os.path.splitext(f)[1]=='.mp4':
            vfs.append (os.path.join(fpathe,f))
    return vfs

def get_durationfromstring(target):
    durations = []
    fle = len("Duration: 00:06:37.20") 
    fi = 0
    fnext =target.find("Duration",fi)
    while ( fnext  > 0 ):
        if(fnext>0):
            durations.append(target[fnext:fnext+fle])
            fi =  fnext+fle + 1
            fnext =target.find("Duration",fi)
            
def calculate_total(durations):
    total = datetime.timedelta()

    for duration in durations:
        time = datetime.datetime.strptime(duration, "%H:%M:%S.%f")

        time_delta = datetime.timedelta(
            hours = time.hour,
            minutes = time.minute,
            seconds = time.second,
            microseconds = time.microsecond
        )

        total += time_delta

    return total

def main():
    durations = []
    videos_infor = []
    regex = r"Duration:.+(\d\d:\d\d:\d\d\.\d\d)"
    
    curdir = input("video dir : ")
    videofiles = get_videofiles(curdir)
    for file_name in videofiles:
        output = get_output(file_name)
        save_result = "./d.txt"
        target = output[1:]
        if  os.path.exists(save_result):
            os.unlink(save_result)
        with open(save_result,'a+') as f:
            f.write(target)
            f.close()
        basename = os.path.basename(file_name)
        match = re.search(regex, target)
        if match:
            duration = match.group(1)                     
            videos_infor.append("%-20s  %5s"%(basename, duration))
            durations.append(duration)
            
    #sleep(1.5)
    for x in videos_infor:
        print(x)
    # manually format total from seconds due to lack of timedelta.strftime()
    print("\n========================")
    print("Total Files : %s"%len(videofiles))
    total = calculate_total(durations).total_seconds()
    minutes, seconds = divmod(total, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    print("\nTotal duration: {:.0f} days, {:.0f} hours, {:.0f} minutes, {:.2f}\
            seconds".format(days, hours, minutes, seconds))
    
if __name__ == "__main__":
    main()







 
