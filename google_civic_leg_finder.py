#!/usr/bin/python

# Import modules
import cgi, cgitb 
import urllib
import urllib2
import json
import HTML
import pycurl
import pprint
from io import BytesIO
##############################################################

# Create instance of FieldStorage 
form = cgi.FieldStorage() 

# Get data from fields
if form.getvalue('Address'):
   addressLine = form.getvalue('Address')
else:
   addressLine = ""
   
if form.getvalue('City'):
   city = form.getvalue('City')
else:
   city = ""

if form.getvalue('State'):
   state = form.getvalue('State')
else:
   state = ""

if form.getvalue('Zip'):
   zipcode = form.getvalue('Zip')
else:
   zipcode = ""

address=addressLine+" "+city+" "+state+" "+zipcode


#Gets the address
#address=raw_input("Enter Your Address: ")
#postData =  "{'address':'1263 Pacific Ave. Kansas City KS'}"
postData =  "{'address':"+"'"+address+"'}"


#Runs the CURL to the Civic API and sets the output as a dictionary
key="YOUR API KEY HERE"
c = pycurl.Curl()
data = BytesIO()
c.setopt(pycurl.URL, "https://www.googleapis.com/civicinfo/us_v1/representatives/lookup?key="+key)
c.setopt(pycurl.WRITEFUNCTION, data.write)
c.setopt(pycurl.HTTPHEADER, ["Content-Type: application/json"])
c.setopt(pycurl.POST, 1) 
c.setopt(pycurl.POSTFIELDS, postData)
c.perform()
c.close
repDict = json.loads(data.getvalue())
##############################################################

"""
Functions
"""

#Checks if name of the office is at our desired level
def checkName(officeName, level):
	potusList = ["President"]
	congressList =["United States House of Representatives", "United States Senate"]
	stateList = ["Governor","State House", "State Senate"]
	allNames = {}
	allNames = {"potus":potusList,
				"congress":congressList,
				"state":stateList}
	for singleName in allNames[level]:
		
		if singleName in officeName:
			
			return True
	return False

def deets(officials,repDict):
	"Get contact information for each elected official"
	
	def getSocialID(channels, media):
		"Get the requested social network ID"
		for channel in channels:
			for k,v in channel.iteritems():
				if v==media:
					return channel.get("id","").encode('utf-8')
						
	electeds=[]
	for electedID,electedDict in repDict['officials'].iteritems():
		for name, officialIDs in officials.iteritems():
			if electedID in officialIDs:
				singleElected=[]
				singleElected.append(name.encode('utf-8'))
				singleElected.append(electedDict.get('name',"").encode('utf-8'))
				singleElected.append(electedDict.get('photoUrl',"").encode('utf-8'))
				singleElected.append(electedDict.get('party',"").encode('utf-8'))
				phoneList=electedDict.get('phones',[])
				if phoneList:
					singleElected.append(phoneList[0].encode('utf-8'))
				else:
					singleElected.append("")
				#print electedDict.get('phones',"")[0]
				#singleElected.append(electedDict.get('phones',"")[0].encode('utf-8'))
				singleElected.append(electedDict.get('urls',"")[0].encode('utf-8'))		
				singleElected.append(getSocialID(electedDict.get("channels",[]),"Facebook"))
				singleElected.append(getSocialID(electedDict.get("channels",[]),"Twitter"))
				electeds.append(singleElected)
	return electeds


def getOfficials(repDict, level):
	"Filters the office id out of offices and gets offices[officialIds]" 
	officials= {}
	for officesID,officesDict in repDict['offices'].iteritems():
		if checkName(officesDict.get('name'),level):
			officials[officesDict.get('name')]=officesDict.get('officialIds',[])
	return officials	
################################################################
# Create instance of FieldStorage 

#print deets(getOfficials(repDict, "potus"), repDict)
combinedHTML = ""
if form.getvalue('national'):
	combinedHTML = combinedHTML + HTML.table(deets(getOfficials(repDict, "potus"), repDict), header_row=['Office','Name','Photo','Party','Phone','Website','Facebook','Twitter'])	
if form.getvalue('federal'):
	combinedHTML = combinedHTML + HTML.table(deets(getOfficials(repDict, "congress"), repDict), header_row=['Office','Name','Photo','Party','Phone','Website','Facebook','Twitter'])
if form.getvalue('state1'):
	combinedHTML = combinedHTML + HTML.table(deets(getOfficials(repDict, "state"), repDict), header_row=['Office','Name','Photo','Party','Phone','Website','Facebook','Twitter'])
if form.getvalue('local'):
	combinedHTML = combinedHTML + HTML.table(deets(getOfficials(repDict, "local"), repDict), header_row=['Office','Name','Photo','Party','Phone','Website','Facebook','Twitter'])

#print deets(officials, repDict)
#htmlcode = HTML.table(deets(getOfficials(repDict, "stateLeg"), repDict), header_row=['Office','Name','Photo','Party','Phone','Website','Facebook','Twitter'])

print "Content-type:text/html\r\n\r\n"
print "<html>"
print '<head> \
		<meta charset="utf-8">\
		<meta http-equiv="X-UA-Compatible" content="IE=edge">\
		<meta name="viewport" content="width=device-width, initial-scale=1">\
		<title>Mobile Constituent</title>\
\
    <!-- Bootstrap -->\
    <link href="css/bootstrap.min.css" rel="stylesheet">\
\
    <!-- HTML5 Shim and Respond.js IE8 support of HTML5 elements and media queries -->\
    <!-- WARNING: Respond.js doesnt work if you view the page via file:// -->\
    <!--[if lt IE 9]>\
      <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>\
      <script src="https://oss.maxcdn.com/libs/respond.js/1.4.2/respond.min.js"></script>\
    <![endif]-->\
	</head>'
print "<title>Mobile Constituent</title>"
print "</head>"
print "<body>"
print combinedHTML
print "</body>"

