import sys

import yaml
from pygame import mixer, event, font, display, K_ESCAPE, KEYDOWN, QUIT


class Drumpy:
    KEYMAP_FILE = 'keymap.yaml'
    FONT_SIZE = 30
    FONT_COLOR = (150, 250, 150)
    BG_COLOR = (20, 40, 20)
    WINDOW_SIZE = (550, 28)
    WINDOW_CAPTION = 'Drumpy'

    def __init__(self):
        # Store keyboard keys and corresponded sounds
        self._key_sound = {}

        # Load keymap settings
        with open(self.KEYMAP_FILE) as f:
            self._keymap = yaml.safe_load(f)

        # Lower buffer to lower sound delay
        mixer.init(44100, -16, 2, 256)
        # Set higher channels number, allows to play many sounds
        # at the same time without stopping previously started ones
        mixer.set_num_channels(20)

        # Set up the window
        self._screen = display.set_mode(self.WINDOW_SIZE)
        display.set_caption(self.WINDOW_CAPTION)

        # Set up font
        font.init()
        self._font = font.SysFont(None, self.FONT_SIZE)

    def run(self):
        """ Prepare sounds and run main loop """
        self._register_all_sounds()
        self._print_keys()

        while True:
            for e in event.get():
                if e.type == QUIT:
                    sys.exit()
                elif e.type == KEYDOWN:
                    self._handle_keydown(e)

    def _handle_keydown(self, e):
        if e.key == K_ESCAPE:
            sys.exit()
        else:
            self._play_sound(e.unicode)

    def _register_all_sounds(self):
        """
        Create Sound object for each sound file and
        store it in the key-sound dict
        """
        for key, settings in self._keymap.items():
            # Get sound file and volume for this key
            filename = settings.get('file')
            if not filename:
                self._print(f'Skipping "{key}" key, file not set in keymap')
                continue
            vol = settings.get('volume', 1.0)

            # Create Sound obj and put it in our key-sound dict
            sound = mixer.Sound(filename)
            sound.set_volume(vol)
            self._key_sound[key] = sound

    def _play_sound(self, key):
        if key not in self._key_sound:
            self._print(f'Wrong key "{key}", not set in {self.KEYMAP_FILE}')
            return

        # Forcing finding free channel and use it to play sound
        ch = mixer.find_channel(True)
        sound = self._key_sound[key]
        ch.play(sound)

        self._print_keys()

    def _print(self, txt):
        """ Prints text in the pygame window """
        self._screen.fill(self.BG_COLOR)
        txt_surface = self._font.render(txt, True, self.FONT_COLOR)
        self._screen.blit(txt_surface, (5, 3))
        display.flip()

    def _print_keys(self):
        """ Print all keyboard keys correctly set in keymap settings """
        self._print('[ ' + ' ]  [ '.join(self._key_sound.keys()) + ' ]')


if __name__ == '__main__':
    Drumpy().run()
