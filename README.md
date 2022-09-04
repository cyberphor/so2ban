## so2ban
Blocks IP addresses via the Security Onion Console.

### How to Install so2ban on an Air-Gapped Security Onion Manager Node
**Step 1.** Download this GitHub repository using an Internet-accessible computer. 
```
git clone https://github.com/cyberphor/so2ban
```

**Step 2.** 
```
docker build -t so2ban so2ban
```

**Step 3.** Upload `so2ban` from your Internet-accessible computer to your Security Onion Manager Node using either a CD, USB drive, or SCP. 
```
scp -r so2ban victor@192.168.1.69:~
```

**Step 4.** 
```
cd so2ban
sudo docker-compose up
```

### Screenshots
![action-menu](/Screenshots/action-menu.png)

## Copyright
This project is licensed under the terms of the [MIT license](/LICENSE). 
