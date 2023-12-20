import pygame
import math
from .Mesh3D import *
from .MathOGL import cross_product, dot_product


class Sphere(Mesh3D):
    def __init__(self, draw_type, back_face_cull=False, radius=0.5, num_segments=16):
        self.radius = radius
        self.num_segments = num_segments
        self.vertices = self.generate_vertices()
        self.triangles = self.generate_triangles()
        self.uvs = self.generate_uvs()
        self.draw_type = draw_type
        self.back_face_cull = back_face_cull
        Mesh3D.draw_type = draw_type
        self.faceNormals = []
        self.velocity = (0, 0, 0)

        for t in range(0, len(self.triangles), 3):
            p1 = self.vertices[self.triangles[t]]
            p2 = self.vertices[self.triangles[t + 1]]
            p3 = self.vertices[self.triangles[t + 2]]

            u = pygame.Vector3(p1[0] - p2[0],
                               p1[1] - p2[1],
                               p1[2] - p2[2])

            v = pygame.Vector3(p3[0] - p2[0],
                               p3[1] - p2[1],
                               p3[2] - p2[2])

            norm = cross_product(u, v)
            self.faceNormals.append(norm)

    def generate_vertices(self):
        vertices = []
        for i in range(self.num_segments):
            phi = i * 2 * math.pi / self.num_segments
            for j in range(self.num_segments):
                theta = j * math.pi / (self.num_segments - 1)
                x = self.radius * math.sin(theta) * math.cos(phi)
                y = self.radius * math.sin(theta) * math.sin(phi)
                z = self.radius * math.cos(theta)
                vertices.append((x, y, z))
        return vertices

    def generate_triangles(self):
        triangles = []
        for i in range(self.num_segments - 1):
            for j in range(self.num_segments - 1):
                p1 = i * self.num_segments + j
                p2 = p1 + 1
                p3 = (i + 1) * self.num_segments + j
                p4 = p3 + 1
                triangles.extend([p1, p3, p2, p2, p3, p4])
        return triangles

    def generate_uvs(self):
        uvs = []
        for i in range(self.num_segments):
            for j in range(self.num_segments):
                u = i / (self.num_segments - 1)
                v = j / (self.num_segments - 1)
                uvs.append((u, v))
        return uvs

    def draw(self, forward):
        glEnable(GL_TEXTURE_2D)
        # glBegin(self.draw_type)
        # glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
        # glBindTexture(GL_TEXTURE_2D, self.texID)
        for t in range(0, len(self.triangles), 3):
            glBegin(self.draw_type)
            if self.back_face_cull:
                if dot_product(self.faceNormals[t // 3], forward) <= 0:
                    glTexCoord2fv(self.uvs[self.triangles[t]])
                    glVertex3fv(self.vertices[self.triangles[t]])

                    glTexCoord2fv(self.uvs[self.triangles[t + 1]])
                    glVertex3fv(self.vertices[self.triangles[t + 1]])

                    glTexCoord2fv(self.uvs[self.triangles[t + 2]])
                    glVertex3fv(self.vertices[self.triangles[t + 2]])
            else:
                glTexCoord2fv(self.uvs[self.triangles[t]])
                glVertex3fv(self.vertices[self.triangles[t]])

                glTexCoord2fv(self.uvs[self.triangles[t + 1]])
                glVertex3fv(self.vertices[self.triangles[t + 1]])

                glTexCoord2fv(self.uvs[self.triangles[t + 2]])
                glVertex3fv(self.vertices[self.triangles[t + 2]])
            glEnd()
        # glDisable(GL_TEXTURE_2D)
