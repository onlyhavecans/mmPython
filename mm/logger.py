
class SessionLogger(object):
    """
    Making this a class will allow us to extend this with "plugins" later
    """
    def __init__(self, logfile):
        self.file = logfile

    def log(self, message):
        """Write a message to the file."""
        self.file.write("{}\n".format(message))
        self.file.flush()

    def close(self):
        self.file.close()