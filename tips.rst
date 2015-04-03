================================================================================
Implementing a Storage service classes to save images/videos
================================================================================
------
Bob R.
------

Hello,

Please bear with me, as I'm a newbie I'm still trying to wrap my head around the
protocol. 

I am trying to accomplish the following task, I would like to use storescp.py 
(storage example from the typical use case) to create a listener service such 
that I will be able to send images/videos from two ultrasound machines (aloka 
prosound alpha 10 and the GE volusion 8). In short, I'd like to send dcm files 
from the machines to the listener service and save the image or video with the 
patient's file number from the metadata as the filename. How would you suggest 
I go about doing and testing the above without having constant access to the 
machines?

I'm trying to mimic a test environment as I have limited time with the afore-
mentioned machines.

I am using this code 

    https://code.google.com/p/pydicom/source/browse/source/
    dicom/contrib/pydicom_PIL.py

along with storescp.py to save a jpeg. It seems to work with single frame files.

So what I've done is start the listener on my linux VM and from my Mac OSX desk-
top I installed, OsiriX from http://www.osirix-viewer.com/ and set a DICM node 
for DICOM send, which is the listener. I then went this site 

    http://www.barre.nom.fr/medical/samples/#s-us 

for sample dcm files and attempted to send the images to the listener. So work 
and others do not.

So my questions are the following:

1) How would I distinguish between single or multiple frame dcm files from your 
   code? Am I right to assume that videos (that I wish to encode to avi) are 
   multiple frame dcm files from DICOM's point of view:

2) What values do I need here:

    file_meta.MediaStorageSOPInstanceUID = "1.2.3"  # !! Need valid UID here
    file_meta.ImplementationClassUID = "1.2.3.4"  # !!! Need valid UIDs here

3) Are the metadata fields in dcm files similar across all machines or scu's or 
   specific?

Thank you


--------------
Patrice Munger
--------------

Hi Bob,

| In short, I'd like to send dcm files from the machines to the listener service
| and save the image or video with the patient's file number from the metadata 
| as the filename
Just one precision. DICOM information is stored in datasets, which is a collec-
tion of DICOM elements. Which elements are present in a given dataset depends on
the type of object the dataset represents (CT image, RT Dose, US Image, etc). 
Patient name is one of the many elements of the dataset. Another one is pixel 
data. DICOM datasets do not necessarily have to reside in files. For instance, 
they can be shared through the network. But when datasets must be written to 
files, a few tags that are added to the file. These tags refer to the metadata.

| How would you suggest I go about doing and testing the above without having 
| constant access to the machines?
You could export some data from your US machines to a dcmtk's storescp which 
will give you some DICOM files. You can then test your pynetdicom's storescp by 
sending those files using dcmtk's storescu.  

| I am using this code 
|
|     https://code.google.com/p/pydicom/source/browse/source/
|     dicom/contrib/pydicom_PIL.py along with storescp.py 
|
| to save a jpeg. It seems to work with single frame files.
 
| 1) How would I distinguish between single or multiple frame dcm files from 
|    your code? Am I right to assume that videos (that I wish to encode to avi) 
|    are multiple frame dcm files from DICOM's point of view:
The DICOM dataset is passed to your callback. You can probably tell from this 
dataset if you have a single or multiple frame dataset, although I do not know 
exactly what tags to look at. You could search the pydicom group for more info 
on this.

| 2) What values do I need here:
|    file_meta.MediaStorageSOPInstanceUID = "1.2.3"  # !! Need valid UID here
|    file_meta.ImplementationClassUID = "1.2.3.4"  # !!! Need valid UIDs here
MediaStorageSOPInstanceUID should be the same as the SOPInstanceUID of the 
dataset, unless you modify the data; then you could generate a new UID using 
dicom.UID.generate_uid().

Since your using pydicom to write your files, I believe ImplementationClassUID 
should be that of pydicom, which is '1.2.826.0.1.3680043.8.498.1'. People from 
pydicom may wish to comment on that.

| 3) Are the metadata fields in dcm files similar across all machines or scu's 
|    or specific?
Metadata generally differ. But I believe the FileMetaInformationVersion is 
always the same.

I hope it helps!

Patrice


----------------
Stuart Swerdloff
----------------

| On Monday, 23 June 2014 00:52:00 UTC+12, Bob R. wrote:
| Hello,
| 
| Please bear with me, as I'm a newbie I'm still trying to wrap my head around 
| the protocol. 
| 
| I am trying to accomplish the following task, I would like to use storescp.py 
| (storage example from the typical use case) to create a listener service such 
| that I will be able to send images/videos from two ultrasound machines (aloka 
| prosound alpha 10 and the GE volusion 8). In short, I'd like to send dcm files
| from the machines to the listener service and save the image or video with the
| patient's file number from the metadata as the filename. How would you suggest
| I go about doing and testing the above without having constant access to the 
| machines?
| 
| I'm trying to mimic a test environment as I have limited time with the aforementioned machines.
| 
| I am using this code 
|
|     https://code.google.com/p/pydicom/source/browse/source/
|     dicom/contrib/pydicom_PIL.py 
|
|along with storescp.py to save a jpeg. It seems to work with single frame files.
| 
| So what I've done is start the listener on my linux VM and from my Mac OSX 
| desktop I installed, OsiriX from http://www.osirix-viewer.com/ and set a DICM 
| node for DICOM send, which is the listener. I then went this site 
| 
|     http://www.barre.nom.fr/medical/samples/#s-us 
|
| for sample dcm files and attempted to send the images to the listener. So work 
| and others do not.
|
| So my questions are the following:
| 
| 1) How would I distinguish between single or multiple frame dcm files from 
| your code? Am I right to assume that videos (that I wish to encode to avi) are
| multiple frame dcm files from DICOM's point of view:
| The SOP Class UIDs (See DICOM PS3.4, Section B.5 Standard SOP Classes):
Ultrasound Multi-frame Image Storage 1.2.840.10008.5.1.4.1.1.3.1 Ultrasound 
Multi-frame Image IOD 

Ultrasound Image Storage 1.2.840.10008.5.1.4.1.1.6.1 Ultrasound Image IOD

The SOP Class UID tag is (0x0008,0x0016).  You will need to use that tag if you 
receive the data over a DICOM association.  If you read it from a Part 10 file, 
then you will need to use (read) the MediaStorageSOPClassUID.

I would probably check the SOP Class UID tag first (especially if over an assoc-
iation), and if it isn't there, check the Media Storage SOP Class UID tag, and 
if that isn't there, complain loudly (about the information not being there).

|
| 2) What values do I need here:
|
|    file_meta.MediaStorageSOPInstanceUID = "1.2.3"  # !! Need valid UID here
|    file_meta.ImplementationClassUID = "1.2.3.4"  # !!! Need valid UIDs here
|
| 3) Are the metadata fields in dcm files similar across all machines or scu's 
|    or specific?
|
| Thank you



=================
Release Requested
=================
----------
Marc Ramos
----------

Hi there,
I would like to know when a request ends. In the end of a request there is this 
message: "Release requested"

In the AE file I found it inside the AE class:

    # check for release request
    if self.ACSE.CheckRelease():
        print "Release requested"
        self.Kill()

Is there a way to communicate the server that the transfer has finished from 
there? I am quite new with these dicom servers and I try to understand how it 
works really. I don't get this functions in the examples:

    MyAE.OnAssociateRequest = OnAssociateRequest
    MyAE.OnAssociateResponse = OnAssociateResponse
    MyAE.OnReceiveStore = OnReceiveStore
    MyAE.OnReceiveEcho = OnReceiveEcho

I have searched them in the AE class but didn't find it. How do they work?

Thanks,
M


--------------
Hrishikesh H.B
--------------

Hello Marc, 

Have you found a way to achieve this? I am also looking for the same. 



--------------
Patrice Munger
--------------

| Le vendredi 29 août 2014 11:35:10 UTC-4, Marc Ramos a écrit :
| Hi there,
| I would like to know when a request ends. In the end of a request there is 
| this message: "Release requested" 
| 
| In the AE file I found it inside the AE class:
|
|    # check for release request
|    if self.ACSE.CheckRelease():
|        print "Release requested"
|        self.Kill()
| 
The OnAssociateRequest, OnAssociateResponse,  OnReceiveStore and OnReceiveEcho 
are callback functions which are called by your AE when the corresponding events
occur. The user (you) have to write them. For what you request, I would suggest 
the following:

In the blocks that check for association release or abort, I would add a call to
a new user-defined callback function, i.e.

    # check for release request
    if self.ACSE.CheckRelease():
        if 'OnRelease' in self.AE.__dict__:
            self.AE.OnRelease()
        self.Kill()

    # check for abort
    if self.ACSE.CheckAbort():
        if 'OnAbort' in self.AE.__dict__:
            self.AE.OnAbort()
        self.Kill()

In your user code, define the OnRelease and OnAbort callbacks (in a way similar 
to other callbacks). They will be called when the association is about to get 
released or is aborted. 

Tell me if this approach works for you. If it does, I will add the new callbacks
in the next release.


Patrice