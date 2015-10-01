# Munin-for-Android-GCM-Trigger
Python script called by munin, sending signals to Munin-for-Android-GCM-Proxy

You have to install this script on the master server of your munin installation. Here's how it works:

1. munin detects an alert and calls this script
2. This script sends the signal with plugin information to the proxy, relaying the info to Google Cloud Messaging
3. An alert appears on your device

## Installation
You only have to install this script once, even if several Android devices will be notified.

### Install & configure the script
Install the script wherever you want.

### Configure munin
We have to configure munin in order to make it call this script on each alert.
Open `/etc/munin/munin.conf`, and configure it as following:
    
    # Munin for Android notifications
    # Configure script location & args
    contact.munin_for_android.command | /path/to/script /path/to/script \
       --cmdlineargs="${var:group} ${var:host} ${var:graph_category} '${var:graph_title}'"
    
    # Configure alerts level
    contact.munin_for_android.always_send warning critical
    
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

