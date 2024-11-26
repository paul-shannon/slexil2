import pdb
import json
import traceback
import sys, io

def get_exception_traceback_str(exc: Exception) -> str:
    # Ref: https://stackoverflow.com/a/76584117/
    file = io.StringIO()
    traceback.print_exception(exc, file=file)
    return file.getvalue().rstrip()

try:
    x = 1/0
except Exception as e:
    print("--- exception caught")
    exc_info = sys.exc_info()
    #traceback.print_exception(*exc_info)
    xs = get_exception_traceback_str(e)
    print(xs)
    #json.dumps(e)
    pdb.set_trace()
    xyz = 99
