#!/usr/bin/env python
"""
EIGER Debug Script

a) turn off detector server and detector head for 10 minutes. make sure dry air supply
as well as cooling is connected and running within the specs.

b) turn on the system. execute this script immediately afterwards. please do not
use any other control software or while using this script.

Usage: python DEigerDebug.py [detectorHostAdress] (e.g. 10.0.42.20)
Requires python2.7

What is happening?
i) restart DAQ & initialize detector
ii) dump all status parameters to file "detectorStatus_inital.json"
iii) set detector and filewriter parameters, arm detector, take some dark exposures.
iv) dump status parameters to file "detectorStatus_final.json"
v) download data & log files, zip information

c) please send the resulting data to support@dectris.com
"""

__author__ = "SasG"
__date__ = "17/03/06"
__version__ = "0.5"


import sys, time, os, re
import urllib, json, zipfile

from tools import DEigerClient

try:
    from tools import DModuleMap
    PLOTTABLE = True
except Exception as e:
    print "[WARNING] cannot plot temperatures", e
    PLOTTABLE = False

class DEigerDebugger():
    def __init__(self, host=None, fpath="."):
        self.host = host
        self.fpath = fpath
        if not os.path.exists(self.fpath):
            os.makedirs(self.fpath)
        if host:
            self.cam = self.initialize()

    def initialize(self):
        self.cam = DEigerClient.DEigerClient(self.host)
        print "[*] restart EIGER DAQ on host %s" %self.host
        assert self.cam.sendSystemCommand("restart") is ""
        time.sleep(3)
        print "[*] initialize EIGER host %s" %self.host
        assert self.cam.sendDetectorCommand("initialize") is ""
        self.dumpStatus("detectorStatus_initial")
        print "[*] initialize FileWriter host %s" %self.host
        assert self.cam.sendFileWriterCommand("initialize") is ""
        self.dumpStatus("detectorStatus_initial")
        return self.cam

    def dumpStatus(self, fname="detectorStatus"):
        filename = os.path.join(self.fpath,fname) + ".json"
        with open(filename, "w") as f:
            print "[*] update status %s" %self.host
            self.cam.sendDetectorCommand("status_update")
            print "[*] write status to %s" %filename
            status = {key: self.cam.detectorStatus(key) for key in self.cam.detectorStatus()}
            json.dump(status,f)
        return filename

    def dumpConfig(self, fname="detectorConfig"):
        filename = os.path.join(self.fpath,fname) + ".json"
        with open(filename, "w") as f:
            print "[*] write config to %s" %filename
            config = {key: self.cam.detectorConfig(key) for key in self.cam.detectorConfig()}
            json.dump(config,f)
        return filename

    def _configFileWriter(self, fname="EIGERDebug"):
        config = {"name_pattern": fname,"compression_enabled": True,"nimages_per_file": 1000,"mode":"enabled"}
        print "[*] configure file writer"
        for key, value in config.iteritems():
            print "\t[-] setting %s to %s" %(key, value)
            self.cam.setFileWriterConfig(key, value)

    def _configDetector(self,config):
        print "[*] configure detector"
        for key, value in config.iteritems():
            print "\t[-] setting %s to %s" %(key, value)
            self.cam.setDetectorConfig(key, value)
        self.cam.setDetectorConfig("pixel_mask_applied", False)



    def expose(self, fname="EIGERDebug", count_time=29.9, frame_time=30, nimages=10, ntrigger=144):
        config = {"nimages":nimages, "count_time":count_time,"frame_time":frame_time,
                "ntrigger":ntrigger, "trigger_mode": "ints", "compression":"bslz4"}

        try:
            self._configFileWriter(fname)
            self._configDetector(config)

            self.dumpConfig()

            print "[*] arming"
            self.cam.sendDetectorCommand("arm")

            for i in range(config["ntrigger"]):
                while self.cam.detectorStatus("state")["value"] != "ready":
                    time.sleep(1)
                    if self.cam.detectorStatus("state")["value"] in ["error","na"]:
                        raise RuntimeError("DETECTOR NOT AVAILABLE")

                self.dumpStatus("detectorStatus_%s" %time.strftime("%y%m%d_%H%M%S"))
                try:
                    if PLOTTABLE:
                        DModuleMap.plotTemperatures(self.fpath)
                except Exception as e:
                    print "[WARNING] could not save temperature plot", e
                print "[*] trigger %d/%d (%d s, abort with CTRL + C)" %(i+1, config["ntrigger"], config["frame_time"]*config["nimages"])
                self.cam.sendDetectorCommand("trigger")

            self.cam.sendDetectorCommand("disarm")

        except KeyboardInterrupt:
            print "[WARNING] user keyboard interrupt"
            self.cam.sendDetectorCommand("abort")
        except Exception as e:
            print "[ERROR]", e
        finally:
            print "[*] finished acquisition %s" %fname
            time.sleep(2)
        return fname

    def finish(self):
        self.dumpStatus("detectorStatus_final")
        self.getLogFile()
        dataname = self._compressFolder(self.fpath)

        msg = 80*"*"
        msg += "\n[FINISHED] please send %s to support@dectris.com:\n" %dataname
        msg += 80*"*"
        print msg

    def downloadData(self, fname):
        files = [f for f in self.cam.fileWriterFiles() if fname in f]
        print "[*] download files %s" %files
        for f in files:
            try:
                self.cam.fileWriterSave(f, self.fpath)
                print "\t[OK] %s" %f
            except Exception as e:
                print "\t[ERROR] could not download %s" %f
                print "\t%s" %e
        return True

    def getLogFile(self,fname="rest_api.log"):
        try:
            print "[*] download %s" %fname
            urllib.urlretrieve("http://%s/%s" %(self.host,fname), os.path.join(self.fpath,fname))
        except Exception as e:
            print "[ERROR] could not download rest_api.log"


    def _compressFolder(self, dname):
        zipname = dname + ".zip"
        print "[INFO] compressing %s to %s (this might take a while, maybe go grab a coffee)" %(dname, zipname)
        with zipfile.ZipFile(zipname, "w") as zf:
            for dirname, subdirs, files in os.walk(dname):
                zf.write(dirname)
                for filename in files:
                    fname = os.path.join(dirname, filename)
                    print "\t[-] adding", fname
                    zf.write(fname)
        return zipname

def getHost():
    try:
        host = sys.argv[1]
    except Exception as e:
        print "[ERROR] Specify EIGER Host,", e
        sys.exit(1)

    return host

if __name__ == "__main__":
    fpath = time.strftime("EIGERDebug" + "_%y%m%d_%H%M%S")
    debugger = DEigerDebugger(getHost(), fpath)
    debugger.expose(time.strftime(fpath), count_time=1, frame_time=1, nimages=60, ntrigger=20)
    debugger.downloadData(fpath)
    debugger.finish()
