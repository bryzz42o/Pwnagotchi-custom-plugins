import logging
from time import sleep
from scapy.all import Dot11, Dot11Beacon, Dot11Elt, RadioTap, sendp, RandMAC
from pwnagotchi import plugins

class WiFiHoneypot(plugins.Plugin):
    __author__ = 'bryzz42o'
    __version__ = '1.0.1'
    __license__ = 'GPL3'
    __description__ = 'Creates a Wi-Fi honeypot.'

    def __init__(self):
        super().__init__()
        self.honeypot_active = False
        self.shutdown = False

        # Default configuration options
        self.options = {
            'ssid': 'FreeWiFi',
            'password_protected': False,
            'beacon_interval': 0.1,
            'max_clients': 10
        }

    def create_beacon(self, name, password_protected=False):
        dot11 = Dot11(type=0,
                      subtype=8,
                      addr1='ff:ff:ff:ff:ff:ff',
                      addr2=str(RandMAC()),
                      addr3=str(RandMAC()))

        beacon = Dot11Beacon(cap='ESS+privacy' if password_protected else 'ESS')
        essid = Dot11Elt(ID='SSID', info=name, len=len(name))

        if not password_protected:
            return RadioTap() / dot11 / beacon / essid

        rsn = Dot11Elt(ID='RSNinfo', info=(
            '\x01\x00'
            '\x00\x0f\xac\x02'
            '\x02\x00'
            '\x00\x0f\xac\x04'
            '\x00\x0f\xac\x02'
            '\x01\x00'
            '\x00\x0f\xac\x02'
            '\x00\x00'))

        return RadioTap() / dot11 / beacon / essid / rsn

    def on_loaded(self):
        logging.info('[WiFiHoneypot] Plugin loaded')

    def on_ready(self, agent):
        logging.info('[WiFiHoneypot] Ready to start honeypot')
        self.honeypot_active = True
        main_config = agent.config()

        # Read configuration options from config.toml
        wifi_honeypot_config = main_config['main']['plugins']['wifi_honeypot']
        self.options['ssid'] = wifi_honeypot_config.get('ssid', self.options['ssid'])
        self.options['password_protected'] = wifi_honeypot_config.get('password_protected', self.options['password_protected'])
        self.options['beacon_interval'] = wifi_honeypot_config.get('beacon_interval', self.options['beacon_interval'])
        self.options['max_clients'] = wifi_honeypot_config.get('max_clients', self.options['max_clients'])

        while self.honeypot_active and not self.shutdown:
            beacon = self.create_beacon(self.options['ssid'], password_protected=self.options['password_protected'])
            sendp(beacon, iface=main_config['main']['iface'], verbose=False)
            sleep(self.options['beacon_interval'])

    def on_before_shutdown(self):
        self.shutdown = True

    def on_unload(self):
        logging.info('[WiFiHoneypot] Plugin unloaded')


    def on_unload(self, ui):
        with ui._lock:
            ui.remove_element('honeypot_status')
