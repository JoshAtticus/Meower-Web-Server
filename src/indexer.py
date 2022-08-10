from urllib.request import urlopen,Request
import re
from xml.dom.expatbuilder import theDOMImplementation

from pymongo import MongoClient

import threading

mongo_ip = "mongodb://localhost:27017"
db = MongoClient(mongo_ip)["indexedfiles"]

pastlinks = []
blockedchars = [
    "<",
    "{",
    "}",
    #filetypes
    ".css",
    ".js",
    ".png"
]

blocked = ["https://facebook.com/creativecommons"]

def jumptopage(data_page):
    global pastlinks

    for m in re.finditer('https', data_page.lower()):
        print('https found', m.start(), m.end())
        sitelink = "https"
        i = 0
        while True:
            if data_page[m.end() + i] == '"':
                break
            sitelink = sitelink + data_page[m.end() + i]
            i += 1
        # and not "<" in sitelink and not "}" in sitelink and not ".js" in sitelink and not ".css" in sitelink
        if not db["html"].find_one({"_id": sitelink}) and not sitelink in blocked and not any(ext in sitelink for ext in blockedchars):
            print(sitelink)
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0"
            }

            req = Request(sitelink + "/", headers=headers)
            data = urlopen(req).read().decode()# send the request and save the response
            pastlinks.append(sitelink)
            db["html"].insert_one({"_id":sitelink,"html":data})
            try:
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0"
                }

                req = Request(sitelink + "/", headers=headers)
                data = urlopen(req).read().decode()# send the request and save the response
                jumptopage(data)
            except:
                print("error while indexing "+sitelink)

initalurl = "https://meower.org/"

headers = {
    "User-Agent": ""
}

req = Request(initalurl, headers=headers)
data = urlopen(req).read().decode()# send the request and save the response

print(data)

jumptopage(data)

