## so2ban
Blocks IP addresses via the Security Onion Console.

### How to Install so2ban on an Air-Gapped Security Onion Manager Node
**Step 1.** Download this GitHub repository using an Internet-accessible computer. 
```
git clone https://github.com/cyberphor/so2ban.git
```

**Step 2.** Use `pip3` to download all `so2ban` dependencies using an Internet-accessible computer.
```
pip3 download -r so2ban/requirements.txt -d so2ban --no-binary :all: --no-cache-dir
```

**Step 3.** Upload the entire `so2ban` directory from your Internet-accessible computer to your Security Onion Manager Node using either a CD, USB drive, or SCP. 
```
scp -r so2ban victor@192.168.1.69:~
```

**Step 4.** Login to your Security Onion Manager Node and install all `so2ban` dependencies. 
```
pip3 install --no-index --find-links so2ban/ -r so2ban/requirements.txt
```

**Step 5.** Run `so2ban.py` with the `--install` parameter.
```
cd so2ban
sudo python3 so2ban.py --install
```

### Screenshots
![action-menu](/Screenshots/action-menu.png)

## Copyright
This project is licensed under the terms of the [MIT license](/LICENSE). 
