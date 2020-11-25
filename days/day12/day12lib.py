import re
import struct
import sys

line_re = re.compile(r"^<x=\s*(-?\d+), y=\s*(-?\d+), z=\s*(-?\d+)>$")


def parse_input(text):
    results = []
    for line in text.strip().splitlines():
        line = line.strip()
        match = line_re.fullmatch(line)
        results.append(Moon(int(match[1]), int(match[2]), int(match[3])))
    return results


def sign(n):
    if n < 0:
        return -1
    return 1


class Moon:
    __slots__ = "x", "y", "z", "vx", "vy", "vz"

    def __init__(self, x, y, z, vx=0, vy=0, vz=0):
        self.x, self.y, self.z = x, y, z
        self.vx, self.vy, self.vz = vx, vy, vz

    def apply_velocity(self):
        self.x += self.vx
        self.y += self.vy
        self.z += self.vz

    def total_energy(self):
        return self.potential_energy() * self.kinetic_energy()

    def potential_energy(self):
        return abs(self.x) + abs(self.y) + abs(self.z)

    def kinetic_energy(self):
        return abs(self.vx) + abs(self.vy) + abs(self.vz)

    @property
    def position(self):
        return (self.x, self.y, self.z)

    @property
    def velocity(self):
        return (self.vx, self.vy, self.vz)

    @staticmethod
    def apply_gravity(a, b):
        if a.x != b.x:
            s = sign(a.x - b.x)
            a.vx -= s
            b.vx += s
        if a.y != b.y:
            s = sign(a.y - b.y)
            a.vy -= s
            b.vy += s
        if a.z != b.z:
            s = sign(a.z - b.z)
            a.vz -= s
            b.vz += s

    def __eq__(self, other):
        if not isinstance(other, Moon):
            return NotImplemented
        return self.position == other.position and self.velocity == other.velocity

    def __repr__(self):
        x, y, z = self.position
        vx, vy, vz = self.velocity
        return f"Moon(x={x}, y={y}, z={z}, vx={vx}, vy={vy}, vz={vz})"


def moon_pairs(moons):
    pairs = []
    for i in range(len(moons)):
        for j in range(i + 1, len(moons)):
            pairs.append((moons[i], moons[j]))
    return pairs


def step(moons):
    for a, b in moon_pairs(moons):
        Moon.apply_gravity(a, b)
    for m in moons:
        m.apply_velocity()


def simulate(moons, nsteps):
    energy = 0
    for _ in range(nsteps):
        step(moons)
        energy = sum(map(Moon.total_energy, moons))
    return energy
