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

class Event():
    date = ""
    description = ""
    distribution = {
        "your_organisation_only": 0,
	"this_community_only": 1,
	"connected_communities": 2,
	"all_communities": 3,
	"sharing_group": 4,
	"inherit": 5
    }
    threat_level = {
        "high": 1,
	"medium": 2,
	"low": 3,
	"undefined": 4
    }
    analysis = {
        "initial": 0,
	"ongoing": 1,
        "completed": 2
    }

class Attribute():
    type = ""
    category = ""
    value = ""
    distribution = {
        "your_organisation_only": 0,
	"this_community_only": 1,
	"connected_communities": 2,
	"all_communities": 3,
	"sharing_group": 4,
	"inherit": 5
    }
    for_ids = "false"
    contextual_comment = ""

def get_cases(elastic_server_ip, elastic_server_port, elastic_api_key):
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
                #pprint(foo)
    return

def add_event(misp_server_ip, misp_api_key, event):
    event = Event()
    url = "https://" + misp_server_ip + "/events"
    headers = {
        "Accept": "application/json",
	"content-type": "application/json",
	"Authorization": misp_api_key
    }
    response = requests.post(url, headers = headers, json = event, verify = False)
    print(response.text)
    return

def add_attribute():
    return

def main():
    requests.packages.urllib3.disable_warnings()
    parser = argparse.ArgumentParser()
    parser.add_argument("--get-cases", action="store_true", help = "Get events from Elasticsearch")
    parser.add_argument("--add-event", action="store_true", help = "Send an event to MISP")
    args = parser.parse_args()
    if args.get_cases:
        get_cases(elastic_server_ip, elastic_server_port, elastic_api_key)
    elif args.add_event:
        add_event(misp_server_ip, misp_api_key)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
