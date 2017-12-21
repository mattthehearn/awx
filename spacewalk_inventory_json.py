#!/usr/bin/python
import xmlrpclib
import json

SATELLITE_URL = "http://spacewalk.hearn.local/rpc/api"
SATELLITE_LOGIN = "admin"
SATELLITE_PASSWORD = "shitcockhorsebacon"

client = xmlrpclib.Server(SATELLITE_URL, verbose=0)

key = client.auth.login(SATELLITE_LOGIN, SATELLITE_PASSWORD)
grouplist = client.systemgroup.listAllGroups(key)

print "{"
print "	\"_meta\": {"
print "		\"hostvars\": {}"
print "	}"

for group in grouplist:  #[:-1]:
  groupname=group.get('name')
  print "	\"" + groupname + "\": {"
  #print "[" + groupname.lower() + "]"
  systemlist = client.systemgroup.listSystems(key, groupname)
  print "		\"hosts\":"
  systemnames=[]
  for system in systemlist:
    systemnames.append(system.get('profile_name'))
    #print system.get('profile_name')
  print json.dumps(systemnames)
  print "	},"

#group=grouplist[-1]
#groupname=group.get('name')
#print "	\"" + groupname + "\": {"
##print "[" + groupname.lower() + "]"
#print "		\"hosts\":"
#systemlist = client.systemgroup.listSystems(key, groupname)
#systemnames=[]
#for system in systemlist:
  #systemnames.append(system.get('profile_name'))
  #print system.get('profile_name')

print "	\"Ungrouped\": {"
systemlist = client.system.listUngroupedSystems(key)
systemnames=[]
for system in systemlist:
  systemnames.append(system.get('name'))

print json.dumps(systemnames)
print "	}"

print "}"
client.auth.logout(key)
