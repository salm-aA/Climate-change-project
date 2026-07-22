"""Input validation helpers for the cinema application."""


def validate_customer_name(name):
    """Return a cleaned customer name or raise ValueError."""
    cleaned = name.strip()
    if len(cleaned) < 2:
        raise ValueError("Please enter a name containing at least two characters.")
    if len(cleaned) > 60:
        raise ValueError("The customer name must be 60 characters or fewer.")
    return cleaned


def validate_ticket_count(value):
    """Return a valid ticket count between 1 and 10."""
    try:
        tickets = int(value)
    except (TypeError, ValueError) as error:
        raise ValueError("The number of tickets must be a whole number.") from error
    if tickets < 1 or tickets > 10:
        raise ValueError("You can book between 1 and 10 tickets at a time.")
    return tickets
