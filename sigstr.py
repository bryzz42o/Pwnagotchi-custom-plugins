import logging
import os
import json
import pwnagotchi.plugins as plugins
import pwnagotchi.ui.fonts as fonts
from pwnagotchi.ui.components import LabeledValue
from pwnagotchi.ui.view import BLACK

# Static Variables
TAG = "[SigStr Plugin]"

class SigStr(plugins.Plugin):
    __author__ = 'bryzz42o'
    __version__ = '1.0.3'
    __license__ = 'GPL3'
    __description__ = 'Plugin to display signal strength as a bar.'

    def __init__(self):
        self.strength = 0

    def on_loaded(self):
        logging.info(TAG + " Plugin loaded")

    def on_ui_setup(self, ui):
        ui.add_element('SignalStrength', LabeledValue(color=BLACK, label='Signal', value='',
                                                      position=(10, 10),
                                                      label_font=fonts.Bold, text_font=fonts.Medium))

    def on_ui_update(self, ui):
        # Assuming self.strength is updated elsewhere in the code
        signal_bar = self.generate_signal_bar(self.strength)
        ui.set('SignalStrength', signal_bar)

    def generate_signal_bar(self, strength):
        # Assuming strength is a value between 0 and 100 representing signal strength
        bar_length = int(strength / 10)  # Divide strength by 10 to get bar length (assuming 10 units per bar segment)
        bar_segments = '█' * bar_length  # Use '█' character to represent filled bar segments
        empty_segments = '░' * (10 - bar_length)  # Use '░' character to represent empty bar segments
        signal_bar = f'|{bar_segments}{empty_segments}|'  # Construct the full signal bar string
        return signal_bar
