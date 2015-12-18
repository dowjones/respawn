class RespawnResourceError(Exception):
    def __init__(self, error_string, resource_type, resource_name=""):
        super(RespawnResourceError, self).__init__(resource_type + ": " + resource_name + ": " + error_string)