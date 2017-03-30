import os
import zipfile
import sys

if "build" in sys.argv:
    zf = zipfile.PyZipFile('idty_proof.zip', mode='w')
    try:
        zf.writepy('idty_proof')
    finally:
        zf.close()
    for name in zf.namelist():
        print(name)
