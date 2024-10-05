# Base templates for Omada Log Analysis

# Disconnects, hardwired and wireless, with/ without reconnect
disc_hw = (
    "{utc} {hardware_controller}  {local_time} {controller} - - - [client:{client_name_and_mac}] "
    'was disconnected from network "{network}" on [{network_device_type}:{network_device}:{network_device_mac}]'
    "(connected time:{time} connected, traffic: {data})."
)

disc_w = (
    "{utc} {hardware_controller}  {local_time} {controller} - - - [client:{client_name_and_mac}] "
    'is disconnected from SSID "{ssid}" on [{network_device_type}:{network_device}:{network_device_mac}] '
    "({time} connected, {data})."
)

disc_hw_recon = (
    "{utc} {hardware_controller}  {local_time} {controller} - - - [client:{client_name_and_mac}] "
    'was disconnected from network "{network}" on '
    "[{network_device_type}:{network_device}:{network_device_mac}](connected time:{time} "
    'connected, traffic: {data}) and connected to network "{recon_network}" on '
    "[{recon_network_device_type}:{recon_network_device}:{recon_network_device_mac}]."
)

disc_w_recon = (
    "{utc} {hardware_controller}  {local_time} {controller} - - - [client:{client_name_and_mac}] "
    'is disconnected from SSID "{ssid}" on [{network_device_type}:{network_device}:{network_device_mac}] '
    '({time} connected, {data}) and connected to SSID "{recon_ssid}" on '
    "[{recon_network_device_type}:{recon_network_device}:{recon_network_device_mac}]."
)

# DHCP server assigned an address
dhcp_assign = (
    "{utc} {hardware_controller}  {local_time} {controller} - - - "
    "DHCP Server allocated IP address {client_ip} for the client[MAC: {client_mac}].#015"
)

dhcp_reject = (
    "{utc} {hardware_controller}  {local_time} {controller} - - - DHCP Server rejected the request"
    " of the client[MAC: {client_mac} IP: {client_ip}].#015"
)

# DHCPS initialization
dhcps = "{utc} {hardware_controller}  {local_time} {controller} - - - DHCPS initialization {result}.#015"

# Connections, hardwired and wireless
conn_hw = (
    "{utc} {hardware_controller}  {local_time} {controller} - - - [client:{client_name_and_mac}] "
    "is connected to [{network_device_type}:{network_device}:{network_device_mac}] on {network} network."
)

conn_w = (
    "{utc} {hardware_controller}  {local_time} {controller} - - - [client:{client_name_and_mac}] "
    'is connected to [{network_device_type}:{network_device}:{network_device_mac}] with SSID "{ssid}" '
    "on channel {channel}."
)

# Wireless roaming
roaming = (
    "{utc} {hardware_controller}  {local_time} {controller} - - - [client:{client_name_and_mac}] "
    "is roaming from [{network_device_type}:{network_device}:{network_device_mac}][{channel}] to "
    "[{roaming_network_device_type}:{roaming_network_device}:{roaming_network_device_mac}][{roaming_channel}] "
    "with SSID {roaming_ssid}"
)

# Logins
login = (
    "{utc} {hardware_controller}  {local_time} {controller} - - - "
    "{user} logged in to the controller from {login_ip}."
)

failed_login = (
    "{utc} {hardware_controller}  {local_time} {controller} - - - "
    "{user} failed to log in to the controller from {login_ip}."
)

# Blocked connections
blocked = (
    "{utc} {hardware_controller}  {local_time} {controller} - - - [client:{client_name_and_mac}] "
    "failed to connected to [{network_device_type}:{network_device}:{network_device_mac}] "
    'with SSID "{ssid}" on channel {channel} because the user '
    "is blocked by Access Control.({number} {discard_text})"
)

# Auto backup
auto_backup = (
    "{utc} {hardware_controller}  {local_time} {controller} - - - "
    "Auto Backup executed with generating file {filename}."
)

# Online/Offline Devices, hardwired and wireless
online_hw = (
    "{utc} {hardware_controller}  {local_time} {controller} - - - [client:{client_name_and_mac}] "
    "went online on [{network_device_type}:{network_device}:{network_device_mac}] on {network} network."
)

offline_hw = (
    "{utc} {hardware_controller}  {local_time} {controller} - - - [client:{client_name_and_mac}] "
    'went offline from network "{network}" on '
    "[{network_device_type}:{network_device}:{network_device_mac}](connected time:{time} "
    "connected, traffic: {data})."
)

online_w = (
    "{utc} {hardware_controller}  {local_time} {controller} - - - [client:{client_name_and_mac}] "
    "(IP: {client_ip}, Username: {username} went online on "
    '[{network_device_type}:{network_device}:{network_device_mac}] with SSID "{ssid}" on channel {channel}.'
)

offline_w = (
    "{utc} {hardware_controller}  {local_time} {controller} - - - [client:{client_name_and_mac}] "
    '(IP: {client_ip}, Username: {username}) went offline from SSID "{ssid}" on '
    "[{network_device_type}:{network_device}:{network_device_mac}] ({time} connected, {data})."
)

# Network devices connected/disconnected
device_connected = (
    "{utc} {hardware_controller}  {local_time} {controller} - - - "
    "[{network_device_type}:{network_device}:{network_device_mac}] was connected."
)

device_disconnected = (
    "{utc} {hardware_controller}  {local_time} {controller} - - - "
    "[{network_device_type}:{network_device}:{network_device_mac}] was disconnected."
)

# Network devices obtaining IP Addresses
got_ip_address = (
    "{utc} {hardware_controller}  {local_time} {controller} - - - "
    "[{network_device_type}:{network_device}:{network_device_mac}] "
    "got IP address {ip_address}/{subnet_mask}."
)

# Interface up/down
up_or_down = (
    "{utc} {hardware_controller}  {local_time} {controller} - - - "
    "[{interface}] of [{network_device_type}:{network_device}:{network_device_mac}] is {state}.#015"
)


# Dictionary of templates 'search_string' : [template, number_of_expected_values, event name]
# Some notes: use of the search string increases the speed of the parsing function
# Search string must be present in the event data for the parsing function to even attempt using a template
# Some search strings (ie: disconnected from SSID, connected to) will be present in multiple log event types
# In order to confirm that the correct template was used, its results will be tested for correct number of values
# The event name will be that value that populates the event_type column as the search string isn't terrific

omada_template_dict = {
    "is disconnected from SSID": [disc_w, 11, "disc_w"],
    "disconnected from SSID": [disc_w_recon, 15, "disc_w_recon"],
    "was disconnected from network": [disc_hw, 11, "disc_hw"],
    "disconnected from network": [disc_hw_recon, 15, "disc_hw_recon"],
    "allocated IP address": [dhcp_assign, 6, "dhcp_assign"],
    "rejected the request": [dhcp_reject, 6, "dhcp_reject"],
    "is connected to": [conn_hw, 9, "conn_hw"],
    "connected to": [conn_w, 10, "conn_w"],
    "roaming": [roaming, 14, "roaming"],
    "logged in to": [login, 6, "login"],
    "failed to log in": [failed_login, 6, "failed_login"],
    "blocked by Access Control": [blocked, 12, "blocked"],
    "Auto Backup executed": [auto_backup, 5, "auto_backup"],
    "DHCPS initialization": [dhcps, 5, "dhcps"],
    "went online": [online_hw, 9, "online_hw"],
    "went offline from network": [offline_hw, 11, "offline_hw"],
    "went online on": [online_w, 12, "online_w"],
    "went offline from SSID": [offline_w, 13, "offline_w"],
    "was connected.": [device_connected, 7, "device_connected"],
    "was disconnected.": [device_disconnected, 7, "device_disconnected"],
    "got IP address": [got_ip_address, 9, "device_dhcp_assign"],
    "] of [": [up_or_down, 9, "up_or_down"], # This search string is pretty goofy, but it works,
}  # could potentially be two different templates with 'is up' and 'is down' search strings for better clarity

