# Munin for Android GCM Trigger
Python script called by munin, sending signals to [Munin for Android GCM Proxy](https://github.com/chteuchteu/Munin-for-Android-GCM-Proxy).

You have to install this script on the master server of your munin installation. Here's how it works:

1. munin detects an alert and calls this script
2. This script sends the signal with plugin information to the proxy, relaying the info to Google Cloud Messaging
3. An alert notification appears on your devices

## Installation
You only have to install this script once, even if several Android devices will be notified.

### 1. Install & configure the script

The script relies on the [requests](https://github.com/kennethreitz/requests) library to communicate with Google Cloud
Messaging. Make sure the lib is present on your system by running the following command first (you might need to `sudo` it on some systems) : 

```bash
pip install requests
```

You must put this script in a directory accessible by munin. A good place would be /home/munin:

```bash
sudo mkdir /home/munin
sudo chown "$USER":munin /home/munin
```

Clone this repository on your server to download the script, or just download it as a ZIP archive:
    
```bash
# Navigate to the script final location
cd /home/munin

# Clone the repo
git clone https://github.com/chteuchteu/Munin-for-Android-GCM-Trigger.git

# ... OR download the ZIP archive
wget https://github.com/chteuchteu/Munin-for-Android-GCM-Trigger/archive/master.zip
unzip master.zip -d Munin-for-Android-GCM-Trigger
rm master.zip

# Update directory permissions
sudo chown -R "$USER":munin Munin-for-Android-GCM-Trigger
```
    

Don't forget to mark main file as executable:

```bash
cd Munin-for-Android-GCM-Trigger
chmod ug+x main.py
```
    
If not already done, request your unique device id for each device you'll use. Navigate to the notifications screen on
the app and hit the *Send me the instructions by mail* button.

Open the `devices.json` file and add the device id(s) in it. It should look like this:

```json
{
    "devices": [
        "VOPCG0LUaXWcnl56g2yp",
        "BLlWcH6Rh7Sb3t1S4bY1",
        "dkOoc2qDCtaHvY5yJSg7"
    ]
}
```

### 2. Test it
Once done, you can check if the script works by running the test command:

```bash
./main.py --test
```

A confirmation notification should appear on all of your devices:
![Test notification](README_testNotification.png)


### 3. Configure munin
We have to configure munin in order to make it call this script on each alert.
Open `/etc/munin/munin.conf`, and configure it as following. Replace `/home/munin/Munin-for-Android-GCM-Trigger/` with the script location.

```
# Munin for Android notifications
# Configure script location & args
contact.munin_for_android.command /home/munin/Munin-for-Android-GCM-Trigger/main.py

# Uncomment this if you want to be notified every 5 minutes about every alert
# contact.munin_for_android.always_send warning critical

# Set infos format
contact.munin_for_android.text  <alert group="${var:group}" host="${var:host}"\
  graph_category="${var:graph_category}" graph_title="${var:graph_title}" >\
  ${loop< >:wfields <warning label="${var:label}" value="${var:value}"\
    w="${var:wrange}" c="${var:crange}" extra="${var:extinfo}" /> }\
  ${loop< >:cfields <critical label="${var:label}" value="${var:value}"\
    w="${var:wrange}" c="${var:crange}" extra="${var:extinfo}" /> }\
  ${loop< >:ufields <unknown label="${var:label}" value="${var:value}"\
    w="${var:wrange}" c="${var:crange}" extra="${var:extinfo}" /> }\
  </alert>
```

Restart `munin-node` service to take configuration changes into account:

```bash
service munin-node restart
```

**That's it!**

> Tip: Watch + Star this repository to be notified when a new version of this script comes out!
