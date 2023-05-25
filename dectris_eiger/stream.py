from .communication import get_value, set_value


class EigerStreamInterface(object):
    
    def __init__(self, host, port=80, api_version="1.5.0"):
        super(EigerStreamInterface, self).__init__()
        self._host = host
        self._port = port
        self._api_v = api_version
        
    def get_enabled(self, timeout=2.0):
        en = get_value(self._host, self._port, self._api_v, "stream",
                       "config", "mode", timeout=timeout,
                       return_full=False)
        return en == "enabled"
        
    def set_enabled(self, enabled, timeout=2.0):
        en = "enabled" if enabled else "disabled"
        set_value(self._host, self._port, self._api_v, "stream",
                  "config", "mode", en, timeout=timeout,
                  no_data=True)
                  
    enabled = property(get_enabled, set_enabled)
   
