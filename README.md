# CAT
Conan Exiles Anti-DDOS Tools

## Tools:
- DumpIps_win.py: Creates a list of IPs to blacklist in real time reading Conan Exiles server logs
- Simple_server.py: It exposes the current directory to the localhost

## Requeriments:
- Python 3
- pypiwin32 (maybe it's installed by default Anaconda install, otherwise use: pip install pypiwin32)
- Conan Exiles sandbox log file with the needed debug information.

## Use:
In Win32: 
- Copy the dumpips_win.py and simple_server.py to the running Conan logs folder, and run both. They will use such folder.
- Use a third-party app to add the iplist.txt file to the Firewall, and reload it in realtime if possible to avoid DDoS activity. 

I recommend WaGi's IP-blacklister: https://github.com/WaGi-Coding/WaGis-Mass-IP-Blacklister-Windows , just change the url:port and file to the exposed by simple_server.py 

At the moment other platforms are not supported (this is an easy TODO) but the changes in dumpips should be minimum, and you will need a crontab or something to update the iptables, and consider they can be thousands per minute. 

## Notes
In case of heavy attacks keep an eye on WaGi's blacklister because with high number it can be saturated in only a few hours specially if the number of ips like 10.000, 50.000... 
The solution then is restarting WaGi(and don't forget to press On/Off check), or if the number is huge: stop dumpIps, stop Wagi, RENAME the win32 firewall rules to avoid WaGi overwriting them, stop Conan, remove all the conan logs from the folder, restart conan, and restart dumpIps and WaGi. 

Then you will then accummulate windows firewall rules for all the ips (remember to rename using dates if the collection is huge too!), but this will keep WaGi fresh and healthy against new attacks.

There is no magic solutions to avoid a DDOS but there are a lot of things to try to mitigate it, because there are a lot of different DDOS attacks too. Basically you can mitigate it if you have a really good ISP provider, you close all the non-important rules on the firewall, and block some ip activity. 


Just remember that you will never win all the battles and that you will always have to learn new things to try. Maintaining a server it's not an easy task when you get attacked, just never give up and get help.


[![CodeFactor](https://www.codefactor.io/repository/github/powermates/cat/badge/main)](https://www.codefactor.io/repository/github/powermates/cat/overview/main)
