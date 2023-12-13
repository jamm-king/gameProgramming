from .Mesh3D import *
from .Transform import *
from .Object import *
from .Cube import *
from .Sphere import *


def apply_gravity(object, dt):
    gravity = -9.8
    velocity = object.velocity
    velocity_x = velocity.x
    velocity_y = velocity.y
    velocity_z = velocity.z

    velocity_y += gravity * dt
    velocity.update((velocity_x, velocity_y, velocity_z))


def detect_collision(objects):
    for i in range(len(objects)):
        object = objects[i]
        for j in range(i + 1, len(objects)):
            other_object = objects[j]
            if object.check_collision(other_object):
                print("collision detected")
                process_collision(object, other_object)


def process_collision(a: Object, b: Object):
    a.resolve_collision(b)
