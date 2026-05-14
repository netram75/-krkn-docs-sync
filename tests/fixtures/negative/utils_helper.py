"""Internal utility — not a scenario, should not trigger doc generation."""


def retry(func, attempts=3):
    for i in range(attempts):
        try:
            return func()
        except Exception:
            if i == attempts - 1:
                raise
