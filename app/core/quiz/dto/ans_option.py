from app.shared import DTO


class AnsOption(DTO):
    name: str
    img: str | None
    file: str | None
    is_correct: bool
