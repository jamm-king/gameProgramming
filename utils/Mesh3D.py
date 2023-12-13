from OpenGL.GL import *
import pygame


class Mesh3D:
    def __init__(self):
        self.vertices = [(0.5, -0.5, 0.5),
                         (-0.5, -0.5, 0.5),
                         (0.5, 0.5, 0.5),
                         (-0.5, 0.5, 0.5),
                         (0.5, 0.5, -0.5),
                         (-0.5, 0.5, -0.5)]
        self.triangles = [0, 2, 3, 0, 3, 1]
        self.draw_type = GL_LINE_LOOP
        self.texture = pygame.image.load()
        self.texID = 0

    def init_texture(self):
        self.texID = glGenTextures(1)
        textureData = pygame.image.tostring(self.texture, "RGB", 1)
        width = self.texture.get_width()
        height = self.texture.get_height()
        glBindTexture(GL_TEXTURE_2D, self.texID)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, 3, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, textureData)

    def draw(self):
        glEnable(GL_TEXTURE_2D)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
        glBindTexture(GL_TEXTURE_2D, self.texID)
        for t in range(0, len(self.triangles), 3):
            glBegin(self.draw_type)
            glTexCoord2fv(self.uvs[self.triangles[t]])
            glVertex3fv(self.vertices[self.triangles[t]])
            glTexCoord2fv(self.uvs[self.triangles[t + 1]])
            glVertex3fv(self.vertices[self.triangles[t + 1]])
            glTexCoord2fv(self.uvs[self.triangles[t + 2]])
            glVertex3fv(self.vertices[self.triangles[t + 2]])
            glEnd()
        glDisable(GL_TEXTURE_2D)


    # def triangle_intersection(self, vertex1, vertex2, vertex3, other_mesh):
    #     epsilon = 1e-5
    #
    #     def calculate_normal(v1, v2, v3):
    #         u = pygame.Vector3(v2[0] - v1[0], v2[1] - v1[1], v2[2] - v1[2])
    #         v = pygame.Vector3(v3[0] - v1[0], v3[1] - v1[1], v3[2] - v1[2])
    #         return pygame.Vector3(u.y * v.z - u.z * v.y, u.z * v.x - u.x * v.z, u.x * v.y - u.y * v.x)
    #
    #     def same_side(p1, p2, a, b):
    #         cp1 = pygame.Vector3.cross(b - a, p1 - a)
    #         cp2 = pygame.Vector3.cross(b - a, p2 - a)
    #         return pygame.Vector3.dot(cp1, cp2) >= 0
    #
    #     def point_in_triangle(point, v1, v2, v3):
    #         b1 = same_side(point, v1, v2, v3)
    #         b2 = same_side(point, v2, v1, v3)
    #         b3 = same_side(point, v3, v1, v2)
    #         return b1 and b2 and b3
    #
    #     ov1, ov2, ov3 = other_mesh.vertices[other_mesh.triangles[:3]]
    #
    #     normal1 = calculate_normal(vertex1, vertex2, vertex3)
    #     normal2 = calculate_normal(ov1, ov2, ov3)
    #
    #     if pygame.Vector3.dot(normal1, normal2) > 1.0 - epsilon:
    #         return False
    #
    #     e1 = vertex2 - vertex1
    #     e2 = vertex3 - vertex1
    #     h = pygame.Vector3.cross(other_mesh.vertices[other_mesh.triangles[0]] - vertex1, normal2)
    #     a = pygame.Vector3.dot(e1, h)
    #
    #     if a > -epsilon and a < epsilon:
    #         return False
    #
    #     f = 1.0 / a
    #     s = other_mesh.vertices[other_mesh.triangles[0]] - vertex1
    #     u = f * pygame.Vector3.dot(s, h)
    #
    #     if u < 0.0 or u > 1.0:
    #         return False
    #
    #     q = pygame.Vector3.cross(s, e1)
    #     v = f * pygame.Vector3.dot(other_mesh.vertices[other_mesh.triangles[0]] - vertex1, q)
    #
    #     if v < 0.0 or u + v > 1.0:
    #         return False
    #
    #     t = f * pygame.Vector3.dot(e2, q)
    #
    #     if t > epsilon:
    #         intersection_point = vertex1 + t * e2
    #
    #         if point_in_triangle(intersection_point, vertex1, vertex2, vertex3) and \
    #                 point_in_triangle(intersection_point, ov1, ov2, ov3):
    #             return True
    #
    #     return False
    #
    # def check_collision(self, other_mesh):
    #     for t1 in range(0, len(self.triangles), 3):
    #         v1 = self.vertices[self.triangles[t1]]
    #         v2 = self.vertices[self.triangles[t1 + 1]]
    #         v3 = self.vertices[self.triangles[t1 + 2]]
    #
    #         for t2 in range(0, len(other_mesh.triangles), 3):
    #             ov1 = other_mesh.vertices[other_mesh.triangles[t2]]
    #             ov2 = other_mesh.vertices[other_mesh.triangles[t2 + 1]]
    #             ov3 = other_mesh.vertices[other_mesh.triangles[t2 + 2]]
    #
    #             if self.triangle_intersection(v1, v2, v3, other_mesh) or \
    #                     self.triangle_intersection(ov1, ov2, ov3, self):
    #                 return True
    #
    #     return False
