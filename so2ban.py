sr/bin/env python3

import argparse
import http.server
import ipaddress
import json
#import netmiko
import os
import shutil
import ssl
import subprocess

class RequestHandler(object):
    def __init__(self, address, http.server.BaseHTTPRequestHandler):
        self.gatekeeper = self.Gateway()
    class Gateway:
        def __init__(self):
            self.settings = {
                "gatekeeper_type": "",
                "host": "",
                "username": "",
                "password": "",
            }
            self.acl = ""
            self.configure_acl_command_prefix = ""
            self.block_command_prefix = ""
            self.unblock_command_prefix = ""
        def block_host(self, host):
            commands = [
                " ".join(self.configure_acl_command_prefix, self.acl), 
                " ".join(self.block_command_prefix, host)
            ]
            #with netmiko.ConnectHandler(**self.settings) as connection:
            #    connection.send_config_set(commands)
            #    message = "Blocking " + host + "\n"
            #return message
        def unblock_host(self, host):
            commands = [
                " ".join(self.configure_acl_command_prefix, self.acl),
                " ".join(self.unblock_command_prefix, host)
            ]
            #with netmiko.ConnectHandler(**self.settings) as connection:
            #    connection.send_config_set(commands)
            #    message = "Unblocking " + host + "\n"
            #return message
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
                #message = self.gatekeeper.block_host(host)
                self.wfile.write(message.encode("UTF-8"))
            except ValueError:
                self.send_error(400)
        elif self.path.startswith("/unblock/"):
            host = self.path.split("/unblock/")[1]
            try:
                ipaddress.ip_address(host)
                self.send_response(200)
                self.send_header("Content-Type", "text/html")
                self.end_headers()
                #message = self.gatekeeper.unblock_host(host)
                self.wfile.write(message.encode("UTF-8"))
            except ValueError:
                self.send_error(400)
        else:
            self.send_error(404)

def start_listening_api():
    address = ("127.0.0.1", 8666)
    handler = RequestHandler
    handler.gatekeeper.settings["device_type"] = "cisco_ios"
    handler.gatekeeper.settings["host"] = "192.168.1.1"
    handler.gatekeeper.settings["username"] = "admin"
    handler.gatekeeper.settings["password"] = "password"
    handler.gatekeeper.acl_name = "BLOCK_ADVERSARY"
    handler.gatekeeper.acl_command_prefix = "ip access-list standard"
    handler.gatekeeper.ace_command_prefix = "1 deny"
    api = http.server.HTTPServer(address, handler)
    api.socket = ssl.wrap_socket(
        api.socket,
        server_side = True,
        keyfile = "private.key",
        certfile = "public.key",
        ssl_version = ssl.PROTOCOL_TLS
    )
    api.serve_forever()
    return

def update_action_menu():
    default_action_menu = "/opt/so/saltstack/default/salt/soc/files/soc/menu.actions.json"
    local_action_menu = "/opt/so/saltstack/local/salt/soc/files/soc/menu.actions.json"
    link = "https://127.0.0.1:8666/block/{value}"
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
    args = parser.parse_args()
    if args.update_soc:
        update_action_menu()
        restart_security_onion_console()
    elif args.start:
        start_listening_api()
    else:
        parser.print_help()
    return
  
if __name__ == "__main__":
    main()
