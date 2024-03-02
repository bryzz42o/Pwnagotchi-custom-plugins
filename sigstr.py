import logging
import subprocess
import pwnagotchi.plugins as plugins
from pwnagotchi.ui.components import LabeledValue, Bar
from pwnagotchi.ui.view import BLACK
import pwnagotchi.ui.fonts as fonts


class SigStr(plugins.Plugin):
    __author__ = 'bryzz42o'
    __version__ = '1.0.1'
    __license__ = 'GPL3'
    __description__ = 'Plugin to display signal strength as a bar.'

    def __init__(self):
        super().__init__()

    def get_signal_strength(self):
        try:
            # Run iwconfig command to get the signal strength
            iwconfig_output = subprocess.check_output(['iwconfig', 'wlan0']).decode('utf-8')
            # Find and extract the signal strength from the output
            signal_strength_line = [line for line in iwconfig_output.split('\n') if 'Signal level' in line][0]
            signal_strength = int(signal_strength_line.split('Signal level=')[-1].split(' ')[0])
            return signal_strength
        except Exception as e:
            logging.error(f'Error retrieving signal strength: {e}')
            return None

    def on_ui_setup(self, ui):
        with ui._lock:
            # Add UI element to display signal strength as a bar
            ui.add_element('signal_strength', Bar(color=BLACK, label='Signal', value=0, min_value=0, max_value=100, position=(ui.width() / 2 + 20, ui.height() - 25),
                                                  label_font=fonts.Bold, text_font=fonts.Medium))

    def on_ui_update(self, ui):
        with ui._lock:
            # Update signal strength bar value on UI update
            signal_strength = self.get_signal_strength()
            if signal_strength is not None:
                # Map the signal strength to a value between 0 and 100
                signal_strength_percentage = max(0, min(100, signal_strength))
                # Set the signal strength bar value
                ui.set('signal_strength', signal_strength_percentage)
                
