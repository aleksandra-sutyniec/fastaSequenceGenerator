# Album number: s30621
# Date: 2026-05-11
# Description: Random DNA sequence generator using the FASTA format.

import random


def generate_sequence(length: int) -> str:
    """Returns a random DNA sequence of the specified length."""
    nucleotides = ["A", "C", "G", "T"]
    sequence_parts = []

    for _ in range(length):
        sequence_parts.append(random.choice(nucleotides))

    return "".join(sequence_parts)


def calculate_stats(sequence: str) -> dict:
    """
    Returns a dictionary of sequence statistics.
    Keys: "A", "C", "G", "T" and "GC".
    Values are percentages.
    """
    sequence_length = len(sequence)

    # This protects the function from division by zero.
    if sequence_length == 0:
        return {
            "A": 0.0,
            "C": 0.0,
            "G": 0.0,
            "T": 0.0,
            "GC": 0.0,
        }

    count_a = sequence.count("A")
    count_c = sequence.count("C")
    count_g = sequence.count("G")
    count_t = sequence.count("T")

    return {
        "A": count_a / sequence_length * 100,
        "C": count_c / sequence_length * 100,
        "G": count_g / sequence_length * 100,
        "T": count_t / sequence_length * 100,
        "GC": (count_g + count_c) / sequence_length * 100,
    }

def print_stats(stats: dict, sequence_length: int) -> None:
    """Prints nucleotide statistics in a readable format."""
    print(f"Sequence statistics (n={sequence_length}):")
    print(f"A: {stats['A']:.2f}%")
    print(f"C: {stats['C']:.2f}%")
    print(f"G: {stats['G']:.2f}%")
    print(f"T: {stats['T']:.2f}%")
    print(f"GC-content: {stats['GC']:.2f}%")

def insert_name(sequence: str, name: str) -> str:
    """Inserts a name at a random position in the sequence. Name written in lowercase letters."""
    cleaned_name = name.strip().lower()

    if cleaned_name == "":
        return sequence

    # Position may be at the beginning, inside the sequence, or at the end.
    insertion_position = random.randint(0, len(sequence))

    return (
        sequence[:insertion_position]
        + cleaned_name
        + sequence[insertion_position:]
    )


def format_fasta(seq_id: str, description: str, sequence: str, line_width: int = 80) -> str:
    """Returns a formatted FASTA record as a string."""
    if description:
        header = f">{seq_id} {description}"
    else:
        header = f">{seq_id}"

    sequence_lines = []

    # Split the sequence into fixed-width lines required by the FASTA format.
    for start in range(0, len(sequence), line_width):
        line = sequence[start:start + line_width]
        sequence_lines.append(line)

    return header + "\n" + "\n".join(sequence_lines) + "\n"


def save_text_to_file(file_name: str, text: str) -> None:
    """Saves text content to a file using UTF-8 encoding."""
    with open(file_name, "w", encoding="utf-8") as output_file:
        output_file.write(text)


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

def validate_sequence_id(prompt: str) -> str:
    """Gets a FASTA sequence ID from the user and checks that it contains no whitespace."""
    while True:
        seq_id = input(prompt).strip()

        if not seq_id:
            print("Error: sequence ID cannot be empty.")
            continue

        if any(character.isspace() for character in seq_id):
            print("Error: sequence ID cannot contain whitespace.")
            continue

        return seq_id


def main():
    """Controls the main program flow."""
    print("FASTA DNA sequence generator")

    sequence_length = validate_positive_int("Enter sequence length: ")
    seq_id = validate_sequence_id("Enter sequence ID: ")
    description = input("Enter a description of the sequence: ").strip()
    user_name = input("Enter your name: ")

    # The biological sequence contains only A, C, G and T.
    # The inserted name is only a visual addition in the FASTA output.
    sequence = generate_sequence(sequence_length)
    sequence_with_name = insert_name(sequence, user_name)

    # Statistics are calculated only from the biological sequence.
    stats = calculate_stats(sequence)

    fasta_text = format_fasta(seq_id, description, sequence_with_name)
    output_file_name = f"{seq_id}.fasta"

    save_text_to_file(output_file_name, fasta_text)

    print(f"Sequence saved to file: {output_file_name}")
    print_stats(stats, sequence_length)

if __name__ == "__main__":
    main()