def parse_fastq(filepath):
    sequences =[]
    qualities = []

    with open(filepath,"r") as f:
        while True:
            header = f.readline().strip()
            if not header:
                break


            seq = f.readline().strip()
            plus = f.readline().strip()
            qual = f.readline().strip()

            sequences.append(seq)
            qualities.append(qual)

    return sequences, qualities

def phred_scores(quality_string):
    return [ord(char)-33 for char in quality_string]

