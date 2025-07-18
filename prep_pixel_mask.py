from yamtbx.dataproc import eiger
import h5py
import numpy
import cPickle as pickle

flag_bit = 3 # over responding
hot_threshold = 1

def run(h5in):
  h = h5py.File(h5in, "r")
  current_pm = h["/entry/instrument/detector/detectorSpecific/pixel_mask"][:]

  hot_count = numpy.zeros(shape=current_pm.shape, dtype=numpy.uint32)
  n_tested = 0
  for i in xrange(100):
    data = eiger.extract_data(h5in, i+1)
    if data is None: break
    hot_count[numpy.where(data >= hot_threshold)] += 1
    n_tested += 1

  for n in numpy.unique(hot_count):
    if n == 0: continue
    print "  %6d times (%3d pixels)" % (n, numpy.sum(hot_count==n))

  rhs = numpy.zeros(shape=data.shape, dtype=current_pm.dtype)
  rhs[hot_count>n_tested//2] = 2**flag_bit
  print "Detected %d over-responding pixels" % numpy.sum(rhs>0)
  wh = numpy.where(rhs>0)
  for x, y in zip(wh[0], wh[1]):
    print " %5d %4d" % (y, x)

  new_pm = current_pm | rhs

  pickle.dump(new_pm, open("pixel_mask.pkl", "w"), -1)

  from yamtbx.dataproc import cbf
  cbf.save_numpy_data_as_cbf(new_pm.flatten(),
                                   size1=new_pm.shape[1], size2=new_pm.shape[0], title="pixel_mask",
                                   cbfout="test_pixel_mask.cbf")


if __name__ == "__main__":
  import sys
  run(sys.argv[1])
