#!/usr/bin/env python

import h5py
import sys
import numpy as np
import tifffile
import os

import DModuleMap

Gap = 2
ChipLength = 256
ModuleGapWidth = 10
ModuleGapHeight = 37

BareHalfModuleWidth = 4*ChipLength
BareHalfModuleHeight = ChipLength
BareModuleWidth = BareHalfModuleWidth
BareModuleHeight = 2*BareHalfModuleHeight
HalfModuleWidth = BareHalfModuleWidth + 3*Gap
HalfModuleHeight = BareHalfModuleHeight + Gap/2
ModuleWidth = HalfModuleWidth
ModuleHeight = 2*HalfModuleHeight


def calib2mask(fname):
    ModuleMap = getModuleMap(fname)
    with h5py.File(fname,"r") as f:
        for key, value in ModuleMap.iteritems():
            data = f["entry/module_%03d/calibration_000/pixel_mask"%value["number"]][:].T
            if not value["pos"][-1]%2: # some rotation magic
                data = np.rot90(data,2)
            mdata = []
            for c in range(4): # add virtual pixels chip-wise
                c_start = c * ChipLength
                c_end = c_start + ChipLength
                chipdata = np.ndarray((ChipLength+2,ChipLength+2))
                chipdata[1:-1,1:-1] = data[c_start:c_start+ChipLength]
                chipdata[:,0] = chipdata[:,1]
                chipdata[:,-1] = chipdata[:,-2]
                chipdata[0,:] = chipdata[1,:]
                chipdata[-1,:] = chipdata[-2,:]
                mdata.append(chipdata)

            if value["pos"][-1]%2: # some more rotation magic
                ModuleMap[key]["mask"] = np.vstack(mdata)[1:-1,:-1]
            else:
                ModuleMap[key]["mask"] = np.vstack(mdata)[1:-1,1:]

    mask = np.ones((2070,2167)).astype("uint32")
    for key, value in ModuleMap.iteritems():
        x,y = value["pos"]
        x_start = x * (ModuleWidth+ModuleGapWidth)
        y_start = y/2 * (ModuleHeight+ModuleGapHeight) + (y%2) * HalfModuleHeight
        print "storing module %d at [%d,%d]" %(value["number"], x_start, y_start)
        mask[x_start:x_start+BareHalfModuleWidth+6,y_start:y_start+BareHalfModuleHeight+1] = value["mask"]
    return mask

def getModuleMap(fname):
    moduleMaps = {  2:DModuleMap.ModuleTable500K,
                    4:DModuleMap.ModuleTable1M,
                    16:DModuleMap.ModuleTable4M,
                    36:DModuleMap.ModuleTable9M,
                    64:DModuleMap.ModuleTable16M
                    }

    with h5py.File(fname,"r") as f:
        nModules = len([i for i in f["entry"].keys() if "module" in i])

    return moduleMaps[nModules]

if __name__ == "__main__":
    fname = sys.argv[1]
    mask = calib2mask(fname)
    fname = fname.replace(".h5","_pixelmask.tiff")
    tifffile.imsave(fname, mask.T)
    print "[OK] wrote %s" %fname
