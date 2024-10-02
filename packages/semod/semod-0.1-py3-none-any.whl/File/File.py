import struct
import time
logfile=open('log.log','wb')
print("\nWARNING : The File may have too many terminators.\nSystem may fail to respond. Run this code with Caution.")
secs=23
while secs:
    secs-=1
    time.sleep(1)
    print(f"{0}:{secs}",end="\r")
for i in range(9000000000000000):
    logfile.write(struct.pack('>i',0o2)) #0o3



























#R = Read
#W = Write
#A = Append
#x = create