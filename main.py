import sys

import yaml
from pygame import mixer, event, font, display, K_ESCAPE, KEYDOWN, QUIT


class Drumpy:
    KEYMAP_FILE = 'keymap.yaml'
    FONT_SIZE = 20
    FONT_COLOR = (150, 250, 150)
    BG_COLOR = (20, 40, 20)
    WINDOW_WIDTH = 420
    WINDOW_CAPTION = 'Drumpy'
    MARGIN = 5

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

        # Get any mono font, if no mono fonts use system default
        fonts = tuple(filter(lambda txt: 'mono' in txt, font.get_fonts()))
        win_font = fonts[0] if fonts else None
        font.init()
        self._font = font.SysFont(win_font, self.FONT_SIZE)

        # Set up the window
        win_height = len(self._keymap) * self.FONT_SIZE + 2 * self.MARGIN
        self._screen = display.set_mode((self.WINDOW_WIDTH, win_height))
        display.set_caption(self.WINDOW_CAPTION)

    def run(self):
        """ Prepare sounds and run main loop """
        self._register_all_sounds()
        self._print(self._keymap_description)

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
        # To describe keymap to user
        self._keymap_description = []

        for key, settings in self._keymap.items():
            # Get sound file and volume for this key
            filename = settings.get('file')
            vol = settings.get('volume', 1.0)

            # Create Sound obj and put it in our key-sound dict
            sound = mixer.Sound(filename)
            sound.set_volume(vol)
            self._key_sound[key] = sound

            # Prepare key description
            filename_description = filename.replace("samples/", "")
            self._keymap_description.append(f'[ {key} ]  {filename_description} {round(vol * 100)}%')

    def _play_sound(self, key):
        if key not in self._key_sound:
            self._print((f'Key "{key}" is not set in {self.KEYMAP_FILE}',))
            return

        # Forcing finding free channel and use it to play sound
        ch = mixer.find_channel(True)
        sound = self._key_sound[key]
        ch.play(sound)

        self._print(self._keymap_description)

    def _print(self, txt_list):
        """ Prints text in the pygame window """
        self._screen.fill(self.BG_COLOR)
        for line, txt in enumerate(txt_list):
            line_y_pos = line * self.FONT_SIZE
            txt_surface = self._font.render(txt, True, self.FONT_COLOR)
            self._screen.blit(txt_surface, (self.MARGIN, self.MARGIN + line_y_pos))
        display.flip()


if __name__ == '__main__':
    Drumpy().run()
