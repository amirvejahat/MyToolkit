from json import dumps, loads
from requests.sessions import Session
import sys
import requests

_session = None
base_url = "https://new.support.parspooyesh.com/jira/rest"
issue_url = "api/2/issue"
login_url = "auth/1/session"


projects = { 'ORGANIZATION1' : ['PROJECT1',281] , 'ORGANIZATION2' : ['PROJECT2',258] }


def _prepare_data(name,args,**kwargs):
    data = {
    "create": {
        "worklog": [
        {
            "add": {
            "timeSpent": "60m",
            "started": "2011-07-05T11:05:00.000+0000"
            }
        }
        ]
    },
    "fields": {
        "project": {
        "id": "10807"
        },
        "summary": kwargs["summary"],
        "issuetype": {
        "id": "10005"
        },
        "assignee": {
        "name": ""
        },
        "reporter": {
        "name": projects[name][0]
        },
        "labels": args,
        "description": kwargs["description"],
        "customfield_10002" : [projects[name][1]]
    }
    }
    return data

def _get_session():
    DEFAULT_HEADER = {
    "Content-type": "application/json",
    "Accept": "application/json",
    "Accept-Charset": "utf-8",
    "Cache-Control": "no-cache",
    }
    global _session
    if _session is None:
        _session = Session()
        _session.headers.update(DEFAULT_HEADER)
    return _session

def _login():
    auth = {}
    auth["username"] = "USERNAME"
    auth["password"] = "PASSWORD"
    url = "/".join((base_url,login_url))
    session = _get_session()
    resp = session.post(url=url,data=dumps(auth))
    return loads(resp.text)

def _logout():
   url = "/".join((base_url,login_url))
   resp = requests.delete(url)    
   return loads(resp.text)

def _create_issue(data):
    url = "/".join((base_url,issue_url))
    session = _get_session()
    resp = session.post(url=url,data=dumps(data))
    return loads(resp.text)

if __name__ == "__main__" :

    data = _prepare_data(sys.argv[1],sys.argv[4:],summary=sys.argv[2],description=sys.argv[3])
    _login())
    _create_issue(data)
    _logout()
