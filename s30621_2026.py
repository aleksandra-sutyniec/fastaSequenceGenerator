# Album number: s30621
# Date: 2026-05-11
# Description: Random DNA sequence generator using the FASTA format.

import random


def generate_sequence(length: int) -> str:
    """Returns a random DNA sequence of the specified length."""
    return ""


def calculate_stats(sequence: str) -> dict:
    """
    Returns a dictionary of sequence statistics.
    Keys: "A", "C", "G", "T" and "GC".
    Values are percentages.
    """
    return {
        "A": 0.0,
        "C": 0.0,
        "G": 0.0,
        "T": 0.0,
        "GC": 0.0,
    }


def insert_name(sequence: str, name: str) -> str:
    """Inserts a name at a random position in the sequence. Name written in lowercase letters."""
    return sequence


def format_fasta(seq_id: str, description: str, sequence: str, line_width: int = 80) -> str:
    """Returns a formatted FASTA record as a string."""
    return ""


def validate_positive_int(prompt: str, min_val: int = 1, max_val: int = 100_000) -> int:
    """Gets an integer from the user in a range. In case of an error, repeats the question."""
    while True:
        user_value = input(prompt)

        try:
            number = int(user_value)
        except ValueError:
            print(f"Error: value must be an integer in the range [{min_val}, {max_val}].")
            continue

        if min_val <= number <= max_val:
            return number

        print(f"Error: value must be an integer in the range [{min_val}, {max_val}].")


def main():
    """Controls the main program flow."""
    print("FASTA DNA sequence generator")

    sequence_length = validate_positive_int("Enter sequence length: ")

    print(f"Selected sequence length: {sequence_length}")


if __name__ == "__main__":
    main()