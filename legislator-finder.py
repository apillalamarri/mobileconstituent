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
stateDelURL = ('https://www.govtrack.us/api/v2/role?current=true&state='+stateChoice)
stateDel = json.load(urllib2.urlopen(stateDelURL))

#Create a list to store the name, party, phone, twitter, and website info for all members of the state's Congressional delegation
stateDelInfo = []

#For each member, add that member's info to stateDelInfo
for stateDelMember in stateDel['objects']:
	#Start with a blank list for the current member
	singleMemberInfo = []
	
	#Concatenate title, firstname, land lastname to form name
	title=stateDelMember['title']
	firstName=stateDelMember['person']['firstname']
	lastName=stateDelMember['person']['lastname']
	name=title+" "+firstName+" "+lastName
	
	#Convert the long party name to a party code (R, D, or I)
	partyLong = stateDelMember['party']
	if partyLong == 'Republican':
		party = 'R'
	elif partyLong == 'Democrat':
		party = 'D'
	elif partyLong == 'Independent':
		party = 'I'
	else:
		party = ''
	#Form a tel: link from the phone number
	try:
		phoneNumber = stateDelMember['phone']
		phone='<a href="tel:'+phoneNumber+'">'+phoneNumber+'</a>'
	except:
		phone = ""
	#Form a twitter URL from the twitter ID
	try:
		twitterHandle = stateDelMember['person']['twitterid']
		twitter='<a href="http://www.twitter.com/'+twitterHandle+'">'+twitterHandle+'</a>'
	except:
		twitter=""
	#Form a full website URL from the website
	websiteURL = stateDelMember['website']
	website='<a href="'+websiteURL+'">'+websiteURL+'</a>'
	
	#Form a list containing name, party, phone, twitter, and website 
	singleMemberInfo.extend([name, party, phone, twitter, website])
	
	#Add that list to stateDelInfo, our list of lists
	stateDelInfo.append(singleMemberInfo)

#HTML.table adds html to make a table out of a list of lists.
htmlcode = HTML.table(stateDelInfo, header_row=['Name','Party','Phone','Twitter','Website'])

#Add HTML to make a proper page
print "Content-type:text/html\r\n\r\n"
print "<html>"
print "<head>"
print "<title>Mobile Constituent</title>"
print "</head>"
print "<body>"
print htmlcode
print "</body>"

