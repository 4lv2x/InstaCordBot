from random import choice, randint

def get_response(user_input: str) -> str:
    lowered: str = user_input.lower()

    if lowered == "roll a dice":
        return f"You rolled a {randint(1, 6)}"
    elif lowered == "flip a coin":
        return choice(["Heads", "Tails"])
    elif lowered == "roll a d20":
        return f"You rolled a {randint(1, 20)}!"
    elif lowered == "rickroll":
        return "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    else:
        return "Invalid input."
