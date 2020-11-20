#!/usr/bin/env python

from double_helix_structures import nucleotides

# import C++ modules
from CDoubleHelix.DoubleHelix_transcript import transcript_DNA
from CDoubleHelix.DoubleHelix_revcomp_dna import revcomp_dna
from CDoubleHelix.DoubleHelix_revcomp_rna import revcomp_rna
from CDoubleHelix.DoubleHelix_translate_dna import translate_DNA
from CDoubleHelix.DoubleHelix_translate_rna import translate_RNA

from collections import Counter
import random

class double_helix:

    def __init__(self, seq='ACTG', type='DNA', label='No label'):
        self.seq = seq.upper()
        self.type = type
        self.label = label
        self.valid = self.__check()
        if self.valid is not True:
            raise ValueError('Provide a valid DNA or RNA string')

    def __check(self):
        """Checks if sequence is valid"""
        return set(nucleotides[self.type]).issuperset(self.seq)

    def get_type(self):
        """Returns sequence type (DNA or RNA)"""
        return self.type

    def get_info(self):
        """Returns sequence info"""
        return f"[Label]: {self.label}\n[Type]: {self.type}\n[Length]: {len(self.seq)}"

    def generate_random(self, length=1000, new_type='DNA'):
        """Generates random sequence of a given length"""
        seq = ''.join([random.choice(nucleotides[new_type]) for i in range(length)])
        self.__init__(seq, new_type, label='Random sequence')

    def nucleotide_freq(self):
        """Count of nucleotides in sequence"""
        return dict(Counter(self.seq))

    def transcription(self):
        """DNA transcription --> RNA"""
        if self.type == 'DNA':
            return transcript_DNA(self.seq)
        return 'Not a DNA sequence'

    def rev_complement(self):
        """Returns reverse complement of the sequence"""
        if self.type == 'DNA':
            mapping = str.maketrans('ATCG', 'TAGC')
        else:
            mapping = str.maketrans('AUCG', 'UAGC')
        return self.seq.translate(mapping)[::-1]

    def gc_content(self):
        """Returns GC content percentage"""
        return round((self.seq.count('C') + self.seq.count('G')) / len(self.seq) * 100, 6)

    def gc_k_mer(self, k=20):
        """Returns GC content percengage in k-mer"""
        gc_list = []
        for i in range(0, len(self.seq)-k+1, k):
            k_mer = self.seq[i:i+k]
            res.append(
                round((k_mer.count('C') + k_mer.count('G')) / len(k_mer) * 100, 6)
                )
        return gc_list

    def translate_seq(self, start_position=0):
        '''Translates DNA/RNA sequence into an aminoacid sequence'''
        if self.type == 'DNA':
            return translate_DNA(self.seq)
        elif self.type == 'RNA':
            return translate_RNA(self.seq)

    def aminoacid_codon(self, aminoacid):
        '''Returns percentage of a given aminoacid produced by codons'''
        temp = []
        if self.type == 'DNA':
            for i in range(0, len(self.seq)-2, 3):
                if DNA_Codons[self.seq[i:i+3]] == aminoacid:
                    temp.append(self.seq[i:i+3])
        elif self.type == 'RNA':
            for i in range(0, len(self.seq)-2, 3):
                if RNA_Codons[self.seq[i:i+3]] == aminoacid:
                    temp.append(self.seq[i:i+3])
        freq = dict(Counter(temp))
        total_count = sum(freq.values())
        for i in freq:
            freq[i] = round(freq[i] / total_count, 2)
        return freq

    def open_reading_frames(self):
        """Generates the six open reading frames of DNA"""
        frames = []
        frames.append(self.translate_seq(0))
        frames.append(self.translate_seq(1))
        frames.append(self.translate_seq(2))
        temp_seq = double_helix(self.rev_complement(), self.type)
        frames.append(temp_seq.translate_seq(0))
        frames.append(temp_seq.translate_seq(1))
        frames.append(temp_seq.translate_seq(2))
        del temp_seq
        return frames

    def prot_reading_frames(self, aminoacid_seq):
        '''Returns possible protein between M and Stop'''
        temp_protein = []
        proteins = []
        for i in aminoacid_seq:
            if i == '_':
                # stop appending aminoacids in temp
                if temp_protein:
                    for j in temp_protein:
                        proteins.append(j)
                    temp_protein = []
            else:
                if i == 'M':
                    # start appending aminoacids in temp
                    temp_protein.append('')
                for k in range(len(temp_protein)):
                    temp_protein[k] += i
        return proteins

    def proteins_rf(self, start=0, end=0, ordered=False):
        '''Returns all possible proteins from open reading frames'''
        if end > start:
            tmp_seq = double_helix(self.seq[start:end], self.type)
            reading_frames = tmp_seq.open_reading_frames()
        else:
            reading_frames = self.open_reading_frames()
        proteins_result = []
        for i in reading_frames:
            proteins = self.prot_reading_frames(i)
            for j in proteins:
                proteins_result.append(j)
        if ordered:
            return sorted(proteins_result, key=len, reverse=True)
        else:
            return proteins_result
