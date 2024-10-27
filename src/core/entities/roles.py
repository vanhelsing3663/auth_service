from dataclasses import dataclass


@dataclass
class UserRole:
    id: int
    service: str
    role: str

    @classmethod
    def create(cls, service: str, role: str):
        return cls(id=None, service=service, role=role)
