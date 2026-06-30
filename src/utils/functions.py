from src.utils.librairies import *
from src.utils.settings import *


data = {}
images = {}
fonts = {}

def load_data(file, path = 'data/'):
    global data
    if file not in data:
        file_path = path + str(file) + '.json'
        with open(file_path, 'r') as f:
            data[file] = json.load(f)
    return data[file]

def write_data(updated_data, file, path = 'data/'):
    global data
    if file in data:
        data[file] = updated_data
    file_path = path + str(file) + '.json' 
    with open(file_path, 'w') as f:
        json.dump(updated_data, f)


def load_image(image_name, image_path : str):
    if image_name not in images:
        image = pygame.image.load('assets/textures/' + image_path).convert_alpha()
        images[image_name] = image
    return images[image_name]

def load_font(size):
    """Récupère la police d'écriture"""
    if size not in fonts:
        fonts[size] = pygame.font.Font(TEXT_FONT, size)
    return fonts[size]

def rand(value, int_mode=False):
    if not type(value) is tuple:
        return value  # int, float
    lo, hi = value
    if lo >= hi:
        return lo
    return random.randint(lo, hi) if int_mode else random.uniform(lo, hi)

def easeDefault(t):
    return t

def easeOutBack(t, s=1.70158):
    return 1 + (s + 1) * (t - 1)**3 + s * (t - 1)**2

def easeOutQuart(t):
    return 1 - pow(1 - t, 4)

def easeOutCubic(t):
    return 1 - pow(1 - t, 3)


def easeOutElastic(t,
                    amplitude=1,
                    frequency=5.0,
                    decay=14.0):
    
    c4 = (2 * math.pi) / 3

    if t == 0:
        return 0
    if t == 1:
        return 1

    return (
        amplitude *
        pow(2, -decay * t) *
        math.sin((t * frequency - 0.75) * (2 * math.pi / 3))
        + 1
    )

def smoothApproach(val, target, dt, slowness=1):
    val += (target - val) / slowness * min(dt, slowness)
    return val


def generateRound(pixel_size = 5, radius = 100, color = (255, 255, 255)):
    scaled_radius = radius // pixel_size if pixel_size <= radius else radius

    surface = pygame.Surface((scaled_radius*2, scaled_radius*2), pygame.SRCALPHA).convert_alpha()
    pygame.draw.circle(surface, color, (scaled_radius, scaled_radius), scaled_radius)
    surface = pygame.transform.scale(surface, (radius * 2, radius * 2))

    return surface


def getFrame(sprite_sheet, width, height, frame_x = 0, frame_y = 0):
    image = pygame.Surface((width, height), pygame.SRCALPHA).convert_alpha()
    image.blit(sprite_sheet, (0, 0), ((frame_x* width), (frame_y* height), width, height))
    return image

def drawText(surface, text, text_size, pos, text_color = (255, 255, 255), alignment = 'center', angle = 0):
    font = load_font(int(text_size))
    text_surface = font.render(str(text), True, text_color)

    if angle != 0:
        text_surface = pygame.transform.rotate(text_surface, angle)

    text_rect = text_surface.get_rect(**{alignment: pos})
    surface.blit(text_surface, text_rect)