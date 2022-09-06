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
    settings = {
        "device_type": "cisco_ios",
        "host": "192.168.1.1",
        "username": "admin",
        "password": "password",
    }
    acl_name = "BLOCK_ADVERSARY"
    configure_acl_command_prefix = "ip access-list standard"
    block_command_prefix = "1 deny"
    def block_host(self, host):
        commands = [
            (self.configure_acl_command_prefix + " " + self.acl_name), 
            (self.block_command_prefix + " " + host)
        ]
        """
        with netmiko.ConnectHandler(**self.settings) as connection:
            connection.send_config_set(commands)
            message = "Blocking " + host + "\n"
        """
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

def start_listening_api(ip):
    address = (ip, 8666)
    handler = RequestHandler
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
    args = parser.parse_args()
    if args.update_soc:
        update_action_menu(args.ip_address)
        restart_security_onion_console()
    elif args.start:
        start_listening_api(args.ip_address)
    else:
        parser.print_help()
    return
  
if __name__ == "__main__":
    main()
