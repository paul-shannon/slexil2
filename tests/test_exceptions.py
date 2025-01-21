from slexil.exceptions import *
import pdb
import os
#--------------------------------------------------------------------------------
def test_MillisecondTimeError():

   print("--- test_MillisecondTimeError")

   times = [32, "1h20m58.871s", "1h21m02.203s", "1h20m54.237s", "1h20m56.973s"]
   try:
      for time in times:
        print("time: %s   type: %s" % (time, type(time)))
        if type(time) != int:
          raise MillisecondTimeError(time)
   except MillisecondTimeError as tme:
       print("MTE exception successfully raised")
       print(repr(tme))

#--------------------------------------------------------------------------------   
# shows how to catch, re-represent and then raise a context specific error
def test_MillisecondTimeError_afterValueError():

   print("--- test_MillisecondTimeError_afterValueError")

   try:

      times = [32, "1h20m58.871s", "1h21m02.203s", "1h20m54.237s", "1h20m56.973s"]
      try:
         for time in times:
           print("time: %s   type: %s" % (time, type(time)))
           intTime = int(time)
      except ValueError as ve:
         # cryptic "None" suppresses the ValueError display
         raise(MillisecondTimeError(time)) from None

   except MillisecondTimeError as tme:
       print("MTE exception successfully raised out of ValueError")
       print("Error!  expected integer milliseconds, found: '%s'" % tme.args[0])
   
#--------------------------------------------------------------------------------
def test_MediaFormatError():

   print("--- test_MediaFormatError")

   videoExtensions = [".m4v", ".mov", ".mp4"]
   audioExtensions = [".wav"] # , ".mp3")
   supported =  videoExtensions + audioExtensions

   testers = ["tmp0.m4v", "tmp1.mov", "tmp2.mp4", "tmp3.ogg",
              "tmp4.wave", "tmp5.wav"]
   try:
      for x in testers:
        urlSuffix = os.path.splitext(x)[1].lower()
        print("--- testing %s" % x)
        if urlSuffix not in supported:
          raise MediaFormatError(supported, urlSuffix)
   except MediaFormatError as mfe:
       print("MFE exception successfully raised")
       print(mfe)

#--------------------------------------------------------------------------------   
def runTests():

   test_MillisecondTimeError()
   test_MillisecondTimeError_afterValueError()

   test_MediaFormatError()

#----------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    runTests()
   
