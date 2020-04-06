#!/usr/bin/env python
"""Play drums with your keyboard"""
import shutil
import sys
from pathlib import Path

import yaml
from pygame import mixer, event, font, display, K_ESCAPE, KEYDOWN, QUIT


class FileResolver:
    KEYMAP_FILENAME = 'keymap.yaml'
    SAMPLES_DIRNAME = 'samples'
    STATIC_DIRNAME = 'static'
    USER_STATIC_DIRNAME = '.drumpy'

    def __init__(self):
        # Original static files dir located in the package
        self._static_dir = Path(__file__).parent.absolute().joinpath(self.STATIC_DIRNAME)
        # A user copy of the orig static files dir to be able modify conf or samples
        self._user_static_dir = Path.home().joinpath(self.USER_STATIC_DIRNAME)
        # Make a copy of static dir in user's home dir
        self._make_user_static_copy()

    @property
    def keymap_path(self):
        return str(self._static_dir.joinpath(self.KEYMAP_FILENAME))

    def get_sample_path(self, rel_path):
        """
        Gets sound file relative path which is set in the keymap file
        and returns its absolute path.
        """
        return str(self._static_dir.joinpath(self.SAMPLES_DIRNAME, rel_path))

    def _make_user_static_copy(self):
        if not self._user_static_dir.exists():
            try:
                shutil.copytree(str(self._static_dir), str(self._user_static_dir))
            except shutil.Error:
                print('Failed to copy config files and samples to user '
                      'home directory. Using defaults instead')

        # If static files were successfully copied to user home dir
        # or it existed before use it instead of original
        if self._user_static_dir.exists():
            self._static_dir = self._user_static_dir


class Drumpy:
    FONT_SIZE = 20
    FONT_COLOR = (150, 250, 150)
    BG_COLOR = (20, 40, 20)
    WINDOW_WIDTH = 420
    WINDOW_CAPTION = 'Drumpy'
    MARGIN = 5

    def __init__(self):
        self._files = FileResolver()

        # Store keyboard keys and corresponded sounds
        self._key_sound = {}

        # Load keymap settings
        with open(self._files.keymap_path) as f:
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
            rel_path = settings.get('file')
            abs_path = self._files.get_sample_path(rel_path)
            vol = settings.get('volume', 1.0)

            # Create Sound object and put it in the key->Sound dict
            try:
                sound = mixer.Sound(abs_path)
            except FileNotFoundError:
                sys.exit(f'\nSample file {abs_path} does not exist!\nCheck your config and samples!')
            else:
                sound.set_volume(vol)
                self._key_sound[key] = sound

            # Prepare key description
            self._keymap_description.append(f'[ {key} ] {rel_path} {round(vol * 100)}%')

    def _play_sound(self, key):
        if key not in self._key_sound:
            self._print((f'Key "{key}" is not set in {self._files.KEYMAP_FILENAME}',))
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


def run():
    """Entry point"""
    Drumpy().run()


if __name__ == '__main__':
    run()
