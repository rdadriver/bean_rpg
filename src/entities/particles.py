from src.etc import spritesheet

"""
particles.py

The games particle engine
"""

particle_sprite_sheet = None


def load_sprite_sheet():
    global particle_sprite_sheet
    particle_sprite_sheet = spritesheet.SpriteSheet("src/resources/particles.png")


class ParticleEngine:

    def __init__(self):

        self.particles = []

        self.fade_particles = []

    def update(self):

        for particle in self.particles:
            particle.update()

            if particle.lifetime == 0:
                self.particles.remove(particle)
                self.fade_particles.append(particle)

        for particle in self.fade_particles:

            particle.fade_time -= 1
            if particle.fade_time == 0:
                self.fade_particles.remove(particle)
            else:
                particle.image.set_alpha(particle.image.get_alpha()-particle.fade_increment)

    def draw(self, display):

        for particle in self.particles:
            particle.draw(display)

    def clear_particles(self):

        self.particles = []
        self.fade_particles = []

    def create_fire_particle(self, x, y, lifetime):

        self.particles.append(FireParticle(x, y, lifetime))


class Particle:

    def __init__(self, image, x, y, lifetime, fade_time=10):

        self.image = image

        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

        self.lifetime = lifetime
        self.fade_time = fade_time
        self.fade_increment = 255//fade_time

    def update(self):

        self.lifetime -= 1

    def draw(self, display):

        display.blit(self.image, (self.rect.x, self.rect.y))


class FireParticle(Particle):

    def __init__(self, x, y, lifetime):

        self.image = particle_sprite_sheet.get_image_src_alpha(0, 0, 20, 20)

        Particle.__init__(self, self.image, x, y, lifetime)
