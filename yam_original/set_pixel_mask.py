import eigerclient
import json
import numpy
from base64 import b64encode, b64decode
import h5py
import cPickle as pickle

eiger_host = "192.168.163.204"
e = eigerclient.DEigerClient(host=eiger_host)

pm = pickle.load(open("pixel_mask.pkl"))

new_conf = {
'__darray__': (1,0,0),
'type': pm.dtype.str,
'shape': pm.shape,
'filters': ['base64'],
'data': b64encode(pm.data) }

print e.setDetectorConfig("pixel_mask", new_conf)
