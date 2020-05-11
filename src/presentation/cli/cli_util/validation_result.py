from dataclasses import dataclass
from typing import List


@dataclass
class CliValidationResult:
    messages: List[str]

    def display_messages(self) -> None:
        for message in self.messages:
            print(message)

    def is_ダメ(self) -> bool:
        return len(self.messages) > 0
