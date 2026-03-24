## FASTA/FASTQ tools

# Project Overview
This project implements a small, self‑contained bioinformatics pipeline designed to explore key concepts in raw sequencing data analysis. The workflow focuses on three core tasks commonly performed during early‑stage FASTQ quality control: parsing, identifying overrepresented sequences (ORS), and adapter trimming. The aim is not to build a production‑grade tool, but to demonstrate clear biological reasoning, transparent methodology, and an understanding of the limitations inherent in simplified pipelines.

To achieve this, the project uses a combination of synthetic datasets—each tailored to highlight a specific behaviour—and a real biological FASTQ file. Synthetic data allows controlled demonstration of ORS detection, adapter inference, and trimming logic, while the real dataset shows how the pipeline behaves on genuine sequencing reads, including cases where no adapter contamination is present.

The notebooks walk through the full workflow:
- reading and parsing FASTQ files
- identifying overrepresented suffixes as potential adapter candidates
- trimming reads based on the longest matching adapter suffix
- summarising trimming outcomes and reporting detected adapter types

Throughout the analysis, the project emphasises transparency: known issues (such as partial‑adapter trimming inconsistencies) are documented, and the behaviour of the pipeline is interpreted in the context of real sequencing biology. The result is a clear, educational demonstration of how raw read structure can be analysed and processed, and how simplified QC tools behave on both controlled and real‑world data.

-------

# Repository Contents

Notebooks:
- Analysis_Real_Data, this notebook contains analysis on a small, seemingly real, biological dataset (R1.fq)
- Analysis_Synthetic_Data, this notebook contains analysis on a set of differing synthetic datasets, the aim of this notebook is to demonstrate the function of each tool/piece of code.

Python Modules:
- fasta_parser, multifasta_parser & fastq_parser - all mainly used to contain the parsing function for their respective data forms. Some however, (namely fastq_parser) contain a couple other QC functions such as GC content, Base composition calculations etc.
- read_structure_content_biases - this is the main module containing all of the analysis functions

Datasets:
- test_sequence.fasta, test_sequence.fastq, test_sequence2.fastq, testdata_10000.fastq - These are all synthetic datasets - the first three were generated for me by Microsoft Copilot while the last one was written using Generate_FastQ
- R1.fq - this is the real sequence, I borrowed this from another fastq toolset I found online (So it might not be real, but it does portray the hallmarks of a biological dataset)

Helper Scripts:
- Generate_FastQ - This script was written to generate a much larger dataset with adapters in order to test the adapter_candidate & analysis functions

----------

# Synthetic Data Analysis (Analysis_Synthetic_Data)

Here synthetic datasets were used in order to test and demonstrate each tools function since the 'Real' dataset I found didn't contain any adapters. 

The datasets used vary from each tool in order to best highlight their functionality. 

While synthetic datasets are useful in order to test and develop tools, there are known limitations to sythetic generation such as having unrealistic partial adapters - this is an issue I encountered throughout this project. I decided to use these unrealistic, predicatable patterns to my advantage, these limitations and choices are documented in the "Known Issues & Limitations" section later on in the README.

-----------

# Real Data Analysis (Analysis_Real_Data)

The real dataset used in this project is a small subset of Illumina R1 reads taken from a genuine sequencing run. It contains eight reads of typical Illumina length with realistic Phred quality scores and biological sequence structure.

The dataset appears to have undergone prior trimming or QC, as no adapter contamination is present at the read ends. As a result, the ORS (Overrepresented Sequences) module does not detect any repeated suffixes, and the trimming step performs no modifications.

Although the dataset is small and repetitive, it provides a useful demonstration of how the pipeline behaves on real sequencing data, and it highlights the contrast between controlled synthetic examples (where adapters are deliberately introduced) and real-world reads that may already be clean.

---------

# Methods / Pipeline

This project implements a lightweight sequencing‑read processing pipeline that mirrors the early stages of FASTQ quality control. The workflow is intentionally simple and transparent, focusing on core concepts rather than production‑grade optimisation. The pipeline consists of four main components:

1. FASTQ Parsing
- Reads are loaded from a standard FASTQ file.
- The parser extracts:
- the nucleotide sequence
- the corresponding Phred quality string
- Output is stored as two parallel lists (seqs and quals) for downstream analysis.
- This step ensures the pipeline can operate on both synthetic and real datasets without modification.

2. Overrepresented Sequence (ORS) Detection
- ORS analysis identifies short sequence suffixes that appear more frequently than expected across the dataset.
- The method focuses on suffixes (e.g., 12‑mers, 10‑mers, 8‑mers), as adapter contamination typically occurs at the end of reads.
- For each suffix length:
- the final k bases of every read are extracted
- frequencies are counted
- any suffix exceeding a minimum incidence threshold is flagged as “overrepresented”
- These overrepresented suffixes form the adapter candidate list.
- This approach mirrors the logic used by tools like FastQC, but in a simplified and transparent form.

3. Adapter Trimming
- Reads are scanned for the presence of any adapter candidate at their 3′ end.
- Trimming follows a longest‑match‑wins rule:
- if multiple candidates match a read’s suffix, the longest one is removed
- Both the sequence and its quality string are trimmed to maintain alignment.
- The trimming step outputs:
- trimmed sequences
- trimmed quality strings
- number of bases removed per read

4. Trimming Report
After processing, the pipeline generates a concise summary including:
- total number of reads
- number of reads trimmed
- total bases removed
- unique adapter types detected
- average number of bases trimmed per trimmed read
This report provides a quick overview of dataset cleanliness and trimming behaviour.

5. Synthetic vs Real Data Behaviour
- Synthetic datasets are used to demonstrate each component of the pipeline in isolation (ORS detection, trimming, k‑mer behaviour).
- The real FASTQ dataset illustrates how the pipeline behaves on genuine sequencing reads, including cases where:
- no adapter contamination is present
- ORS returns no candidates
- trimming performs no modifications
- This contrast highlights both the strengths and limitations of simplified QC logic

-------------

# Known Issues & Limitations

For the overrepresented sequences & adapter candidate generation I specified the length of the adapters that are in the dataset - I was only able to do this because during generation of the synthetic dataset I specified the adapters and therefore their lengths. Without prior knowledge of the adapter/partial adapter lengths such as in real data this tool would not function correctly. 

Real FastQC use a combination of statistics, alignement and prior knowledge to infer adapters. I simply did not have the time to pour into this project to produce a tool to this level and therefore this level of functionality will suffice for this project.
