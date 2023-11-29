import json
# Open Static URL config file and convert it from json to a python dictionary (Store in memory)
def load_url_config():
    urls={}
    with open("url-config.json") as url_config_file:
        urls = json.load(url_config_file)
    return urls

def get_url(service, urls):
    url = -1
    if service in urls:
        url = urls[service]
        # if service == "state-save":
        #     url = url['url']
    return url
def get_saver_url(option, url):
    return  url['url'] + url[option]