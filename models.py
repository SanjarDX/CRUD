from typing import Optional

from pydantic import BaseModel


class TaskIn(BaseModel):
    title: str = ""
    done: bool = False


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None
