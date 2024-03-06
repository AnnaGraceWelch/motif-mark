#!/usr/bin/env python

# Author: Anna Grace Welch

'''This module is a collection of functions useful in bioinformatics.'''

import re

##########################################################################################################
# Constants
##########################################################################################################

DNA_bases = set('ATGCNatcgn')
RNA_bases = set('AUGCNaucgn')

amino_acids = {"UUU":"F", "UUC":"F", "UUA":"L", "UUG":"L",
        "UCU":"S", "UCC":"S", "UCA":"S", "UCG":"S",
        "UAU":"Y", "UAC":"Y", "UAA":"STOP", "UAG":"STOP",
        "UGU":"C", "UGC":"C", "UGA":"STOP", "UGG":"W",
        "CUU":"L", "CUC":"L", "CUA":"L", "CUG":"L",
        "CCU":"P", "CCC":"P", "CCA":"P", "CCG":"P",
        "CAU":"H", "CAC":"H", "CAA":"Q", "CAG":"Q",
        "CGU":"R", "CGC":"R", "CGA":"R", "CGG":"R",
        "AUU":"I", "AUC":"I", "AUA":"I", "AUG":"M",
        "ACU":"T", "ACC":"T", "ACA":"T", "ACG":"T",
        "AAU":"N", "AAC":"N", "AAA":"K", "AAG":"K",
        "AGU":"S", "AGC":"S", "AGA":"R", "AGG":"R",
        "GUU":"V", "GUC":"V", "GUA":"V", "GUG":"V",
        "GCU":"A", "GCC":"A", "GCA":"A", "GCG":"A",
        "GAU":"D", "GAC":"D", "GAA":"E", "GAG":"E",
        "GGU":"G", "GGC":"G", "GGA":"G", "GGG":"G",}


##########################################################################################################
# Functions
##########################################################################################################

def count_DNA_nucleo(dna:str):
    '''This function takes a DNA string as input, and returns the amount of As, Cs, Gs, and Ts.'''
    #initialize dictionary to hold nucleotide counts
    nucleo_count = {'A': 0, 
                    'C': 0,
                    'G': 0,
                    'T': 0}
    #loop through string 
    for c in dna.upper():
        #match to respective nucleotide and increment that count
        match c:
            case 'A':
                nucleo_count['A'] += 1
            case 'G':
                nucleo_count['G'] += 1
            case 'C':
                nucleo_count['C'] += 1
            case 'T':
                nucleo_count['T'] += 1
            case _:
                return 'This is not a valid DNA nucleotide'
    return nucleo_count
    


def all_substrings(seq: str) -> set:
    '''This function takes a DNA sequence and returns a set containing all possible substrings from the DNA sequence.'''
    if len(seq) == 0:
        return 0
    elif len(seq) == 1:
        return seq
    else:
        substrings = {seq[i:j] for i in range(len(seq)) for j in range(i, len(seq))}
    return substrings



def reverse_complement(seq: str):
    '''Takes a string as input. Returns the reverse complement of the DNA or RNA sequence.'''
    rev_comp = ''
    reverse_seq = seq[::-1]
    for base in reverse_seq.upper(): 
        if base == "A":
            rev_comp += 'T'
        elif base == "T":
            rev_comp += 'A'
        elif base == "G":
            rev_comp += 'C'
        elif base == "C":
            rev_comp += 'G'
        else: 
            rev_comp += 'N'
    return rev_comp


def convert_phred(letter: str) -> int:
    '''Converts a single character into a phred score'''
    return ord(letter) - 33

def transcribe_dna(dna:str):
    '''This function takes a DNA string as input and transcribes it to RNA.'''
    rna = ''
    for c in dna.upper():
        if c == 'T':
            rna += 'U'
        else:
            rna += c
    return rna

def translate_rna(rna:str):
    '''Takes a string of an RNA sequence and returns the respective transcribed amino acid for each codon.'''
    matches = re.findall(r"([A|U|C|G]{3})", rna)
    proteins = []
    for match in matches:
        if match in amino_acids:
            if amino_acids[match] != "STOP":
                proteins.append(amino_acids[match])




def qual_score(phred_score: str) -> float:
    '''Takes a string of phred scores, sums them, and returns the average quality score of the string.'''
    phred_sum = 0
    for score in phred_score: 
        phred_sum += convert_phred(score)
    return phred_sum / len(phred_score)


def validate_base_seq(seq, RNAflag=False):
    '''This function takes a string. Returns True if string is composed
    of only As, Ts (or Us if RNAflag), Gs, Cs. False otherwise. Case insensitive.'''
    return set(seq) <= (RNA_bases if RNAflag else DNA_bases)

def gc_content(DNA):
    '''Returns GC content of a DNA or RNA sequence as a decimal between 0 and 1.'''
    DNA = DNA.upper()
    return (DNA.count("G") + DNA.count("C")) / len(DNA)


def oneline_fasta(r_file, w_file):
    '''Takes a FASTA file as input. Removes wrapping from FASTA file to make each sequence only one line. 
    Returns FASTA file as output with only two lines for each read (header and sequence).'''
    header = seq = ''
    with (open(r_file, 'r') as input, open(w_file, 'w') as output):
        for line in input: 
            line = line.strip()
            if line.startswith('>') and header == '':
                header = line
            elif line.startswith('>'):
                    output.write(f'{header}\n{seq}\n')
                    header = line
                    seq = ''
            else:
                    seq += line
        output.write(f'{header}\n{seq}\n')

def calc_median(lst: list):
    '''Takes a sorted list and returns median value.'''
    length = len(lst)
    if len(lst)%2 == 0:
        mid_pos1 = lst[length//2]
        mid_pos2 = lst[length//2 - 1]
        median = (mid_pos1 + mid_pos2)/2
    else: 
        median = lst[length//2]
    return median

