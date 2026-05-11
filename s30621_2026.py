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

def generate_sequence_with_distribution(length: int, weights: list[int]) -> str:
    """Returns a random DNA sequence using user-defined nucleotide percentages."""
    nucleotides = ["A", "C", "G", "T"]
    sequence_parts = []

    for _ in range(length):
        selected_nucleotide = random.choices(nucleotides, weights=weights, k=1)[0]
        sequence_parts.append(selected_nucleotide)

    return "".join(sequence_parts)



def ask_yes_no(prompt: str) -> bool:
    """Asks a yes/no question and returns True for yes or False for no."""
    while True:
        answer = input(prompt).strip().lower()

        if answer in ("y", "yes"):
            return True

        if answer in ("n", "no"):
            return False

        print("Error: enter y/yes or n/no.")


def get_nucleotide_distribution() -> list[int]:
    """
    Gets nucleotide percentages from the user.
    The sum of A, C, G and T percentages must be exactly 100.
    """
    while True:
        print("Enter nucleotide distribution as percentages.")
        percent_a = validate_positive_int("A percentage: ", 0, 100)
        percent_c = validate_positive_int("C percentage: ", 0, 100)
        percent_g = validate_positive_int("G percentage: ", 0, 100)
        percent_t = validate_positive_int("T percentage: ", 0, 100)

        total = percent_a + percent_c + percent_g + percent_t

        if total == 100:
            return [percent_a, percent_c, percent_g, percent_t]

        print("Error: percentages must sum to 100.")


def get_motif_from_user() -> str:
    """Gets a DNA motif from the user and validates that it contains only A, C, G and T."""
    while True:
        motif = input("Enter motif to search for, or leave empty to skip: ").strip().upper()

        if motif == "":
            return ""

        invalid_characters = [character for character in motif if character not in "ACGT"]

        if invalid_characters:
            print("Error: motif can contain only A, C, G and T.")
            continue

        return motif


def find_motif_positions(sequence: str, motif: str) -> list[int]:
    """
    Finds all motif occurrences in the DNA sequence.
    Positions are returned using 1-based biological indexing.
    """
    positions = []

    if motif == "":
        return positions

    start_index = 0

    while True:
        found_index = sequence.find(motif, start_index)

        if found_index == -1:
            break

        # Python indexes from 0, biology usually reports positions from 1.
        positions.append(found_index + 1)

        # Move by one to allow overlapping motifs, for example AAA in AAAAA.
        start_index = found_index + 1

    return positions

def print_motif_results(motif: str, positions: list[int]) -> None:
    """Prints motif search results."""
    if motif == "":
        print("Motif search skipped.")
        return

    if not positions:
        print(f"Motif {motif} was not found in the sequence.")
        return

    joined_positions = ", ".join(str(position) for position in positions)
    print(f"Motif {motif} found at positions: {joined_positions}")



def get_complement(sequence: str) -> str:
    """Returns the complementary DNA strand."""
    complement_table = {
        "A": "T",
        "T": "A",
        "C": "G",
        "G": "C",
    }

    complement_parts = []

    for nucleotide in sequence:
        complement_parts.append(complement_table[nucleotide])

    return "".join(complement_parts)


def get_reverse_complement(sequence: str) -> str:
    """Returns the reverse complementary DNA strand."""
    complement = get_complement(sequence)
    return complement[::-1]


def transcribe_dna_to_mrna(sequence: str) -> str:
    """Returns an mRNA sequence transcribed from the DNA sequence."""
    return sequence.replace("T", "U")


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

    use_custom_distribution = ask_yes_no("Use custom nucleotide distribution? (y/n): ")

    if use_custom_distribution:
        nucleotide_weights = get_nucleotide_distribution()
        sequence = generate_sequence_with_distribution(sequence_length, nucleotide_weights)
    else:
        sequence = generate_sequence(sequence_length)

    motif = get_motif_from_user()
    motif_positions = find_motif_positions(sequence, motif)

    # The inserted name is only a visual addition in the main FASTA record.
    sequence_with_name = insert_name(sequence, user_name)

    # Additional records are calculated from the biological DNA sequence only.
    complement_sequence = get_complement(sequence)
    reverse_complement_sequence = get_reverse_complement(sequence)
    mrna_sequence = transcribe_dna_to_mrna(sequence)

    # Statistics are calculated only from the biological sequence, without the inserted name.
    stats = calculate_stats(sequence)

    fasta_records = [
        format_fasta(seq_id, description, sequence_with_name),
        format_fasta(f"{seq_id}_complement", "complementary strand", complement_sequence),
        format_fasta(f"{seq_id}_reverse_complement", "reverse complementary strand", reverse_complement_sequence),
        format_fasta(f"{seq_id}_mRNA", "transcribed mRNA sequence", mrna_sequence),
    ]

    fasta_text = "".join(fasta_records)
    output_file_name = f"{seq_id}.fasta"

    save_text_to_file(output_file_name, fasta_text)

    print(f"Sequence saved to file: {output_file_name}")
    print_stats(stats, sequence_length)
    print_motif_results(motif, motif_positions)

if __name__ == "__main__":
    main()