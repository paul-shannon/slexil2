class MillisecondTimeError(ValueError):
    def __init__(self, timeString):
        self.timeString = timeString
    def __str__(self): 
        return("MillisecondTimeError, expected int, got: %s" % repr(self.timeString))

class MediaFormatError(ValueError):
    def __init__(self, urlsSupported, urlFound):
        self.urlsSupported = urlsSupported
        self.urlFound = urlFound
    def __str__(self): 
        supported = ", ".join(self.urlsSupported)
        return("MediaFormatErrofError, expected one of %s, found: %s" % \
                 (repr(supported), repr(self.urlFound)))

class MediaFileMissingError(ValueError):
    pass

class MediaFileFormatUnrecognizedMissingError(ValueError):
    pass

class NoTimeAlignedTierLines(ValueError):
    pass


   
