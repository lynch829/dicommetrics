"""
This script attempts to parse the long text file outputed from
Pinnacle containing the DVH info; volume (%) versus dose (cGy).
"""

# Create a file handle.
filename = 'Fake_Patient_0000103167.txt'
filehandle = open(filename)

# Make a dictionary to hold metadata such as First Name, Last Name,
# MRN, Plan Name, Trial Name, Plan Version, Creation Date (of the txt
# file).
metadata = {}

# Make a dictionary to hold the various DVHs and bins. The histograms 
# are created using right edged bins of 5 cGy intervals.
DVHs = {}
DVHs['Dose [cGy]'] = []

# Read in the beginning portion of the file line by line to fill in the
# metadata. First skip the first five lines as they are just comments.
dummy = filehandle.readline()
dummy = filehandle.readline()
dummy = filehandle.readline()
dummy = filehandle.readline()
dummy = filehandle.readline()

# Capture the datetime that the text file was created on.
# Sample: 16:43:11 Mon 2015 Feb 2
Created = filehandle.readline().split()
metadata['Created'] = Created[7] + ' ' + \
                      Created[4] + ' ' + \
                      Created[8] + ' ' + \
                      Created[5] + ' ' + \
                      Created[6]

# Capture the MRN.
metadata['MRN'] = filehandle.readline().split()[1].zfill(10)

# Capture the Last Name.
metadata['LastName'] = filehandle.readline().split()[1]

# Capture the First Name
metadata['FirstName'] = filehandle.readline().split()[1]

# Capture the Plan Name.
metadata['PlanName'] = ' '.join(filehandle.readline().split()[1:])

# Capture the Plan Version.
metadata['PlanVersion'] = filehandle.readline().split()[2]

# Capture the Trial.
metadata['Trial'] = ' '.join(filehandle.readline().split()[2:])

# Capture bin size.
metadata['BinSize [cGy]'] = filehandle.readline().split()[1]

print 'Finished capturing the metadata.'

# Skip another line.
dummy = filehandle.readline()

# Set which structure is currently having its DVH data filled in.
CurrentStructure = ''

# Loop through the file, filling in the data into the above defined
# dictionaries as it goes.
for line in filehandle:
    LineSplit = line.split()
    if LineSplit[0] == 'Roi:':
        print 'Finished adding DVH data for: ' + CurrentStructure
        CurrentStructure = LineSplit[1]
        DVHs[CurrentStructure] = []
    elif LineSplit[0] == 'Trial:':
        continue
    else:
        DVHs['Dose [cGy]'].append(int(LineSplit[0])*5)
        DVHs[CurrentStructure].append(float(LineSplit[1]))

print 'done'
print DVHs['Dose [cGy]']
# END

"""
How to determine the volume (cc) for any dose (cGy), ie interpolate.

import scipy

f = scipy.interpolate.interp1d(x=DVHs['Dose [cGy]'], y=DVHs['Heart'], kind='linear')
f = scipy.interpolate.interp1d(x=DVHs['Dose [cGy]'], y=DVHs['Heart'], kind='cubic')
f = scipy.interpolate.InterpolatedUnivariateSpline(x=DVHs['Dose [cGy]'], y=DVHs['Heart'], k=3, ext='const')

print f(3400)
"""