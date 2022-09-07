#!/usr/bin/env python3

import argparse
import http.server
import ipaddress
import json
import netmiko
import os
import ssl
import subprocess

class RequestHandler(http.server.BaseHTTPRequestHandler):
    settings = {"device_type": None, "host": None, "username": None, "password": None}
    acl_name = None
    acl_command_prefix = None
    block_command_prefix = None
    audit_only = False
    def block_host(self, host):
        commands = [
            (self.acl_command_prefix + " " + self.acl_name), 
            (self.block_command_prefix + " " + host)
        ]
        if self.audit_only == True:
            return "Blocking " + host + "\n"
        else:
            with netmiko.ConnectHandler(**self.settings) as connection:
                connection.send_config_set(commands)
                message = "Blocking " + host + "\n"
            return "Blocking " + host + "\n" 
    def do_GET(self):
        self.send_error(405)
    def do_POST(self):
        if self.path.startswith("/block/"):
            host = self.path.split("/block/")[1]
            try:
                ipaddress.ip_address(host)
                self.send_response(200)
                self.send_header("Content-Type", "text/html")
                self.end_headers()
                message = self.block_host(host)
                self.wfile.write(message.encode("UTF-8"))
            except ValueError:
                self.send_error(400)
        else:
            self.send_error(404)

def start_listening_api(ip, device_type, host, username, password, acl_name, acl_command_prefix, block_command_prefix, audit_only):
    address = (ip, 8666)
    handler = RequestHandler
    handler.settings["device_type"] = device_type
    handler.settings["host"] = host
    handler.settings["username"] = username
    handler.settings["password"] = password
    handler.acl_name = acl_name
    handler.acl_command_prefix = acl_command_prefix
    handler.block_command_prefix = block_command_prefix
    handler.audit_only = audit_only
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile = "public.key", keyfile = "private.key")
    api = http.server.HTTPServer(address, handler)
    api.socket = context.wrap_socket(api.socket, server_side = True)
    api.serve_forever()
    return

def update_action_menu(ip):
    default_action_menu = "/opt/so/saltstack/default/salt/soc/files/soc/menu.actions.json"
    local_action_menu = "/opt/so/saltstack/local/salt/soc/files/soc/menu.actions.json"
    link = "https://%s:8666/block/{value}" % (ip)
    action = {
        "name": "Block",
        "description": "Block at network perimeter",
        "icon": "fas fa-shield-alt",
        "target": "_blank",
        "links": [ link ],
        "background": True,
        "method": "POST"
    }
    so2ban = " ," + json.dumps(action) + "\n"
    if os.path.exists(local_action_menu):
        action_menu = local_action_menu
    else:
        action_menu = default_action_menu
    with open(action_menu) as old_action_menu:
        update = old_action_menu.readlines()
        second_to_last_line = len(update) - 1
        update.insert(second_to_last_line, so2ban)
        with open(local_action_menu, 'w') as new_action_menu:
            for entry in update:
                new_action_menu.write(entry)
    print("Done!")
    return

def restart_security_onion_console():
    print("Restarting the Security Onion Console...")
    subprocess.run("so-soc-restart", stdout = subprocess.PIPE, check = True)
    print("Done!")
    return

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--update-soc", action = "store_true", help = "Add so2ban to the Security Onion Console (SOC) action menu")
    parser.add_argument("--start", action = "store_true", help = "Start so2ban")
    parser.add_argument("--ip-address", help = "IP address for so2ban API to listen on")
    parser.add_argument("--device-type", help = "Network boundary device type (e.g., cisco_ios, paloalto_panos)")
    parser.add_argument("--host", help = "Network boundary device hostname or IP address")
    parser.add_argument("--username", help = "Network boundary device username")
    parser.add_argument("--password", help = "Network bonudary device password")
    parser.add_argument("--acl-name", help = "Network boundary Access Control List (ACL) (e.g., 'BLOCK_ADVERSARY'")
    parser.add_argument("--acl-command-prefix", help = "Network boundary ACL command prefix (e.g., 'ip access-list standard')")
    parser.add_argument("--block-command-prefix", help = "Network boundary block command prefix (e.g., '1 deny'")
    parser.add_argument("--audit-only", action = "store_true", help = "Audit only, do not block (use for troubleshooting)")
    args = parser.parse_args()
    if args.update_soc:
        update_action_menu(args.ip_address)
        restart_security_onion_console()
    elif args.start:
        start_listening_api(
            args.ip_address, 
            args.device_type, 
            args.host, 
            args.username, 
            args.password,
            args.acl_name,
            args.acl_command_prefix,
            args.block_command_prefix,
            args.audit_only
        )
    else:
        parser.print_help()
    return
  
if __name__ == "__main__":
    main()
