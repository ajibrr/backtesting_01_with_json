def greater_than_all_previous(current, previous_values):
    if current is None or not previous_values or any(v is None for v in previous_values):
        return False
    return all(current > v for v in previous_values)

def absolute_greater_than_all_previous(current, previous_values):
    if current is None or not previous_values or any(v is None for v in previous_values):
        return False
    return all(abs(current) > abs(v) for v in previous_values)
