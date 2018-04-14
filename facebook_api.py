import facebook
import urllib2
import json

#{"access_token":"1207531382703068|ba4Gf8LTaSGKgrLLOZFHVRHJ69I","token_type":"bearer"}
#To generate ACCESS_TOKEN on Facebook, acess the link: https://graph.facebook.com/oauth/access_token?%20client_id=1207531382703068%20&client_secret=d7da00d55d97572f7adfc5f474e1623a&grant_type=client_credentials
ACCESS_TOKEN = "1207531382703068|ba4Gf8LTaSGKgrLLOZFHVRHJ69I"


def get_page_data(page_id,access_token):
    api_endpoint = "https://graph.facebook.com/v2.4/"
    fb_graph_url = api_endpoint+page_id+"?fields=id,name,likes,link&access_token="+ACCESS_TOKEN
    try:
        api_request = urllib2.Request(fb_graph_url)
        api_response = urllib2.urlopen(api_request)
        
        try:
            return json.loads(api_response.read())
        except (ValueError, KeyError, TypeError):
            return "JSON error"

    except IOError, e:
        if hasattr(e, 'code'):
            return e.code
        elif hasattr(e, 'reason'):
            return e.reason

page_id = "1071153679650340" # username or id

page_data = get_page_data(page_id,ACCESS_TOKEN)

print "Page Name:"+ page_data['name']
print "Likes:"+ str(page_data)
print "Link:"+ page_data['link']