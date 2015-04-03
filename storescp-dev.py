"""
Storage SCP example.

This demonstrates a simple application entity that support a number of
Storage service classes. For this example to work, you need an SCU
sending to this host on specified port.

For help on usage, 
python storescp.py -h 
"""

import argparse
from netdicom import AE, StorageSOPClass, VerificationSOPClass
from dicom.dataset import Dataset, FileDataset
import tempfile

# parse commandline
parser = argparse.ArgumentParser(description='storage SCP example')
parser.add_argument('port', type=int, default=104)
parser.add_argument('-aet', help='AE title of this server', default='DCMMETRICS')
args = parser.parse_args()


# callbacks
def OnAssociateRequest(association):
    print "association requested"


def OnAssociateResponse(association):
    print "Association response received"


def OnReceiveEcho(self):
    print "Echo received"


def OnReceiveStore(SOPClass, DS):
    print "Received C-STORE"
    # do something with dataset. For instance, store it on disk.
    file_meta = Dataset()
    file_meta.MediaStorageSOPClassUID = DS.SOPClassUID
    file_meta.MediaStorageSOPInstanceUID = DS.SOPInstanceUID # Change to my own UID via dicom.UID.generate_uid() though I should make sure such genereated UIDs use my orgroot.
    file_meta.ImplementationClassUID = "1.2.826.0.1.3680043.9.5066.0"  # My UID for my implementation, with a '.0' appended to it to represent development testing, ie the UID I got from Medical Connections.
    file_meta.ImplementationVersionName = "DICOMMETRICS-DEV" # My implementation version name. Remember to change this for each version. Remember to correspondingly change the ImplementationClassUID too.
    filename = '%s/%s.dcm' % (tempfile.gettempdir(), DS.SOPInstanceUID)
    ds = FileDataset(filename, {}, file_meta=file_meta, preamble="\0" * 128)
    ds.update(DS)
    ds.is_little_endian = True
    ds.is_implicit_VR = True
    ds.save_as(filename)
    print "File %s written" % filename
    # must return appropriate status
    return SOPClass.Success


# setup AE
MyAE = AE(args.aet, args.port, [], [StorageSOPClass, VerificationSOPClass])
MyAE.OnAssociateRequest = OnAssociateRequest
MyAE.OnAssociateResponse = OnAssociateResponse
MyAE.OnReceiveStore = OnReceiveStore
MyAE.OnReceiveEcho = OnReceiveEcho

# start AE
print "starting AE ... ",
MyAE.start()
print "done"
MyAE.QuitOnKeyboardInterrupt()
