# randomness.py
import time
import datetime
import random

def get_true_random(min_value=None, max_value=None):
    """
    Generates an unpredictable random number using real-time data within a user-defined range.
    This function uses the current timestamp, seconds, minutes, and other time-based values 
    to create a complex and hard-to-predict randomness.
    
    Args:
        min_value (int): Minimum value of the desired random number.
        max_value (int): Maximum value of the desired random number.
    
    Returns:
        int: A random integer within the specified range [min_value, max_value].
    """
    current_time = time.time()  # Current timestamp
    now = datetime.datetime.now()

    # Extracting time details
    seconds = now.second  # Current seconds
    milliseconds = int((current_time - int(current_time)) * 1000)  # Current milliseconds
    minute = now.minute  # Current minutes
    hour = now.hour  # Current hour

    # Complex random value using a combination of time-based values
    random_value = (milliseconds * seconds + hour) - minute
    if not min_value and not max_value:
        return abs(random_value % 100)
    else:
        abs_random_value = abs(random_value)  # Take absolute value to avoid negatives

        # Map the random value to the desired range [min_value, max_value]
        range_size = max_value - min_value + 1
        return min_value + (abs_random_value % range_size)



def get_time_based_random():
    """
    Creates a time-based complex random value.
    Combines the current second and microsecond values to form a pseudo-random number.
    """
    current_time = time.time()
    seconds = int(current_time % 60)  # Get seconds
    microseconds = int((current_time * 1000000) % 1000)  # Get microseconds

    return (seconds * microseconds) % 100  # Create an unpredictable random value


def randint(min_value, max_value):
    """
    Returns a random integer between min_value and max_value, inclusive.

    Args:
        min_value (int): Minimum value for the random number. Must be an integer greater than or equal to 0.
        max_value (int): Maximum value for the random number. Must be an integer greater than min_value.

    Returns:
        int: A random integer between min_value and max_value.
    """

    if not isinstance(min_value, int):
        raise ValueError(f"Invalid input for `min_value`: Expected an integer, got {type(min_value).__name__}.")
    if not isinstance(max_value, int):
        raise ValueError(f"Invalid input for `max_value`: Expected an integer, got {type(max_value).__name__}.")
    if max_value < min_value:
        raise ValueError(f"Invalid range: `max_value` ({max_value}) cannot be less than `min_value` ({min_value}).")

    return get_true_random(min_value, max_value)


def choice(sequence):
    """
    Returns a random element from the given sequence.
    """
    if not sequence:
        raise IndexError("Cannot choose from an empty sequence.")
    random_index = get_true_random() % len(sequence)
    return sequence[random_index]


def shuffle(sequence):
    """
    Shuffles the given list in place.
    """
    n = len(sequence)
    for i in range(n - 1, 0, -1):
        j = randint(0, i)
        sequence[i], sequence[j] = sequence[j], sequence[i]
    return sequence


def sample(sequence, k):
    """
    Returns a list of k unique random elements from the sequence.
    """
    if k > len(sequence):
        raise ValueError("Sample size cannot exceed sequence length.")
    selected_indices = set()
    result = []

    while len(result) < k:
        random_index = randint(0, len(sequence) - 1)
        if random_index not in selected_indices:
            result.append(sequence[random_index])
            selected_indices.add(random_index)
    return result
