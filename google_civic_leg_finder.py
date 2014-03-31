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
key = ""
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
	governorList = ["Governor"]
	stateLegList = ["State House", "State Senate"]
	allNames = {}
	allNames = {"potus":potusList,
				"congress":congressList,
				"governor":governorList,
				"stateLeg":stateLegList}
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
				singleElected.append(electedDict.get('phones',"")[0].encode('utf-8'))
				singleElected.append(electedDict.get('urls',"")[0].encode('utf-8'))		
				singleElected.append(getSocialID(electedDict.get("channels",[]),"Facebook"))
				singleElected.append(getSocialID(electedDict.get("channels",[]),"Twitter"))
				electeds.append(singleElected)
	return electeds
	
################################################################

#Filters the office id out of offices and gets offices[officialIds] 
officials= {}
for officesID,officesDict in repDict['offices'].iteritems():

	if checkName(officesDict.get('name'),"stateLeg"):
		officials[officesDict.get('name')]=officesDict.get('officialIds',[])		

#print deets(officials, repDict)
htmlcode = HTML.table(deets(officials, repDict), header_row=['Office','Name','Photo','Party','Phone','Website','Facebook','Twitter'])
print htmlcode



	
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

