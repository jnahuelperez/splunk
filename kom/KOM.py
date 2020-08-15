import sys
import requests
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

splunk_user = sys.argv[1]
splunk_pwd = sys.argv[2]
splunk_environment = sys.argv[3]
splunk_dst_user = sys.argv[4]
splunk_new_owner= splunk_dst_user+"@appdirect.com"
Splunk_URL = 'https://'+splunk_environment+':8089/'
Splunk_Objs = []

def GetSplunkAPIData(pObj,pSplunk_Search,pTarget_user,pInitial_request):
    mParams = {
    'output_mode': 'json',
    'count':'0'
    }
    response = requests.get(Splunk_URL+pSplunk_Search, auth=(splunk_user, splunk_pwd),verify=False,params=mParams)
    i=0
    for item in response.json()['entry']:
        if(pInitial_request):
            if item['acl']['owner'] == pTarget_user:
                print(item['acl']['owner']+"\t"+item['id'])
                Splunk_Objs.append(item['id'])
                i+=1
            else:
                pass
        else:
            if item['acl']['owner'] == splunk_new_owner:
                print(item['acl']['owner']+"\t"+item['id'])
    return i

def GetInfo(pCondition):
    i=0
    i += GetSplunkAPIData('views','servicesNS/-/-/data/ui/views',splunk_dst_user,pCondition) # Get Views
    i += GetSplunkAPIData('searches','servicesNS/-/-/saved/searches',splunk_dst_user,pCondition) # Get searches
    i += GetSplunkAPIData('eventtypes','servicesNS/-/-/saved/eventtypes',splunk_dst_user,pCondition) # Get eventtypes
    i += GetSplunkAPIData('lookup-table-files','servicesNS/-/-/data/lookup-table-files',splunk_dst_user,pCondition) # Get lookup-table-files'
    i += GetSplunkAPIData('panels','servicesNS/-/-/data/ui/panels',splunk_dst_user,pCondition) # Get panels
    return i

def ChangeOwnership(pNewOwner):
    mParams = {
    'owner':pNewOwner,
    'sharing':'global'
    }
    i=0
    for item in Splunk_Objs:
        print(item)
        response = requests.post(item+"/acl", auth=(splunk_user, splunk_pwd),verify=False,params=mParams)
        i+=1
    print("\n"+str(i)+" KO changed")
    print("Checking ownership change...\n")
    GetInfo(False)

print("Getting knowledge objects...")
if GetInfo(True) > 0:
    print("\nAsigning ownershipt to:\t"+splunk_new_owner)
    ChangeOwnership(splunk_new_owner)
else:
    print("\nNo objects found for the given user\n")
