## so2ban
Blocks IP addresses from the Security Onion Console.

### How to Install so2ban on Security Onion
**Step 1.** Download this GitHub repository using an Internet-accessible computer. 
```
git clone https://github.com/cyberphor/so2ban
```

**Step 2.** Run `Get-Requirements.sh` using an Internet-accessible computer.
```
cd so2ban
bash Get-Requirements.sh
```

**Step 3.** Copy everything from your Internet-accessible computer to Security Onion using SCP. An alternative method is burning `so2ban` and the files downloaded in Step 2 to a CD or USB drive. 
```bash
scp -r so2ban/ victor@192.168.1.69:~
```

**Step 4.** Install Netmiko and its dependencies on Security Onion. 
```bash
cd so2ban
cd netmiko
pip3 install --no-index --find-links . -r requirements.txt
```

## Copyright
This project is licensed under the terms of the [MIT license](/LICENSE). 
