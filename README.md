supplicanted
============

Supplicanted is a Web service that listens on particular port and exposes
user-friendly Web interface that can be used to change WiFi settings.

It can help you if your system is running wpa-supplicant and using it
to configure encryption. It is especially useful if you have an embedded board
(like a Raspberry Pi) and want to configure it's WiFi over DHCP-driven Ethernet.

If you pass both SSID and passphrase, a protected network will be configured.
If you don't pass SSID, open network (key_mgmt=NONE) will be configured.

wpa_supplicant will be forced to reread config after change. Supplicanted
will periodically refresh info from wpa_cli status.

It requires [brilliant](https://github.com/piotrmaslanka/brilliant) to operate.

Read COPYRIGHT for copyright stuff.