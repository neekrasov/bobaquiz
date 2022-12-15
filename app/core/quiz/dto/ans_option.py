from app.shared import DTO


class AnsOptionCreate(DTO):
    name: str
    img: str | None
    file: str | None
    is_correct: bool
