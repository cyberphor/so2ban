#!/usr/bin/python3

import glob
import json
import os

def check_if_sudo():
    if not 'SUDO_UID' in os.environ.keys():
        print('[x] This script requires super-user privileges (sudo).')
        exit()

def ingest_crowdstrike():
    files = glob.glob('*_indicators_*.json')
    updates = 0
    for cs_file in files:
        print('[+] Ingesting ' + cs_file)
        if get_iocs(cs_file) > 0:
            updates = updates + 1
    if updates > 0:   
        os.system('sudo so-zeek-restart')

def get_iocs(cs_file):
    json_filepath = './' + cs_file
    json_file = open(json_filepath,)
    json_data = json.load(json_file)
    json_file.close()

    label = {
        'ip_address':'Intel::ADDR',
        'ip_address_block':'Intel::SUBNET',
        'email_address':'Intel::EMAIL',
        'url':'Intel::URL',
        'domain':'Intel::DOMAIN',
        'hash_md5':'Intel::FILE_HASH',
        'hash_sha1':'Intel::FILE_HASH',
        'hash_sha256':'Intel::FILE_HASH',
        'file_name':'Intel::FILE_NAME'
     }
 
    dict_of_iocs = {}
    for line in json_data:
        ioc = line['value']
        ioc_type = label.get(line['type_name'], 'Intel::SOFTWARE')
        for actor in line['actors']:
            if 'slug' in actor:
                ioc_source = 'crowdstrike_' + actor['slug']
        attributes = ioc, ioc_type, ioc_source, "T"
        dict_of_iocs[ioc] = '\t'.join(attributes)
    return tell_bro(dict_of_iocs)

def tell_bro(dict_of_iocs):
    intel_path = '/opt/zeek/share/bro/intel/intel.dat'
    intel_file = open(intel_path, 'a')
    current_intel = open(intel_path).read()
    updates = 0
    for ioc in dict_of_iocs:
        if ioc not in current_intel:
            intel_file.write(dict_of_iocs[ioc] + '\n')
            updates = updates + 1
    print(" -  Added %d IOCs to Bro/Zeek." % updates)
    intel_file.close()
    return updates

check_if_sudo()
ingest_crowdstrike()
