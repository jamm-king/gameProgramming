from .Mesh3D import *
from .Transform import *
from .Camera import *

class Object:
    def __init__(self, obj_name):
        self.name = obj_name
        self.mesh = None
        self.transform = Transform()
        self.components = []
        self.scene_angle = 0

        self.velocity = pygame.Vector3((0, 0, 0))
        self.mass = 10

    def set_mesh(self, mesh):
        if isinstance(mesh, Mesh3D):
            self.mesh = mesh

    def get_mesh(self):
        return self.mesh

    def get_transform(self):
        return self.transform

    def get_position(self):
        return self.transform.get_position()

    def get_velocity(self):
        return self.velocity

    def update(self, camera: Camera, dt, events=None):
        self.transform.update_position(self.velocity * dt)

        glPushMatrix()
        glLoadMatrixf(self.transform.get_MVM() * camera.get_VM())
        glColor(1, 1, 1)
        self.mesh.draw(camera.forward)
        glPopMatrix()

    def get_aabb(self):
        vertices = self.mesh.vertices
        temp = np.hstack((vertices, np.ones((len(vertices), 1))))
        temp = np.dot(temp, self.transform.get_MVM())
        min_x = min(temp[:, 0])
        max_x = max(temp[:, 0])
        min_y = min(temp[:, 1])
        max_y = max(temp[:, 1])
        min_z = min(temp[:, 2])
        max_z = max(temp[:, 2])
        return (min_x, max_x, min_y, max_y, min_z, max_z)

    def check_collision(self, other_mesh):
        min_x1, max_x1, min_y1, max_y1, min_z1, max_z1 = self.get_aabb()
        min_x2, max_x2, min_y2, max_y2, min_z2, max_z2 = other_mesh.get_aabb()

        overlap_x = max(0, min(max_x1, max_x2) - max(min_x1, min_x2))
        overlap_y = max(0, min(max_y1, max_y2) - max(min_y1, min_y2))
        overlap_z = max(0, min(max_z1, max_z2) - max(min_z1, min_z2))

        return overlap_x > 0 and overlap_y > 0 and overlap_z > 0

    # def resolve_collision(self, other):
    #     relative_velocity = other.velocity - self.velocity
    #     relative_position = other.get_position() - self.get_position()
    #     collision_normal = relative_position / np.linalg.norm(relative_position)
    #     relative_velocity_normal = np.dot(relative_velocity, collision_normal)
    #
    #     new_relative_velocity_normal = -relative_velocity_normal
    #
    #     self.velocity -= new_relative_velocity_normal * collision_normal
    #     other.velocity += new_relative_velocity_normal * collision_normal

    def resolve_collision(self, other):
        restitution = 0.8

        relative_velocity = other.velocity - self.velocity
        collision_normal = pygame.Vector3(other.get_position() - self.get_position()).normalize()
        relative_velocity_along_normal = pygame.Vector3.dot(relative_velocity, collision_normal)

        if relative_velocity_along_normal > 0:
            return

        impulse = -(1 + restitution) * relative_velocity_along_normal
        impulse /= (1 / self.mass) + (1 / other.mass)

        self.velocity -= impulse / self.mass * collision_normal
        other.velocity += impulse / other.mass * collision_normal
