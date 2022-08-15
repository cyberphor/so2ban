#!/usr/bin/env python3

import argparse
import json
import requests
from pprint import pprint

elastic_server_ip = ""
elastic_server_port = ""
elastic_api_key = ""
misp_server_ip = ""
misp_api_key = ""

def get_events(elastic_server_ip, elastic_server_port, elastic_api_key):
    elastic_server = elastic_server_ip + ":" + elastic_server_port
    authorization = "ApiKey " + elastic_api_key
    url = "https://" + elastic_server + "/so-case/_search?pretty"
    headers = {
        "Content-Type": "application/json;charset=UTF-8",
        "Authorization": authorization
    }
    response = requests.get(url, headers = headers, verify = False)
    events = json.loads(response.text)["hits"]["hits"]
    cases = []
    related = []
    for event in events:
        kind = event["_source"]["so_kind"]
        if kind == "case":
            cases.append(event)
        elif kind == "related":
            related.append(event)
    for event in related:
        update = event["_source"]["so_related"]
        for case in cases:
            if update["caseId"] == case["_id"]:
                foo = {
                    "id": case["_id"],
                }
                for detail in case["_source"]["so_case"]:
                    foo[detail] = case["_source"]["so_case"][detail]
                for field in update["fields"]:
                    foo[field] = update["fields"][field]
                pprint(foo)
    return

def send_event(misp_server_ip, misp_api_key, event):
    event = {
        "Event":{
            "date":"2020-08-14",
            "distribution":3,    # all communities
            "threat_level_id":1, # general
            "analysis":1,        # ongoing
            "info":"Demo",
            "Attribute": [
                {
                    "type":"domain",
                    "category":"Network activity",
                    "value":"https://cyberphor.com",
                    "distribution":3,
                    "to_ids":"false",
                    "comment":"Known bad domain"
	        }
	    ]
	}
    }
    url = "https://" + misp_server_ip + "/events"
    headers = {
        "Accept": "application/json",
	"content-type": "application/json",
	"Authorization": misp_api_key
    }
    response = requests.post(url, headers = headers, json = event, verify = False)
    print(response.text)
    return

def main():
    requests.packages.urllib3.disable_warnings()
    parser = argparse.ArgumentParser()
    parser.add_argument("--get-events", action="store_true", help = "Get events from Elasticsearch")
    parser.add_argument("--send-event", action="store_true", help = "Send an event to MISP")
    args = parser.parse_args()
    if args.get_events:
        get_events(elastic_server_ip, elastic_server_port, elastic_api_key)
    elif args.send_event:
        send_event(misp_server_ip, misp_api_key)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
