#!/usr/bin/python

# Import modules for CGI handling 
import cgi, cgitb 
import urllib2
import json
import os
import HTML

# Create instance of FieldStorage 
form = cgi.FieldStorage() 

# Get data from fields
if form.getvalue('stateChoice'):
   stateChoice = form.getvalue('stateChoice')
else:
   stateChoice = "Not entered"

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

print "Content-type:text/html\r\n\r\n"
print "<html>"
print "<head>"
print "<title>Dropdown Box - Sixth CGI Program</title>"
print "</head>"
print "<body>"
print htmlcode
print "</body>"
print "</html>"
