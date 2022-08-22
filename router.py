#!/usr/bin/env python3

import argparse
import netmiko

router = {
    "device_type": "cisco_ios",
    "host": "192.168.1.1",
    "username": "admin",
    "password": "password",
}
acl_name = "BLOCK_ADVERSARY"

def show_acl(acl_name):
    with netmiko.ConnectHandler(**router) as net_connect:
        command = "show run | section ip access-list standard " + acl_name
        acl = net_connect.send_command(command)
        print(acl)

def unblock_host(acl_name, host):
    with netmiko.ConnectHandler(**router) as net_connect:
        commands = [
            ("ip access-list standard " + acl_name),
            ("no deny " + host)
        ]
        net_connect.send_config_set(commands)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--show-acl", action = "store_true", help = "Install so2ban")
    parser.add_argument("--unblock-host", action = "store_true", help = "Start so2ban")
    args = parser.parse_args()
    if args.show_acl:
        show_acl()
    elif args.unblock_host:
        unblock_host()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
