# FASTA/FASTQ tools

## Project Overview
This project implements a small, self‑contained bioinformatics pipeline designed to explore key concepts in raw sequencing data analysis. The workflow focuses on three core tasks commonly performed during early‑stage FASTQ quality control: parsing, identifying overrepresented sequences (ORS), and adapter trimming. The aim is not to build a production‑grade tool, but to demonstrate clear biological reasoning, transparent methodology, and an understanding of the limitations inherent in simplified pipelines.

To achieve this, the project uses a combination of synthetic datasets—each tailored to highlight a specific behaviour—and a real biological FASTQ file. Synthetic data allows controlled demonstration of ORS detection, adapter inference, and trimming logic, while the real dataset shows how the pipeline behaves on genuine sequencing reads, including cases where no adapter contamination is present.

The notebooks walk through the full workflow:
- reading and parsing FASTQ files
- identifying overrepresented suffixes as potential adapter candidates
- trimming reads based on the longest matching adapter suffix
- summarising trimming outcomes and reporting detected adapter types

Throughout the analysis, the project emphasises transparency: known issues (such as partial‑adapter trimming inconsistencies) are documented, and the behaviour of the pipeline is interpreted in the context of real sequencing biology. The result is a clear, educational demonstration of how raw read structure can be analysed and processed, and how simplified QC tools behave on both controlled and real‑world data.

-------

## Repository Contents

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

## Synthetic Data Analysis (Analysis_Synthetic_Data)

Here synthetic datasets were used in order to test and demonstrate each tools function since the 'Real' dataset I found didn't contain any adapters. 

The datasets used vary from each tool in order to best highlight their functionality. 

While synthetic datasets are useful in order to test and develop tools, there are known limitations to sythetic generation such as having unrealistic partial adapters - this is an issue I encountered throughout this project. I decided to use these unrealistic, predicatable patterns to my advantage, these limitations and choices are documented in the "Known Issues & Limitations" section later on in the README.



-----------

## Real Data Analysis (Analysis_Real_Data)

The real dataset used in this project is a small subset of Illumina R1 reads taken from a genuine sequencing run. It contains eight reads of typical Illumina length with realistic Phred quality scores and biological sequence structure.

The dataset appears to have undergone prior trimming or QC, as no adapter contamination is present at the read ends. As a result, the ORS (Overrepresented Sequences) module does not detect any repeated suffixes, and the trimming step performs no modifications.

Although the dataset is small and repetitive, it provides a useful demonstration of how the pipeline behaves on real sequencing data, and it highlights the contrast between controlled synthetic examples (where adapters are deliberately introduced) and real-world reads that may already be clean.

Due to its tiny size it does flag normal biological sequences in the overrepresented sequence/Kmer content tables. 

---------

## Methods / Pipeline

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

## Known Issues & Limitations

For the overrepresented sequences & adapter candidate generation I specified the length of the adapters that are in the dataset - I was only able to do this because during generation of the synthetic dataset I specified the adapters and therefore their lengths. Without prior knowledge of the adapter/partial adapter lengths such as in real data this tool would not function correctly. 

Real FastQC use a combination of statistics, alignement and prior knowledge to infer adapters. I simply did not have the time to pour into this project to produce a tool to this level and therefore this level of functionality will suffice for this project.

I am encountering a weird bug with my trimming tool where it trims all three sequences when presented in a manual list but when presented with the list produced from the adapter_candidate generator it only trims one. I have tried to tackle this bug but again, I have run out of time for this project and cannot find whats going on. I expect it might be something to do with which length adapter fragment is first in the list the adapter_candidates script - but I don't have any evidence of this - I will discuss how I would adress these issues if I had more time in the "future improvements" section.

There is also a slight logical issue with the overrepresented sequences & k-mer content tools, both of these require rather large datasets. If a dataset is quite small they will both flag biological sequences as possible adapters.

-------------

## Future Improvements

If more time were available, several enhancements could significantly improve the robustness, accuracy, and biological realism of this pipeline:

1. More sophisticated adapter detection
- Implement fuzzy matching or local alignment (e.g., Smith–Waterman) to detect adapters with mismatches or partial overlaps.
- Incorporate positional bias scoring so that suffixes enriched at the 3′ end are prioritised over biological repeats.
- Add a small database of common Illumina/Nextera/NEBNext adapters to allow known‑adapter matching.

2. Improved handling of partial adapters
- Develop a consensus‑building step to merge overlapping adapter fragments into a reconstructed full adapter.
- Introduce logic to detect and trim partial adapters even when only short fragments are present.
- Add a rule‑based system to choose the correct fragment when multiple candidates overlap.

3. Fixing the trimming inconsistency bug
- Investigate ordering effects in the adapter candidate list (e.g., longest‑first vs shortest‑first).
- Add deterministic sorting of adapter candidates before trimming.
- Write unit tests to isolate cases where manual lists behave differently from generated lists.

4. More realistic ORS and k‑mer analysis
- Expand ORS to analyse full k‑mer positional distributions rather than only suffixes.
- Add minimum dataset size checks to prevent biological sequences being misclassified as adapters.
- Implement statistical enrichment tests to distinguish true technical artefacts from natural sequence repetition.

5. Paired‑end support
- Infer insert sizes from read‑pair overlap.
- Trim adapters based on inferred fragment length rather than suffix matching alone.
- Improve accuracy for datasets with variable insert sizes.
  
6. Better synthetic dataset generation
- Introduce randomised adapter lengths and partial adapters to mimic real contamination patterns.
- Add realistic error models (substitutions, indels, quality drop‑off).
- Generate larger, more diverse datasets to stress‑test ORS and trimming logic.
  
7. Integration with real QC metrics
- Add modules for per‑base quality plots, GC bias, duplication levels, and sequence complexity.
- Provide FastQC‑style summary flags for quick interpretation.
  
8. Packaging and usability improvements
- Convert the pipeline into a small Python package or CLI tool.
- Add argument parsing, logging, and structured output formats (JSON/CSV).
- Improve documentation and add example workflows.

-------

## Installation & Requirements

This project is lightweight and only requires a standard Python environment. The notebooks were developed and tested using:
- Python 3.10+
- Jupyter Notebook / JupyterLab

Required Python packages:
- pandas
- numpy
- matplotlib (optional, only if plotting is added later)
- collections (standard library)
- itertools (standard library)
  
To install the required packages:
-pip install pandas numpy

No external bioinformatics libraries (e.g., Biopython) are required — all parsing and QC logic is implemented manually for transparency and educational value.

------------

## How to Run

1. Clone or download the repository
Place all notebooks, modules, and datasets in the same working directory.

2.Open the notebooks
Launch Jupyter Notebook or JupyterLab and open:
- Analysis_Synthetic_Data.ipynb
- Analysis_Real_Data.ipynb

3. Run the cells sequentially
Each notebook is structured to run top‑to‑bottom without modification.
The synthetic notebook demonstrates each tool individually, while the real‑data notebook shows pipeline behaviour on genuine sequencing reads.

4. Ensure datasets are present
The notebooks expect the following files to be in the working directory:
- Synthetic FASTA/FASTQ files
- R1.fq (real dataset)
- Any files generated by Generate_FastQ
  
5. Review outputs
Each section prints:
- ORS results
- Adapter candidates
- Trimmed sequences
- Trimming reports
- Any relevant tables or summaries
  
No command‑line arguments or configuration files are required — the notebooks are fully self‑contained.


