def format_percentage(value):
    if not isinstance(value, (int, float)):
        return "0.0%"
    percentage = value
    formatted_percentage = f"{percentage:.0f}"
    return f"{formatted_percentage}%"
