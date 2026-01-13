import random
import string


def generate_string(length):
    """Generatea a random string of specified length"""
    return "".join(random.choices(string.ascii_lowercase, k=length))


def generate_chat_id(num_words, word_length):
    """
    Generate a chat ID with multiple random words joined by dashes.

    Args:
        num_words: How many words to generate (e.g., 3)
        word_length: How long each word should be (e.g., 6)

    Returns:
        A string like 'abcdef-xyzabc-mnopqr'
    """
    words = [generate_string(word_length) for i in range(num_words)]
    return "-".join(words)


print(generate_chat_id(num_words=3, word_length=8))
