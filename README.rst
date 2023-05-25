Python API for the Dectris Eiger Detector
=========================================

Introduction
------------
The ``dectris_eiger`` Python package contains functions and classes to control
the *Dectris Eiger*  X-ray detector
(`product page <https://www.dectris.com/EIGER.html>`_) via its control unit's
REST interface. The API should work with Python 2.7 and Python 3.x. It depends
on the ``requests``
(`more information <http://docs.python-requests.org/en/latest/>`_) package for
HTTP communications.

Eventhough the API was developed for the *Dectris Eiger 1M* detector at the
LISA diffractometer at beamline P08 at DESY, it should also work with larger
versions of the detector.

For installation instructions, see the INSTALL.rst file.

Examples
--------
Assuming the Eiger control unit's IP address is *192.168.10.42*, acquiring
a series of data requires just a few lines:

.. code-block::

   from dectris_eiger.eiger import EigerDetector

   # create the API connector
   det = EigerDetector("192.168.10.42")
   # initialize the detector
   det.initialize()
   # prepare a series: 100 images, 0.1 second count time
   det.nimages = 100
   det.count_time = 0.1
   # arm and trigger
   det.arm()
   det.trigger()

The detector's filewriter subsystem can be accessed via the detector api's
``filewriter`` attribute, which points to a
``dectris_eiger.filewriter.EigerFileWriter`` instance. To set the number of
images per data file and the filename pattern::

  det.filewriter.images_per_file = 100
  det.filewriter.filename_pattern = "series_$id"

To access the detector's data file buffer, use the ``buffer`` atribute of the
detector, which points to a ``dectris_eiger.buffer.EigerDataBuffer`` instance.
Example::

  # list all files:
  det.buffer.files
  # Returns something like
  # [u'series_3_data_000001.h5', ... , u'series_1_master.h5']
  #
  # download all files of series 1 to /tmp:
  det.buffer.download("series_1*", "/tmp")
  # delete all data:
  det.clear_buffer()


Missing Features
----------------
The detector's monitor interface will be accessible in version 0.4.
