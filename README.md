# FASTA-tools
A lightweight Python toolkit for parsing FASTA files, counting nucleotides, computing GC content and visualising sequence composition using Pandas and Matplotlib

-------------

FASTA Tools is a lightweight Python mini‑project for basic sequence analysis, providing simple functions to parse FASTA files, extract nucleotide sequences, count A/T/G/C bases, calculate GC content, and visualise nucleotide composition using Pandas and Matplotlib. It includes a reusable Python parser script, an example FASTA file, and a Jupyter Notebook demonstrating how to load sequences, convert results into a DataFrame, and generate bar plots for exploratory analysis. This project serves as an introductory bioinformatics toolkit and a foundation for future extensions such as multi‑FASTA support, FASTQ parsing, k‑mer counting, ORF finding, and additional QC metrics, while also acting as an early portfolio piece showcasing clean Python workflow, data handling, and visualisation skills

-------------

# FASTQ Tools

This implements a minimal FASTQ quality‑control pipeline, similar to the core functionality of FastQC. The goal is to understand how sequencing quality scores work and how to analyse them programmatically.

Features implemented
- FASTQ parsing (4‑line block structure)
- ASCII → Phred score conversion (ord(char) - 33)
- Handling variable read lengths using NaN padding
- Per‑cycle mean quality calculation using np.nanmean
- FastQC‑style “Mean Quality per Cycle” plot
- Padded quality matrix inspection for debugging
- 
What the pipeline does
- Reads a FASTQ file
- Extracts sequences and quality strings.
- Converts quality strings to Phred scores
- Uses Sanger encoding (Phred+33).
- Pads reads of different lengths
- Ensures all reads align by cycle for per‑cycle analysis.
- Computes per‑cycle mean quality
- Ignores missing values using np.nanmean.
- Plots the mean quality curve
- Shows how sequencing accuracy changes across cycles.
  
Example output
- A line plot showing mean Phred score for each sequencing cycle.
- Early cycles typically show high quality.
- Later cycles may drop due to chemistry degradation or shorter reads.

----------------------------------
