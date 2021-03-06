import pygame

from src.etc import constants

# This deals with the loading and playing of sounds.
# Each sound has it's own channel so that we don't
# run out of channels.


class SoundEngine:

    def __init__(self):

        # Create a channel for each sound (and a dedicated music channel)
        self.music_channel = pygame.mixer.Channel(0)
        self.punch_channel = pygame.mixer.Channel(1)
        self.burn_channel = pygame.mixer.Channel(2)

        # Load all the sounds
        self.music1 = pygame.mixer.Sound("src/resources/ambient1.ogg")
        self.music2 = pygame.mixer.Sound("src/resources/ambient2.ogg")
        self.punch = pygame.mixer.Sound("src/resources/punch.ogg")
        self.burn = pygame.mixer.Sound("src/resources/burn.ogg")

        self.music = [self.music1,
                      self.music2]

        # Link the sounds to the channels they should play in
        self.channel_linkup = {self.music1: self.music_channel,
                               self.music2: self.music_channel,
                               self.punch: self.punch_channel,
                               self.burn: self.burn_channel}

        # This is all the sounds that need to be played
        self.queued_sounds = []

        # When the music channel stops playing it should que another sound to be played
        self.music_channel.set_endevent(constants.MUSIC_END_EVENT)

        # Mix the volumes
        [m.set_volume(0.06) for m in self.music]
        self.punch.set_volume(0.1)
        self.burn.set_volume(0.1)

    def play_sounds(self):

        # Plays all the queued sounds
        [self.channel_linkup[sound[0]].play(sound[0], sound[1]) for sound in self.queued_sounds]

        # And empty the queue
        self.queued_sounds = []

    def queue_sound(self, sound):

        # Add a sound to the queue
        self.queued_sounds += [sound]
