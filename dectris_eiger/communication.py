# -*- coding: utf-8 -*-
import json
import requests


def get_value(host, port, api_version, subsystem, section, key, timeout=2,
              return_full=False):
    """
    Get a value from the detector. If return_full is True, the complete return
    value (a dict) is returned.
    """
    conf = dict(host=host, port=port, sys=subsystem, version=api_version,
                section=section, key=key)
    url_fmt = "http://{host}:{port}/{sys}/api/{version}/{section}/{key}"
    url = url_fmt.format(**conf)
    print(url)

    response = requests.get(url, timeout=timeout)
    data = json.loads(response.text)
    if return_full:
        return data
    else:
        return data["value"]


def set_value(host, port, api_version, subsystem, section, key, value,
              timeout=2.0, no_data=False):
    """
    Set a value.
    """
    conf = dict(host=host, port=port, sys=subsystem, version=api_version,
                section=section, key=key)
    url_fmt = "http://{host}:{port}/{sys}/api/{version}/{section}/{key}"
    url = url_fmt.format(**conf)
    payload = json.dumps({"value": value})
    headers = {"Content-type": "application/json"}
    response = requests.put(url, timeout=timeout, data=payload,
                            headers=headers)
    if no_data:
        return None
    data = json.loads(response.text)
    return data
