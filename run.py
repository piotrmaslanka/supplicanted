INTERFACE = ('', 8089)  # interface to listen to
PASSWORD = 'wpa_supplicant'  # password to Web interface
# Path to wpa_supplicant config file
WPA_FILE = '/etc/wpa_supplicant/wpa_supplicant.conf'
# This to prepend before network={ section of wpa_supplicant
WPA_PREPEND = '''ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev\n
update_config=1\n'''

from brilliant.smep import SMEPHandler, start_smep
import os, subprocess, time


class NetworkSettings(object):
    def __init__(self, ssid='', password=''):
        self.ssid = ssid
        self.password = password

    def __str__(self):
        """Convert to wpa supplicant file settings"""
        if self.ssid != '' and self.password != '':
            return WPA_PREPEND + ('''network={
    ssid="%s"
    psk="%s"
}''' % (self.ssid, self.password))

        if self.password == '':
            return WPA_PREPEND + ('''network={
    ssid="%s"
    key_mgmt=NONE
}''' % (self.ssid, ))

    def write(self):
        with open(WPA_FILE, 'wb') as f:
            f.write(str(self))
        os.system('wpa_cli reconfigure')


class Handler(SMEPHandler):
    def get(self):
        try:
            self.was_here
        except:
            self.was_here = True
        else:
            print 'was here'

        if self.path == '/':
            with open('supplicanted.html', 'rb') as f:
                return self.respond(f.read(), contentType='text/html; charset=utf-8')
        if self.path == '/jquery.js':
            with open('jquery.js', 'rb') as f:
                return self.respond(f.read(), contentType='application/javascript')

        self.respond('', statusCode=404)

    def post(self, args):
        if args['password'] != PASSWORD: self.respond({}, statusCode=403)

        if self.path == '/login/':
            self.respond({'status': 'ok'})

        if self.path == '/set_wifi/':
            NetworkSettings(args['ssid'], args['passphrase']).write()
            self.respond({'status': 'ok'})

        if self.path == '/status/':
            p = subprocess.Popen('wpa_cli status', stdout=subprocess.PIPE, shell=True)
            out1, err1 = p.communicate()

            self.respond(out1, contentType='text/plain')


start_smep(INTERFACE, Handler)

while True:
    time.sleep(10)