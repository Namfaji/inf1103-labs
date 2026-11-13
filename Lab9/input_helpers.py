"""Input helpers that keep asking until the user gives a valid value (Section 5.1)."""


def get_positive_float(prompt: str) -> float:
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("Please enter a number greater than zero.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number, e.g. 12.50")


def get_non_negative_float(prompt: str) -> float:
    while True:
        try:
            value = float(input(prompt))
            if value < 0:
                print("Please enter a number that is zero or more.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number, e.g. 2.5")


def get_non_negative_int(prompt: str) -> int:
    while True:
        try:
            value = int(input(prompt))
            if value < 0:
                print("Please enter a whole number that is zero or more.")
                continue
            return value
        except ValueError:
            print("Please enter a whole number, e.g. 10")


def get_non_empty_text(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("This cannot be empty.")


def get_choice(prompt: str, choices: tuple[str, ...]) -> str:
    while True:
        value = input(prompt).strip()
        if value in choices:
            return value
        print(f"Please enter one of: {', '.join(choices)}")
