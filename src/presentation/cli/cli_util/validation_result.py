from dataclasses import dataclass
from typing import List


@dataclass
class CliValidationResult:
    is_ダメ: bool
    messages: List[str]
