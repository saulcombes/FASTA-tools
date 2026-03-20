from itertools import zip_longest
from collections import Counter
import pandas as pd

def read_length_distribution(sequences):
    seqlen = []
    for line in sequences:
        seqlen.append(len(line))

    return seqlen

def n_content_per_cycle(sequences):
    padded = list(zip_longest(*sequences, fillvalue="N"))
    n_percentages = []

    for cycle in padded:
        total = len(cycle)
        n_count = cycle.count("N")
        n_percent = (n_count / total) * 100
        n_percentages.append(n_percent)

    return n_percentages

def overrepresented_sequences(sequences):
    counts = Counter(sequences)
    print("")
    most_common = counts.most_common(5)
    calcs1 = []
    dfresults = []
    for item,number in most_common:
        calc = (number/len(sequences))*100
        calcs1 = {item:calc}
        dfresults.append(calcs1)
        if calc >= 3:
            print(item,"= Likely adapter contamination")
        elif calc >= 0.8:
            print(item, "= Possible PCR duplicate")
        elif calc <= 0.1:
            break
        else:
            print("Error")
    
    dfresman = [(list(d.keys())[0], list(d.values())[0]) for d in dfresults]
    print("")
    df = pd.DataFrame(dfresman,columns=["Sequence", "Percentage Incidence"])
    df.index = df.index +1
    df = df.reset_index().rename(columns={"index": "Rank"})
    print(df.to_string(index=False))

def k_mer_content(sequences):
    kmers = []
    for line in sequences:
        end = len(line) - 4
        x=0
        y=5
        kmers.append(line[x:y])
        while True:
          x += 1
          y += 1 
          if x == end:
              break
          kmers.append(line[x:y])
    
    counts = Counter(kmers)
    return counts, kmers

##ACGTACGTACGT

        



