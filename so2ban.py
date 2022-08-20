#!/usr/bin/env python3

import argparse
import http.server
import ipaddress
import netmiko
import shutil
import subprocess

ip = "127.0.0.1"
port = 666
server_address = (ip, port)
router = {
    "device_type": "cisco_ios",
    "host": "192.168.1.1",
    "username": "admin",
    "password": "password",
}
acl_name = "BLOCK_ADVERSARY"
acl = "ip access-list standard " + acl_name
ace = "1 deny "

class RequestHandler(http.server.BaseHTTPRequestHandler):
    def block(self, acl_name, adversary):
        commands = [acl, (ace + adversary)]
        with netmiko.ConnectHandler(**router) as net_connect:
            net_connect.send_config_set(commands)
        message = "Blocking " + adversary + "\n"
        self.wfile.write(message.encode("UTF-8"))
    def do_GET(self):
        self.send_error(405)
    def do_POST(self):
        if self.path.startswith("/block/"):
            adversary = self.path.split("/block/")[1]
            try:
                ipaddress.ip_address(adversary)
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.block(acl_name, adversary)
            except ValueError:
                self.send_error(400)
        else:
            self.send_error(404)

def install_so2ban():
    default_action_menu = "/opt/so/saltstack/default/salt/soc/files/soc/menu.actions.json"
    local_action_menu = "/opt/so/saltstack/local/salt/soc/files/soc/menu.actions.json"
    so2ban = "foo\n"
    with open(default_action_menu) as default:
        menu = default.readlines()
        second_to_last_line = len(menu) - 1
        menu.insert(second_to_last_line, so2ban)
        with open(local_action_menu, 'w') as local:
            for action in menu:
                local.write(action)
    subprocess.run("so-soc-restart", stdout = subprocess.PIPE, check=True)
    return

def start_so2ban():
    handler = RequestHandler
    server = http.server.HTTPServer(server_address, handler)
    server.serve_forever()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--install", action = "store_true", help = "Install so2ban")
    args = parser.parse_args()
    if args.install:
        install_so2ban()
    else:
        start_so2ban()
  
if __name__ == "__main__":
    main()
