"""Shared datatypes."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Triple:
    x: int
    y: int
    z: int

    def as_tuple(self) -> tuple[int, int, int]:
        return (self.x, self.y, self.z)

    def sorted(self) -> Triple:
        a, b, c = sorted((self.x, self.y, self.z))
        return Triple(a, b, c)


@dataclass(frozen=True)
class Solution:
    n: int
    x: int
    y: int
    z: int
    method: str

    @property
    def triple(self) -> tuple[int, int, int]:
        return (self.x, self.y, self.z)

    def sorted_triple(self) -> tuple[int, int, int]:
        return tuple(sorted(self.triple))
