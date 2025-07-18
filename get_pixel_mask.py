#import eigerclient
#import eiger
import json
import numpy
from base64 import b64encode, b64decode
import h5py

#eiger_host = "192.168.163.204"
eiger_host = "10.178.231.43"

import DEigerClient
e = DEigerClient.DEigerClient(host=eiger_host)
tmp = e.detectorConfig("pixel_mask")
#open("junk.txt","w").write(json.dumps(tmp, indent=True))

pm = numpy.fromstring(b64decode(tmp["value"]["data"]), dtype=tmp["value"]["type"]).reshape(tmp["value"]["shape"])

mpath = "/entry/instrument/detector/detectorSpecific/pixel_mask"
pm10=h5py.File("/user/admin45/Data/250718_BL45XU/check02/noxray100_10hz_master.h5", "r")[mpath][:]
pm50=h5py.File("/user/admin45/Data/250718_BL45XU/check02/noxray100_50hz_master.h5", "r")[mpath][:]

print numpy.all(pm==pm10)
print numpy.all(pm==pm50)

print numpy.where(pm!=pm10)
