# -*- coding: utf-8 -*-
"""
.. module:: buffer
   :synopsis: This module contains an interface to the Dectris Eiger's data
              file buffer. It provides functions to list, retrieve and delete
              the buffered data.

.. moduleauthor:: Sven Festersen <festersen@physik.uni-kiel.de>
"""
import fnmatch
import json
import os
import requests


DOWNLOAD_CHUNK_SIZE = 1024 * 1024


def download_chunks(response, f):
    """
    Download a file opened as ``requests.Response`` into a file object.

    :param requests.Response response: the response object
    :param f: the file-like object to write to
    :type f: file-like
    :returns: number of bytes read
    :rtype: int
    """
    bytes_read = 0
    for chunk in response.iter_content(DOWNLOAD_CHUNK_SIZE):
        bytes_read += len(chunk)
        f.write(chunk)
    return bytes_read


class DataBufferError(Exception):
    pass


class UnknownDataFileError(DataBufferError):
    pass


class EigerDataBuffer(object):
    """
    Interface to the detector's data buffer which is accessible via WebDAV.
    """

    _base_dir = "/data"

    def __init__(self, host, port=80, api_version="1.0.0"):
        super(EigerDataBuffer, self).__init__()
        self._host = host
        self._port = port
        self._api_v = api_version

    def list_files(self):
        """
        Returns a list of all files in the data buffer.

        :returns: list of files in the buffer
        :rtype: list of string
        """
        fmt_data = {"host": self._host,
                    "port": self._port,
                    "api_version": self._api_v
                    }
        url = ("http://{host}:{port}/filewriter/api/"
               "{api_version}/files").format(**fmt_data)
        response = requests.get(url)
        filenames = json.loads(response.text)
        return filenames

    files = property(list_files)

    def get_file(self, filename):
        """
        Downloads a file's content and returns it.

        :param str filename: Data file name
        :returns: The file's content
        :rtype: bytes
        :raises UnknownDataFileError: if the data file can not be found
        """
        fmt_data = {"host": self._host,
                    "port": self._port,
                    "filename": filename
                    }
        url = "http://{host}:{port}/data/{filename}".format(**fmt_data)
        response = requests.get(url)
        if response.status_code == 200:
            return response.content
        else:
            raise UnknownDataFileError(filename)

    def download_file(self, filename, target_dir):
        """
        Downloads a file's content into a file with the same name in the
        given target directory.

        :param str filename: Data file name
        :param str target_dir: Local directory to save the file in
        :raises UnknownDataFileError: if the data file can not be found
        """
        fmt_data = {"host": self._host,
                    "port": self._port,
                    "filename": filename
                    }
        url = "http://{host}:{port}/data/{filename}".format(**fmt_data)
        response = requests.get(url)
        if response.status_code == 200:
            target_fn = os.sep.join([target_dir, filename])
            with open(target_fn, "wb") as f:
                download_chunks(response, f)
        else:
            raise UnknownDataFileError(filename)

    def download(self, filename_pattern, target_dir):
        """
        Similar to :py:meth:`.download_file`, but performs glob (*) expansion
        on the filename. All files matching the filename pattern are downloaded
        into the given directory.
        This can be used to download all files of a series::

          buffer.download("series_1*", "/tmp")

        :param str filename_pattern: Filename or glob pattern
        :param str target_dir: Local directory to save the file(s) in
        """
        filenames = fnmatch.filter(self.files, filename_pattern)
        for filename in filenames:
            self.download_file(filename, target_dir)

    def delete_file(self, filename):
        """
        Deletes the file given by the filename from the buffer.

        :param str filename: Data file to delete
        """
        fmt_data = {"host": self._host,
                    "port": self._port,
                    "filename": filename
                    }
        url = "http://{host}:{port}/data/{filename}".format(**fmt_data)
        response = requests.delete(url)

    def delete_all(self):
        """
        Deletes all files from the buffer.
        """
        for filename in self.files:
            self.delete_file(filename)

    def clear_buffer(self):
        """
        Alias for :py:meth:`delete_all`.
        """
        return self.delete_all()
