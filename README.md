## so2ban
Blocks IP addresses from the Security Onion Console.

### How to Install so2ban on Security Onion
**Step 1.** Download this GitHub repository using an Internet-accessible computer. Steps 2 to 4 were written for someone who has an air-gap instance of Security Onion. If this does not apply to you, skip ahead to Step 5. 
```
git clone https://github.com/cyberphor/so2ban.git
```

**Step 2.** Run `Get-Requirements.sh` from the `so2ban` directory using an Internet-accessible computer.
```
cd so2ban
bash Get-Requirements.sh
cd ../
```

**Step 3.** Copy everything from your Internet-accessible computer to Security Onion using SCP (an alternative method is burning `so2ban` and the files downloaded in Step 2 to a CD or USB drive). 
```bash
scp -r so2ban/ victor@192.168.1.69:~
```

**Step 4.** Install the Python library "Netmiko" and its dependencies on Security Onion. `so2ban` leverages "Netmiko" to access and modify devices at the network perimeter. 
```bash
cd so2ban/netmiko
pip3 install --no-index --find-links . -r requirements.txt
cd ../
```

**Step 5.** Run `so2ban.py` with the `--install` parameter on Security Onion. 
```bash
sudo python3 so2ban.py --install
```

## Copyright
This project is licensed under the terms of the [MIT license](/LICENSE). 
