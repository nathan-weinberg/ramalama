import argparse
from ramalama.stack import Stack
from typing import Callable

class StackFactory:

    def __init__(
        self,
        distro: str,
        args: argparse,
    ):
        self.distro = distro
        self.create: Callable[[], Stack]

    def create(self) -> Stack:
        stack = Stack(self.distro)
        return stack
