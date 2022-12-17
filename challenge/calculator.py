class Calculator:
    def __init__(self, *exceptions) -> None:
        self.exceptions = exceptions
        self.error = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type in self.exceptions:
            self.error = exc_type
            return True
