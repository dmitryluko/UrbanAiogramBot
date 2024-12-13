from dataclasses import dataclass, field
from typing import Optional


@dataclass
class User:
    username: str
    email: str
    age: int
    balance: int = 1000
    id: Optional[int] = None
