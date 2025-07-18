import numpy as np
import matplotlib.pylab as plt
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib
from pylab import MaxNLocator
import glob
import dateutil
import os, json, re, sys

ModuleTable500K = {
0x1100 : { 'pos':[0,0], 'rot': 0, 'number':0},
0x1110 : { 'pos':[0,1], 'rot': 0, 'number':1},
}

ModuleTable1M = {
0x1100 : { 'pos':[0,0], 'rot': 0, 'number':0},
0x1110 : { 'pos':[0,1], 'rot': 0, 'number':1},
0x1120 : { 'pos':[0,2], 'rot': 0, 'number':2},
0x1130 : { 'pos':[0,3], 'rot': 0, 'number':3},
}

ModuleTable4M = {
0x1170 : { 'pos':[0,0], 'rot': 0, 'number':7},
0x1150 : { 'pos':[0,1], 'rot': 0, 'number':5},
0x1120 : { 'pos':[0,2], 'rot': 0, 'number':2},
0x1100 : { 'pos':[0,3], 'rot': 0, 'number':0},
0x1160 : { 'pos':[0,4], 'rot': 0, 'number':6},
0x1140 : { 'pos':[0,5], 'rot': 0, 'number':4},
0x1130 : { 'pos':[0,6], 'rot': 0, 'number':3},
0x1110 : { 'pos':[0,7], 'rot': 0, 'number':1},
0x11B0 : { 'pos':[1,0], 'rot': 0, 'number':11},
0x1190 : { 'pos':[1,1], 'rot': 0, 'number':9},
0x11E0 : { 'pos':[1,2], 'rot': 0, 'number':14},
0x11C0 : { 'pos':[1,3], 'rot': 0, 'number':12},
0x11A0 : { 'pos':[1,4], 'rot': 0, 'number':10},
0x1180 : { 'pos':[1,5], 'rot': 0, 'number':8},
0x11F0 : { 'pos':[1,6], 'rot': 0, 'number':15},
0x11D0 : { 'pos':[1,7], 'rot': 0, 'number':13},
}

ModuleTable9M = {
0x3120 : { 'pos':[0,0], 'rot': 0, 'number':19},
0x3100 : { 'pos':[0,1], 'rot': 0, 'number':18},
0x31C0 : { 'pos':[0,2], 'rot': 0, 'number':25},
0x31E0 : { 'pos':[0,3], 'rot': 0, 'number':26},
0x3190 : { 'pos':[0,4], 'rot': 0, 'number':23},
0x31B0 : { 'pos':[0,5], 'rot': 0, 'number':24},
0x41E0 : { 'pos':[0,6], 'rot': 0, 'number':35},
0x41C0 : { 'pos':[0,7], 'rot': 0, 'number':34},
0x41B0 : { 'pos':[0,8], 'rot': 0, 'number':33},
0x4190 : { 'pos':[0,9], 'rot': 0, 'number':32},
0x4150 : { 'pos':[0,10], 'rot': 0, 'number':29},
0x4170 : { 'pos':[0,11], 'rot': 0, 'number':31},
0x3170 : { 'pos':[1,0], 'rot': 0, 'number':22},
0x3150 : { 'pos':[1,1], 'rot': 0, 'number':21},
0x21E0 : { 'pos':[1,2], 'rot': 0, 'number':16},
0x21C0 : { 'pos':[1,3], 'rot': 0, 'number':15},
0x2100 : { 'pos':[1,4], 'rot': 0, 'number':9},
0x2120 : { 'pos':[1,5], 'rot': 0, 'number':10},
0x11C0 : { 'pos':[1,6], 'rot': 0, 'number':7},
0x11E0 : { 'pos':[1,7], 'rot': 0, 'number':8},
0x1190 : { 'pos':[1,8], 'rot': 0, 'number':4},
0x11B0 : { 'pos':[1,9], 'rot': 0, 'number':6},
0x4100 : { 'pos':[1,10], 'rot': 0, 'number':27},
0x4120 : { 'pos':[1,11], 'rot': 0, 'number':28},
0x3130 : { 'pos':[2,0], 'rot': 0, 'number':20},
0x21F0 : { 'pos':[2,1], 'rot': 0, 'number':17},
0x21B0 : { 'pos':[2,2], 'rot': 0, 'number':14},
0x2190 : { 'pos':[2,3], 'rot': 0, 'number':13},
0x2150 : { 'pos':[2,4], 'rot': 0, 'number':11},
0x2170 : { 'pos':[2,5], 'rot': 0, 'number':12},
0x1120 : { 'pos':[2,6], 'rot': 0, 'number':1},
0x1100 : { 'pos':[2,7], 'rot': 0, 'number':0},
0x1170 : { 'pos':[2,8], 'rot': 0, 'number':3},
0x1150 : { 'pos':[2,9], 'rot': 0, 'number':2},
0x11A0 : { 'pos':[2,10], 'rot': 0, 'number':5},
0x4160 : { 'pos':[2,11], 'rot': 0, 'number':30}
}

ModuleTable16M = {
0x21B0 : { 'pos':[0,0], 'rot': 0, 'number':27},
0x2190 : { 'pos':[0,1], 'rot': 0, 'number':25},
0x21E0 : { 'pos':[0,2], 'rot': 0, 'number':30},
0x21C0 : { 'pos':[0,3], 'rot': 0, 'number':28},
0x2170 : { 'pos':[0,4], 'rot': 0, 'number':23},
0x2150 : { 'pos':[0,5], 'rot': 0, 'number':21},
0x2120 : { 'pos':[0,6], 'rot': 0, 'number':18},
0x2100 : { 'pos':[0,7], 'rot': 0, 'number':16},
0x21A0 : { 'pos':[1,0], 'rot': 0, 'number':26},
0x2180 : { 'pos':[1,1], 'rot': 0, 'number':24},
0x21F0 : { 'pos':[1,2], 'rot': 0, 'number':31},
0x21D0 : { 'pos':[1,3], 'rot': 0, 'number':29},
0x2160 : { 'pos':[1,4], 'rot': 0, 'number':22},
0x2140 : { 'pos':[1,5], 'rot': 0, 'number':20},
0x2130 : { 'pos':[1,6], 'rot': 0, 'number':19},
0x2110 : { 'pos':[1,7], 'rot': 0, 'number':17},
0x41B0 : { 'pos':[0,8], 'rot': 0, 'number':59},
0x4190 : { 'pos':[0,9], 'rot': 0, 'number':57},
0x41E0 : { 'pos':[0,10], 'rot': 0, 'number':62},
0x41C0 : { 'pos':[0,11], 'rot': 0, 'number':60},
0x4170 : { 'pos':[0,12], 'rot': 0, 'number':55},
0x4150 : { 'pos':[0,13], 'rot': 0, 'number':53},
0x4120 : { 'pos':[0,14], 'rot': 0, 'number':50},
0x4100 : { 'pos':[0,15], 'rot': 0, 'number':48},
0x41A0 : { 'pos':[1,8], 'rot': 0, 'number':58},
0x4180 : { 'pos':[1,9], 'rot': 0, 'number':56},
0x41F0 : { 'pos':[1,10], 'rot': 0, 'number':63},
0x41D0 : { 'pos':[1,11], 'rot': 0, 'number':61},
0x4160 : { 'pos':[1,12], 'rot': 0, 'number':54},
0x4140 : { 'pos':[1,13], 'rot': 0, 'number':52},
0x4130 : { 'pos':[1,14], 'rot': 0, 'number':51},
0x4110 : { 'pos':[1,15], 'rot': 0, 'number':49},
0x1160 : { 'pos':[2,0], 'rot': 0, 'number':6},
0x1140 : { 'pos':[2,1], 'rot': 0, 'number':4},
0x1130 : { 'pos':[2,2], 'rot': 0, 'number':3},
0x1110 : { 'pos':[2,3], 'rot': 0, 'number':1},
0x1180 : { 'pos':[2,4], 'rot': 0, 'number':8},
0x11A0 : { 'pos':[2,5], 'rot': 0, 'number':10},
0x11D0 : { 'pos':[2,6], 'rot': 0, 'number':13},
0x11F0 : { 'pos':[2,7], 'rot': 0, 'number':15},
0x1170 : { 'pos':[3,0], 'rot': 0, 'number':7},
0x1150 : { 'pos':[3,1], 'rot': 0, 'number':5},
0x1120 : { 'pos':[3,2], 'rot': 0, 'number':2},
0x1100 : { 'pos':[3,3], 'rot': 0, 'number':0},
0x1190 : { 'pos':[3,4], 'rot': 0, 'number':9},
0x11B0 : { 'pos':[3,5], 'rot': 0, 'number':11},
0x11C0 : { 'pos':[3,6], 'rot': 0, 'number':12},
0x11E0 : { 'pos':[3,7], 'rot': 0, 'number':14},
0x3160 : { 'pos':[2,8], 'rot': 0, 'number':38},
0x3140 : { 'pos':[2,9], 'rot': 0, 'number':36},
0x3130 : { 'pos':[2,10], 'rot': 0, 'number':35},
0x3110 : { 'pos':[2,11], 'rot': 0, 'number':33},
0x3180 : { 'pos':[2,12], 'rot': 0, 'number':40},
0x31A0 : { 'pos':[2,13], 'rot': 0, 'number':42},
0x31D0 : { 'pos':[2,14], 'rot': 0, 'number':45},
0x31F0 : { 'pos':[2,15], 'rot': 0, 'number':47},
0x3170 : { 'pos':[3,8], 'rot': 0, 'number':39},
0x3150 : { 'pos':[3,9], 'rot': 0, 'number':37},
0x3120 : { 'pos':[3,10], 'rot': 0, 'number':34},
0x3100 : { 'pos':[3,11], 'rot': 0, 'number':32},
0x3190 : { 'pos':[3,12], 'rot': 0, 'number':41},
0x31B0 : { 'pos':[3,13], 'rot': 0, 'number':43},
0x31C0 : { 'pos':[3,14], 'rot': 0, 'number':44},
0x31E0 : { 'pos':[3,15], 'rot': 0, 'number':46}
}

def temp2map(tempList):
    detTypes = {2:{"table":ModuleTable500K,"dimensions":[2,1]},
                4:{"table":ModuleTable1M,"dimensions":[4,1]},
                16:{"table":ModuleTable4M,"dimensions":[8,2]},
                36:{"table":ModuleTable9M,"dimensions":[12,3]},
                64:{"table":ModuleTable16M,"dimensions":[16,4]}}

    nModules = _find_nearest(detTypes.keys(), len(tempList))
    table = detTypes[nModules]["table"]
    heatmap = np.zeros(detTypes[nModules]["dimensions"])
    for module, temp in tempList.iteritems():
            for geometry in table.itervalues():
                if geometry["number"] == int(module):
                    heatmap[geometry["pos"][-1],geometry["pos"][0]] = temp
    return heatmap

def _find_nearest(array,value):
    return min(array, key=lambda x:abs(x-value))

def plotTemperatures(fpath=".", fname="tempPlot.pdf"):

    files = sorted(glob.iglob(os.path.join(fpath,"detectorStatus*.json")),
                    key=os.path.getctime)
    temperatures = dict()
    for f in files:
        with open(f,"r") as f:
            for key, value in json.load(f).iteritems():
                if key.startswith("module_") and key.endswith("temp"):
                    entry = {"tstamp":dateutil.parser.parse(value["time"]),
                            "value":value["value"]}
                    try:
                        temperatures[key].append(entry)
                    except KeyError:
                        temperatures[key] = [entry]

    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, sharex='col')
    matplotlib.rcParams.update({'font.size': 8, 'legend.fontsize': 6})
    ax1.set_title("FPGA temperature")
    ax2.set_title("min temperature map")
    ax3.set_title("module temperature")
    ax4.set_title("max temperature map")

    ax3.set_ylabel("temperature [C]")
    ax1.set_ylabel("temperature [C]")

    maxT, minT = {}, {}
    for key, value in sorted(temperatures.iteritems()):
        time = [entry["tstamp"] for entry in value]
        temp = [entry["value"] for entry in value]
        if "fpga" in key:
            ax1.plot(time,temp,label=key.split("/")[0])
        else:
            ax3.plot(time,temp,label=key)
            maxT[re.findall("\d+",key)[0]] = max(temp)
            minT[re.findall("\d+",key)[0]] = min(temp)

    initialMap = temp2map(minT)
    latestMap = temp2map(maxT)

    extent=[0,initialMap.shape[1],initialMap.shape[0],0]
    heatmap = ax2.imshow(initialMap, cmap='jet', interpolation=None, aspect='auto',
                 vmin=40, vmax=65, extent=extent)

    ax4.imshow(latestMap, cmap='jet', interpolation='none', aspect='auto',
                vmin=40, vmax=65,extent=extent)

    ax2.grid(True)
    ax4.grid(True)
    ax4.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax4.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax2.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax2.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax1.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax3.yaxis.set_major_locator(MaxNLocator(integer=True))

    box = ax1.get_position()
    ax1.set_position([box.x0*1.4, box.y0, box.width, box.height])
    box = ax3.get_position()
    ax3.set_position([box.x0*1.4, box.y0, box.width, box.height])

    ax1.legend(bbox_to_anchor=(-0.15, 1.0))

    ax3.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%H:%M:%S'))
    plt.setp(ax3.get_xticklabels(), rotation=15)

    cbar = fig.add_axes([0.92, 0.15, 0.02, 0.7])
    plt.colorbar(heatmap, cax = cbar)

    fname = os.path.join(fpath, fname)
    with PdfPages(fname) as p:
        p.savefig(fig)
    print("[*] plotted temperature data in %s" %fname)
    plt.close(fig)
