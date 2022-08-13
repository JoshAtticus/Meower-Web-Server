import random
from flask import Flask, request
from urllib.request import urlopen,Request
import re
import hashlib

"""
    todo:
        None

    later/might need help:
        add auto 4 hourly reindexing
        optimizations
        add json to db for from site
        index sitemap/robots.txt parser
        disc
        meower member info card
"""

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0"
}

from pymongo import MongoClient

mongo_ip = "mongodb://localhost:27017"
db = MongoClient(mongo_ip)["indexedfiles"]

for item in ["html"]:
    if not item in db.list_collection_names():
        print("Creating collection {0}".format(item))
        db.create_collection(name=item)

db["html"].create_index("html")

app = Flask(__name__)

@app.route("/api/mod/logs")
def getlogs():
    return request.headers.values

"""

@app.route("/api/mod/runindex/<site>/<time>")
def indexsite(site,time):
    return "index site"

@app.route("/api/mod/dropindexes")
def dropindexes():
    return "remove all indexes"

@app.route("/api/mod/blocksite/<site>")
def blocksite():
    return "block site and remove from mongo"

@app.route("/api/mod/addsearchres/<search>")
headers: res
def addsearchres(search):
    return "easter egg type stuff
"""

@app.route("/api/regenmodkey")
def regenkey():
    number = str(random.randint(10000000, 99999999)).encode()
    hashed_l1 = hashlib.md5(number).hexdigest().encode()
    hashed = hashlib.sha1(hashed_l1).hexdigest()
    return hashed

@app.route("/api/search/checkreindex/<site>")
def needsreindex(site):
    req = Request(site, headers=headers)
    data = urlopen(req).read().decode()# send the request and save the response

    a = db["html"].find({})

    needsreindex = False

    for doc in a:
        if data.lower() == doc["html"].lower():
            needsreindex = True
        break

    return needsreindex

@app.route("/api/search/getresults/<query>")
def getsearch(query):
    qlower = query.lower()
    a = db["html"].find({})

    queries = {
        
    }

    for doc in a:
        if qlower in doc["html"].lower():
            needsreindex = False

            title = ""
            i = 1

            for m in re.finditer("title", doc["html"]):
                while True:
                    if doc["html"][m.end() + i] == '<':
                        break
                    title = title + doc["html"][m.end() + i]
                    i += 1
                break

            queries.update({doc["_id"]: [title,"Currently Cannot Fetch a Discription"]})

    if len(queries) == 0:
        queries = "No Search Results"
    
    if query.lower() == "meowy":
        queries = "meowies_fall"
    return queries

@app.route("/")
def root():
    return "<body><script>location.replace('./api/')</script></body>"

#/api/mod/runindex/<site>/<time>, Returns Error or string, Headers: modkey
#/api/mod/logs
#/api/mod/blocksite/<site>
#/api/regenmodkey

#later:
#/api/mod/addcard/<search>/<cardtitle>/<cardesc>, headers: res: JSON
#/api/mod/dropindexes, Returns StatusCode (not added)

@app.route("/api/")
def apidoc():
    return """<pre>
    The Api Seems to be up!
        The endpoints are:
            /api/getresults/<query>/<getindexedhtml>, Returns JSON
            /api/status, Returns JSON
            /api/getheaders/<site>, Returns JSON
    </pre>"""