from bs4 import BeautifulSoup
import requests, urllib, os, json, argparse
import platform, datetime

op = ''
desc = "Articles scraper"

if(platform.system() == 'Windows'):
    os.system('cls')
if (platform.system() == 'Linux'):
    os.system('clear')

argp = argparse.ArgumentParser(usage = "scraper.py -t TYPE -q QUERY -c [COUNT]")
argp.add_argument("-t","--type",required= True)
argp.add_argument("-q","--query",required= True)
argp.add_argument("-c","--count")
argp.add_argument("-o","--output")
parser = argp.parse_args()
type = parser.type
query = parser.query
count = parser.count
output = parser.output
if(count == None): count = '10'

def do_hackerone():

    global query
    global op
    query_ql=r"""
    {"operationName":"HacktivityPageQuery","variables":{"querystring":"%s","where":{"report":{"disclosed_at":{"_is_null":false}}},"orderBy":{"field":"popular","direction":"DESC"},"secureOrderBy":null,"count":%s,"maxShownVoters":10,"cursor":"MTI1"},"query":"query HacktivityPageQuery($querystring: String, $orderBy: HacktivityItemOrderInput, $secureOrderBy: FiltersHacktivityItemFilterOrder, $where: FiltersHacktivityItemFilterInput, $count: Int, $cursor: String, $maxShownVoters: Int) {\n  me {\n    id\n    __typename\n  }\n  hacktivity_items(first: $count, after: $cursor, query: $querystring, order_by: $orderBy, secure_order_by: $secureOrderBy, where: $where) {\n    total_count\n    ...HacktivityList\n    __typename\n  }\n}\n\nfragment HacktivityList on HacktivityItemConnection {\n  total_count\n  pageInfo {\n    endCursor\n    hasNextPage\n    __typename\n  }\n  edges {\n    node {\n      ... on HacktivityItemInterface {\n        id\n        databaseId: _id\n        ...HacktivityItem\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment HacktivityItem on HacktivityItemUnion {\n  type: __typename\n  ... on HacktivityItemInterface {\n    id\n    votes {\n      total_count\n      __typename\n    }\n    voters: votes(last: $maxShownVoters) {\n      edges {\n        node {\n          id\n          user {\n            id\n            username\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    upvoted: upvoted_by_current_user\n    __typename\n  }\n  ... on Undisclosed {\n    id\n    ...HacktivityItemUndisclosed\n    __typename\n  }\n  ... on Disclosed {\n    id\n    ...HacktivityItemDisclosed\n    __typename\n  }\n  ... on HackerPublished {\n    id\n    ...HacktivityItemHackerPublished\n    __typename\n  }\n}\n\nfragment HacktivityItemUndisclosed on Undisclosed {\n  id\n  reporter {\n    id\n    username\n    ...UserLinkWithMiniProfile\n    __typename\n  }\n  team {\n    handle\n    name\n    medium_profile_picture: profile_picture(size: medium)\n    url\n    id\n    ...TeamLinkWithMiniProfile\n    __typename\n  }\n  latest_disclosable_action\n  latest_disclosable_activity_at\n  requires_view_privilege\n  total_awarded_amount\n  currency\n  __typename\n}\n\nfragment TeamLinkWithMiniProfile on Team {\n  id\n  handle\n  name\n  __typename\n}\n\nfragment UserLinkWithMiniProfile on User {\n  id\n  username\n  __typename\n}\n\nfragment HacktivityItemDisclosed on Disclosed {\n  id\n  reporter {\n    id\n    username\n    ...UserLinkWithMiniProfile\n    __typename\n  }\n  team {\n    handle\n    name\n    medium_profile_picture: profile_picture(size: medium)\n    url\n    id\n    ...TeamLinkWithMiniProfile\n    __typename\n  }\n  report {\n    id\n    title\n    substate\n    url\n    __typename\n  }\n  latest_disclosable_action\n  latest_disclosable_activity_at\n  total_awarded_amount\n  severity_rating\n  currency\n  __typename\n}\n\nfragment HacktivityItemHackerPublished on HackerPublished {\n  id\n  reporter {\n    id\n    username\n    ...UserLinkWithMiniProfile\n    __typename\n  }\n  team {\n    id\n    handle\n    name\n    medium_profile_picture: profile_picture(size: medium)\n    url\n    ...TeamLinkWithMiniProfile\n    __typename\n  }\n  report {\n    id\n    url\n    title\n    substate\n    __typename\n  }\n  latest_disclosable_activity_at\n  severity_rating\n  __typename\n}\n"}
    """ % (query, int(count))
    #print(query)

    print("[+] Finding atmost %s public reports on Hackerone..." %count)
    headers = {"content-type": "application/json"}

    try:
        request = requests.post('https://hackerone.com/graphql', data=query_ql, headers=headers)
    except requests.ConnectionError:
        print("[-] Can't connect to the server. Are you connected to the internet?")
        exit()

    if request.status_code == 200:

        json_response = json.loads(json.dumps(request.json()))

        if not len(json_response['data']['hacktivity_items']['edges']):
            print("[-] No data retrieved.")
            exit()

        print("[+] Listing reports...")
        
        for i in range(len(json_response['data']['hacktivity_items']['edges'])):
            try:
                op +=  "-"*70 + "\n" + json_response['data']['hacktivity_items']['edges'][i]['node']['report']['title'] +": " + json_response['data']['hacktivity_items']['edges'][i]['node']['report']['url'] + "\n"
            except:
                pass
        print(op)
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, request.headers))

