#!/usr/bin/python
import xmlrpclib
import json
import sys

if len(sys.argv) != 2:
  print "Usage: " + sys.argv[0] + "[--host | --list]"
  exit(1)

if sys.argv[1] == "--host":
  print "{}"

if sys.argv[1] == "--list":
  SATELLITE_URL = "http://spacewalk.hearn.local/rpc/api"
  SATELLITE_LOGIN = "admin"
  SATELLITE_PASSWORD = "shitcockhorsebacon"

  client = xmlrpclib.Server(SATELLITE_URL, verbose=0)
  
  key = client.auth.login(SATELLITE_LOGIN, SATELLITE_PASSWORD)
  grouplist = client.systemgroup.listAllGroups(key)

  print "{"
  print " \"_meta\": {"
  print "         \"hostvars\": {}"
  print " }"

  for group in grouplist:
    groupname=group.get('name')
    print "       \"" + groupname + "\": {"
    #print "[" + groupname.lower() + "]"
    systemlist = client.systemgroup.listSystems(key, groupname)
    print "               \"hosts\":"
    systemnames=[]
    for system in systemlist:
      systemnames.append(system.get('profile_name'))
      #print system.get('profile_name')
    print json.dumps(systemnames)
    print "       },"

  print " \"Ungrouped\": {"
  systemlist = client.system.listUngroupedSystems(key)
  systemnames=[]
  for system in systemlist:
    systemnames.append(system.get('name'))

  print json.dumps(systemnames)
  print " }"
  
  print "}"
  client.auth.logout(key)
