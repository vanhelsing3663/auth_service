class ItemDataConflict(Exception):
    default_message = "Base exception"

    def __init__(
        self, message: str = None, detail: str = None, cause_entity: str = None
    ):
        super().__init__()
        self.message = message or self.default_message
        self.detail = detail
        self.cause_entity = cause_entity
