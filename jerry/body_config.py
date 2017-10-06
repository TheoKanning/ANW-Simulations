from math import pi
import pygame

# Size and Weight Constants
TOTAL_MASS = 80  # Made up units
TOTAL_HEIGHT = 350  # Pygame pixels
STARTING_X_POSITION = 100
STARTING_Y_POSITION = 5
STARTING_SPEED = 0, 0  # pixels/sec?

# Mass Fractions #
mass_fractions = {
    "head": 0.0826,
    "torso": 0.551,
    "upper_arm": 0.0325,
    "forearm": 0.0187 + 0.0065,  # Including hand
    "thigh": 0.105,
    "calf": 0.0475,
    "foot": 0.0143
}

# Segment Masses
masses = {}
for segment in mass_fractions:
    masses[segment] = mass_fractions[segment] * TOTAL_MASS

# Height Fractions #
height_fractions = {
    "head": 0.2,  # Larger for cartoon, anatomically correct is 0.1075
    "torso": 0.3,
    "upper_arm": 0.172,
    "forearm": 0.157 + 0.057,  # Including hand
    "thigh": 0.25,  # standard is .232
    "calf": 0.23,  # standard is .247
    "foot": 0.1  # Counts foot length, not height
}

# Segment Lengths
lengths = {}
for segment in height_fractions:
    lengths[segment] = height_fractions[segment] * TOTAL_HEIGHT

# Starting Height Fractions #
# todo all of these height calculation assume a completely vertical start. They should be calculated dynamically or
# removed
SHOULDER_STARTING_HEIGHT_FRACTION = height_fractions["calf"] + height_fractions["thigh"] + height_fractions["torso"]
HIP_STARTING_HEIGHT_FRACTION = height_fractions["calf"] + height_fractions["thigh"]

# Starting Positions
HEAD_POSITION = STARTING_X_POSITION, TOTAL_HEIGHT * SHOULDER_STARTING_HEIGHT_FRACTION + lengths[
    "head"] + STARTING_Y_POSITION
TORSO_POSITION = STARTING_X_POSITION, TOTAL_HEIGHT * HIP_STARTING_HEIGHT_FRACTION + lengths[
    "torso"] + STARTING_Y_POSITION

# Joint Constraints #
joint_ranges = {
    "neck": (3 * pi / 4, 5 * pi / 4),
    "elbow": (0, 3 * pi / 4),
    "shoulder": (-pi / 2, pi),
    "hip": (-pi / 8, pi / 3),
    "knee": (-2 * pi / 3, 0),
    "ankle": (0, 2 * pi / 3)
}

default_joint_angles = {
    "neck": pi,
    "left_shoulder": 0,
    "left_elbow": 0,
    "right_shoulder": 0,
    "right_elbow": 0,
    "left_hip": 0,
    "left_knee": 0,
    "left_ankle": (pi / 2),
    "right_hip": 0,
    "right_knee": 0,
    "right_ankle": (pi / 2)
}

# Collision Types #
collision_types = {
    "upper": 1,
    "lower": 2,
    "ground": 3
}

body_collision_types = {
    "torso": collision_types["upper"],
    "head": collision_types["upper"],
    "upper_arm": collision_types["upper"],
    "forearm": collision_types["upper"],
    "thigh": collision_types["upper"],
    "calf": collision_types["lower"],
    "foot": collision_types["lower"]
}

# Images
images = {
    "torso": pygame.image.load("images/torso.bmp"),
    "head": pygame.image.load("images/head.bmp"),
    "upper_arm": pygame.image.load("images/upper_arm.bmp"),
    "forearm": pygame.image.load("images/forearm.bmp"),
    "thigh": pygame.image.load("images/thigh.bmp"),
    "calf": pygame.image.load("images/leg.bmp"),
    "foot": pygame.image.load("images/foot.bmp")
}


class SegmentInfo:
    """
    All starting info for a body segment
    """

    def __init__(self, mass, length, image, collision_type):
        self.mass = mass
        self.length = length
        self.image = image
        self.collision_type = collision_type
        self.start_speed = STARTING_SPEED


segments = {}
for key in mass_fractions:
    segments[key] = SegmentInfo(masses[key], lengths[key], images[key], body_collision_types[key])