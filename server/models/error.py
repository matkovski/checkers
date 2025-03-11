from typing import List
from pydantic import BaseModel

class Error(BaseModel):
    errors: List[str]

    def merge(self, error):
        self.errors += error.errors