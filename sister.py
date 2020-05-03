#!/usr/bin/python3

import json

def get_intel():
    global intel

    json_filepath = './intel.json'
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
 
    intel = []
    for line in json_data:
        ioc_value = line['value']
        ioc_type = label.get(line['type_name'], 'Intel::SOFTWARE')
        for actor in line['actors']:
            if 'slug' in actor:
                slug = (actor['slug'])
        phase = line['kill_chains'][0]
        malware = line['malware_families'][0]
        ioc_source = slug + '_' + phase + '_' + malware
        ioc_entry = ioc_value, ioc_type, ioc_source, "T"
        intel.append('\t'.join(ioc_entry))

def tell_bro():
    intel_path = '/opt/zeek/share/bro/intel/intel.dat'
    intel_file = open(intel_path, 'a')
    for ioc in intel:
        intel_file.write(ioc + '\n')
    intel_file.close()

get_intel()
tell_bro()
# restart_bro()
