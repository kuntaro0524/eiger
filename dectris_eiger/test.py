from buffer import EigerDataBuffer
from filewriter import EigerFileWriter

edb = EigerDataBuffer("192.168.163.204")
eff = EigerFileWriter("192.168.163.204")

print(eff.get_available_space())

try:
   filelist=edb.list_files()
   print(filelist)
except:
    print("ERROR")
