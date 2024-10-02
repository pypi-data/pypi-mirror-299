# randomness.py
import time
import datetime
import random

def get_true_random():
    """
    Generates an unpredictable random number using real-time data.
    This function uses the current timestamp, seconds, minutes, and other time-based values 
    to create a complex and hard-to-predict randomness.
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
    return abs(random_value % 100)  # Keep the result within the range [0, 100]


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
    """
    random_seed = get_true_random()
    return min_value + (random_seed % (max_value - min_value + 1))


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
