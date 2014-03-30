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

#Gets the address
address=raw_input("Enter Your Address: ")
#postData =  "{'address':'1263 Pacific Ave. Kansas City KS'}"
postData =  "{'address':"+"'"+address+"'}"

#Runs the CURL to the Civic API and sets the output as a dictionary
key="AIzaSyCbfuei5igyBXzm2lUAid7Lt0sxIqhDBfY"
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

#Checks the name of the office to filter for US House/Senate
def checkName(name):
	if "United States House of Representatives" in name:
		return "USRep"
	elif "United States Senate" in name:
		return "USSen"
	else:
		return False

#Gets us our shiz
#def deets(electedIDs):
	
	
################################################################


"""
#Filters the scope out of division and gets scope[officeIds]
officeIDs= []
for division,divDict in repDict['divisions'].iteritems():
	if divDict.get('scope', 0) in ['congressional','statewide']:
		officeIDs=officeIDs + divDict.get('officeIds',[])	

#Filters the office id out of offices and gets offices[officialIds] 
officialIDs= []
for officesID,officesDict in repDict['offices'].iteritems():
	#print officesID
	if officesID in officeIDs and checkName(officesDict.get('name')):
		officialIDs=officialIDs + officesDict.get('officialIds',[])		

#Filters the name out of officials to make officials[name] 
electeds=[]
for electedID,electedDict in repDict['officials'].iteritems():
	if electedID in officialIDs:
		electeds.append(electedDict.get('name').encode('utf-8'))
"""

#Filters the office id out of offices and gets offices[officialIds] 
officials= {}
for officesID,officesDict in repDict['offices'].iteritems():

	if checkName(officesDict.get('name')):
		officials[officesDict.get('name')]=officesDict.get('officialIds',[])		

#Filters the name out of officials to make officials[name] 
electeds=[]
for electedID,electedDict in repDict['officials'].iteritems():
	for name, officialIDs in officials.iteritems():
		if electedID in officialIDs:
			singleElected=[]
			singleElected.append(name.encode('utf-8'))
			singleElected.append(electedDict.get('name',"").encode('utf-8'))
			singleElected.append(electedDict.get('photoUrl',"").encode('utf-8'))
			singleElected.append(electedDict.get('party',"").encode('utf-8'))
			singleElected.append(electedDict.get('phones',"")[0].encode('utf-8'))
			singleElected.append(electedDict.get('urls',"")[0].encode('utf-8'))
			for socialChannel in electedDict.get('channels',""):
				#print socialChannel
				for k,v in socialChannel.iteritems():
					if v=="Facebook":
						singleElected.append(socialChannel.get('id',"").encode('utf-8'))
				for k,v in socialChannel.iteritems():
					if v=="Twitter":
						singleElected.append(socialChannel.get('id',"").encode('utf-8'))
			print singleElected	




	
"""
# Create instance of FieldStorage 
form = cgi.FieldStorage() 

# Get data from fields
if form.getvalue('stateChoice'):
   stateChoice = form.getvalue('stateChoice')
else:
   stateChoice = "Not entered"


print "Content-type:text/html\r\n\r\n"
print "<html>"
print "<head>"
print "<title>State Dropdown Box</title>"
print "</head>"
print "<body>"
print "<h2> Selected State is %s</h2>" % stateChoice
print "</body>"
print "</html>"

stateChoice = "AL"



#downloads the object
stateDelegationURL = ('https://www.govtrack.us/api/v2/role?current=true&state='+stateChoice)
stateDelegation = json.load(urllib2.urlopen(stateDelegationURL))

stateDelegationInfo = []
for stateDelegationMember in stateDelegation['objects']:
	singleMemberInfo = []
	name = stateDelegationMember['person']['name'].encode("utf-8")
	phone = stateDelegationMember['phone']
	twitter = stateDelegationMember['person']['twitterid']
	website = stateDelegationMember['website']
	singleMemberInfo.extend([name, phone, twitter, website])
	stateDelegationInfo.append(singleMemberInfo)


htmlcode = HTML.table(stateDelegationInfo, header_row=['Name','Phone','Twitter','Website'])
print htmlcode

"""

