usr/bin/env python3

import argparse
import http.server
import ipaddress
import json
import netmiko
import os
import shutil
import ssl
import subprocess

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
                self.send_header("Content-Type", "text/html")
                self.end_headers()
                self.block(acl_name, adversary)
            except ValueError:
                self.send_error(400)
        else:
            self.send_error(404)

def create_certificate():
    print("Creating a self-signed certificate...")
    country = "US" 
    state = "New York"
    locale = "New York City"
    company = "Allsafe" 
    section = "Cybersecurity"
    common_name = os.uname()[1]
    fields = country, state, locale, company, section, common_name
    openssl = [
        "openssl",
        "req",
        "-new",
        "-x509",
        "-days",
        "365",
        "-nodes",
        "-subj",
        ("/C=%s/ST=%s/L=%s/O=%s/OU=%s/CN=%s" % fields),
        "-keyout",
        certfile_name,
        "-out",
        certfile_name
    ]
    subprocess.run(openssl, stdout = subprocess.PIPE, check = True)
    print("Done!")
    return

def update_action_menu():
    default_action_menu = "/opt/so/saltstack/default/salt/soc/files/soc/menu.actions.json"
    local_action_menu = "/opt/so/saltstack/local/salt/soc/files/soc/menu.actions.json"
    so2ban_api = "https://%s:%s/block/{value}" % (ip, port)
    so2ban = {
        "name": "Block",
        "description": "Block at network perimeter",
        "icon": "fas fa-shield-alt",
        "target": "_blank",
        "links": [ so2ban_api ],
        "background": True,
        "method": "POST"
    }
    so2ban_action = " ," + json.dumps(so2ban) + "\n"
    if os.path.exists(local_action_menu):
        print("Adding so2ban to the local action menu...")
        with open(local_action_menu) as current:
            menu = current.readlines()
            second_to_last_line = len(menu) - 1
            menu.insert(second_to_last_line, so2ban_action)
            with open(local_action_menu, 'w') as updated:
                for action in menu:
                    updated.write(action)
    else:
        print("Creating a custom SOC action menu and adding so2ban to it...")
        with open(default_action_menu) as default:
            menu = default.readlines()
            second_to_last_line = len(menu) - 1
            menu.insert(second_to_last_line, so2ban_action)
            with open(local_action_menu, 'w') as local:
                for action in menu:
                    local.write(action)
    print("Done!")
    return

def restart_soc():
    print("Restarting the Security Onion Console...")
    subprocess.run("so-soc-restart", stdout = subprocess.PIPE, check = True)
    print("Done!")
    return

def add_firewall_exemption():
    iptables = ["iptables","-I","INPUT","1","-p","tcp","--dport","8666","-j","ACCEPT"]
    print("Adding firewall exemption to iptables...")
    subprocess.run(iptables, stdout = subprocess.PIPE, check = True)
    print("Done!")
    return

def start_so2ban():
    handler = RequestHandler
    server = http.server.HTTPServer(server_address, handler)
    server.socket = ssl.wrap_socket(
        server.socket,
        server_side = True,
        certfile = certfile_name,
        ssl_version = ssl.PROTOCOL_TLS
    )
    server.serve_forever()
    return

def show_acl(acl_name):
    with netmiko.ConnectHandler(**router) as connection:
        command = "show run | section ip access-list standard " + acl_name
        acl = connection.send_command(command)
        print(acl)
    return

def unblock_host(acl_name, host):
    with netmiko.ConnectHandler(**router) as connection:
        commands = [
            ("ip access-list standard " + acl_name),
            ("no deny " + host)
        ]
        connection.send_config_set(commands)
    return

def main():
    ip = "192.168.1.69"
    port = 8666
    server_address = (ip, port)
    certfile_name = "so2ban.pem"
    device = {
        "device_type": "",
        "host": "",
        "username": "",
        "password": "",
    }
    device["device_type"] = "cisco_ios"
    device["host"] = "192.168.1.1"
    device["username"] = "admin"
    device["password"] = "password"
    acl_name = "BLOCK_ADVERSARY"
    acl = "ip access-list standard " + acl_name
    ace = "1 deny "
    parser = argparse.ArgumentParser()
    parser.add_argument("--install", action = "store_true", help = "Install so2ban")
    parser.add_argument("--start", action = "store_true", help = "Start so2ban")
    parser.add_argument("--show-acl", action = "store_true", help = "Show access control list")
    parser.add_argument("--device-type", choices = ["cisco_ios", "paloalto_panos"], help = "Network device type")
    parser.add_argument("--device-host", help = "Network device host (e.g., IP, hostname)")
    parser.add_argument("--device-username", help = "Network device username")
    parser.add_argument("--device-password", help = "Network device password")
    args = parser.parse_args()
    if args.install:
        create_certificate()
        update_action_menu()
        restart_soc()
        add_firewall_exemption()
    elif args.start:
        start_so2ban()
    elif args.show_acl:
        show_acl()
    elif args.unblock_host:
        unblock_host()
    else:
        parser.print_help()
    return
  
if __name__ == "__main__":
    main()
