#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
# from netmiko import ConnectHandler
import argparse
import ipaddress
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

class RequestHandler(BaseHTTPRequestHandler):
    def block(self, acl_name, adversary):
        acl = "ip access-list " + acl_name
        ace = "1 deny " + adversary
        commands = [acl, ace]
        with ConnectHandler(**router) as net_connect:
            net_connect.send_command_set(commands)
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
    default_action_menu_filepath = "/opt/so/saltstack/default/salt/soc/files/soc/menu.actions.json"
    local_action_menu_filepath = "/opt/so/saltstack/local/salt/soc/files/soc/menu.actions.json"
    shutil.copyfile(default_action_menu_filepath, local_action_menu_filepath)
    
    new_action = "foo"
    with open(local_action_menu_filepath) as local_action_menu_file:
        local_action_menu = local_action_menu_file.readlines()
        second_to_last_line = len(local_action_menu) - 1
        local_action_menu.insert(second_to_last_line, new_action)
        """
        with open('new_file.txt', 'w') as new_file:
            for line in lines:
                new_file.write(line)
        """
    return

def start_so2ban():
    handler = RequestHandler
    server = HTTPServer(server_address, handler)
    server.serve_forever()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--install",action="store_true",help="Install so2ban")
    args = parser.parse_args()
    if args.install:
        install_so2ban()
    else:
        start_so2ban()
  
if __name__ == "__main__":
    main()
