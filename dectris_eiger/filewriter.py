# -*- coding: utf-8 -*-
"""
.. module:: filewriter
   :synopsis: This module contains an interface to the Dectris Eiger's file
              writer subsystem.

.. moduleauthor:: Sven Festersen <festersen@physik.uni-kiel.de>
"""
#from .communication import get_value, set_value
from communication import get_value, set_value


class EigerFileWriter(object):
    """
    Interface to the Dectris Eiger detector's file writer subsystem. This
    interface can be used to configure filename patterns and storage details.
    """

    def __init__(self, host, port=80, api_version="1.0.0"):
        super(EigerFileWriter, self).__init__()
        self._host = host
        self._port = port
        self._api_v = api_version

    # status
    def get_status(self, timeout=2.0, return_full=False):
        """
        Returns the filewriter's status. The status can be one of "disabled",
        "ready", "acquire", and "error".

        :param float timeout: communication timeout in seconds
        :param bool return_full: whether to return the full response dict
        :returns: subsystem status
        :rytpe: str
        """
        return get_value(self._host, self._port, self._api_v, "filewriter",
                         "status", "state", timeout=timeout,
                         return_full=return_full)
    status = property(get_status)

    # available buffer space
    def get_available_space(self, timeout=2.0, return_full=False):
        """
        Return the available buffer space in KB.

        :param float timeout: communication timeout in seconds
        :param bool return_full: whether to return the full response dict
        :returns: free buffer space in KB
        :rytpe: int
        """
        return float(get_value(self._host, self._port, self._api_v, "detector",
                             "status", "builder/dcu_buffer_free", timeout=timeout,
                             return_full=return_full))

    available_space = property(get_available_space)

    # time
    def get_time(self, timeout=2.0, return_full=False):
        """
        Returns the filewriter's current system time.

        :param float timeout: communication timeout in seconds
        :param bool return_full: whether to return the full response dict
        :returns: time string
        :rytpe: str
        """
        return get_value(self._host, self._port, self._api_v, "filewriter",
                         "status", "time", timeout=timeout,
                         return_full=return_full)
    time = property(get_time)

    # transfer mode
    def get_transfer_mode(self, timeout=2.0, return_full=False):
        """
        Returns the transfer mode. Currently only "http" is supported.

        :param float timeout: communication timeout in seconds
        :param bool return_full: whether to return the full response dict
        :returns: the transfer mode
        :rytpe: str
        """
        return get_value(self._host, self._port, self._api_v, "filewriter",
                         "config", "transfer_mode", timeout=timeout,
                         return_full=return_full)

    def set_transfer_mode(self, mode, timeout=2.0):
        """
        Set the filewriter's transfer mode. Currently only "http" is
        supported.

        :param str mode: transfer mode
        :param float timeout: communication timeout in seconds
        """
        set_value(self._host, self._port, self._api_v, "filewriter",
                  "config", "transfer_mode", mode, timeout=timeout)
    transfer_mode = property(get_transfer_mode, set_transfer_mode)

    # number of images per file
    def get_images_per_file(self, timeout=2.0, return_full=False):
        """
        Returns the number of images stored in a single data file.

        :param float timeout: communication timeout in seconds
        :param bool return_full: whether to return the full response dict
        :returns: number of images per file
        :rytpe: int
        """
        return int(get_value(self._host, self._port, self._api_v, "filewriter",
                             "config", "nimages_per_file", timeout=timeout,
                             return_full=return_full))

    def set_images_per_file(self, n, timeout=2.0):
        """
        Set the number of images stored in a single data file.

        :param int n: number of images per file
        :param float timeout: communication timeout in seconds
        """
        set_value(self._host, self._port, self._api_v, "filewriter",
                  "config", "nimages_per_file", n, timeout=timeout,
                  no_data=True)
    images_per_file = property(get_images_per_file, set_images_per_file)

    # filename pattern
    def get_filename_pattern(self, timeout=2.0, return_full=False):
        """
        Returns the file naming pattern. The string ``$id`` is replaced by
        the series id.

        :param float timeout: communication timeout in seconds
        :param bool return_full: whether to return the full response dict
        :returns: the file naming pattern
        :rytpe: string
        """
        return get_value(self._host, self._port, self._api_v, "filewriter",
                         "config", "name_pattern", timeout=timeout,
                         return_full=return_full)

    def set_filename_pattern(self, pattern, timeout=2.0):
        """
        Set the file naming pattern. The string ``$id`` is replaced by the
        series id.

        :param str pattern: the file naming pattern
        :param float timeout: communication timeout in seconds
        """
        set_value(self._host, self._port, self._api_v, "filewriter",
                  "config", "name_pattern", pattern, timeout=timeout,
                  no_data=True)
    filename_pattern = property(get_filename_pattern, set_filename_pattern)

    # compression
    def get_compression_enabled(self, timeout=2.0, return_full=False):
        """
        Returns True if the LZ4 data compression is enabled, False otherwise.

        :param float timeout: communication timeout in seconds
        :param bool return_full: whether to return the full response dict
        :returns: True if compression is enable, False otherwise
        :rytpe: boolean
        """
        return get_value(self._host, self._port, self._api_v, "filewriter",
                         "config", "compression_enabled", timeout=timeout,
                         return_full=return_full)

    def set_compression_enabled(self, enabled, timeout=2.0):
        """
        Enable or disable LZ4 data compression.

        :param boolean enabled: set the data compression status
        :param float timeout: communication timeout in seconds
        """
        set_value(self._host, self._port, self._api_v, "filewriter",
                  "config", "compression_enabled", enabled, timeout=timeout,
                  no_data=True)
    compression_enabled = property(get_compression_enabled,
                                   set_compression_enabled)


if __name__ == "__main__":
    efw=EigerFileWriter("192.168.163.204")
    print(efw.get_available_space())
