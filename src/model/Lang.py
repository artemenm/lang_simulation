from dataclasses import dataclass


@dataclass
class Lang:
    name: str
    is_official: bool

    def __hash__(self):
        return hash(self.name)
