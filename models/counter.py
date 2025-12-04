from beanie import Document

class Counter(Document):
    id: str  # Имя счетчика (например, "event_id")
    sequence_value: int  # Текущее значение

    class Settings:
        name = "counters"
