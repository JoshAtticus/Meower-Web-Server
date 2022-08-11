from flask import Flask
import os

"""
    todo:
        when released to github:
            add reindexing
            optimizations
"""

from pymongo import MongoClient

mongo_ip = "mongodb://localhost:27017"
db = MongoClient(mongo_ip)["indexedfiles"]

for item in ["html"]:
    if not item in db.list_collection_names():
        print("Creating collection {0}".format(item))
        db.create_collection(name=item)

db["html"].create_index("html")

app = Flask(__name__)

@app.route("/api/mod/runindexer")
def runindexer():
    return "a"

"""
@app.route("/api/mod/reindex/<site>")
def reindexsite():
    return "remove from mongo and re-fetch all indexes from that

@app.route("/api/mod/dropindexes")
def dropindexes():
    return "remove all indexes"
"""

@app.route("/api/getresults/<query>")
def getsearch(query):
    print(db["html"].find({"html":"meower"}))
    return "a"

@app.route("/api/getheaders/<site>/")
def getheaders(site):
    return "headers query" + site

@app.route("/")
def root():
    return "<body><script>location.replace('./api/')</script></body>"

#/api/mod/dropindexes, Returns StatusCode (not added)

@app.route("/api/")
def apidoc():
    return """<pre>
    The Api Seems to be up!
        The endpoints are:
            /api/getresults/<query>, Returns JSON
            /api/status, Returns JSON
            /api/mod/runindexer, Returns Error or string, Headers: modkey, baseurl and time
            /api/getheaders/<site>, Returns JSON
    </pre>"""