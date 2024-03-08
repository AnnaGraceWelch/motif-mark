#!/usr/bin/env python

# Author: Anna Grace Welch
# Date: 03/07/2024

'''This script takes a FASTA file with sequences (less than or equal to 1000 bases) and a text with one motif (less than or equal to 10 bases) per line
and outputs a .png image diagramming location of specific motifs in file as well as introns and exons.'''

from __future__ import annotations
import argparse
import cairo
import re
from bioinfo_functions import oneline_fasta

###################################################################################################################################################################################################################
#Classes
###################################################################################################################################################################################################################

class Transcript:
    def __init__(self, sequence: Read, count, motifs):
        '''This method initializes a class object with a sequence read (header and sequence), a count, and list of motifs as attributes.'''
        self.sequence = sequence
        self.count = count
        self.motifs = motifs
    def find_motifs(self): 
        '''This searches the FASTA file sequences for instances of a motif. 
        It accounts for overlapping and ambiguous motifs found.'''
                # motifs[line.upper()] = {'regex': m, 'position': []}
        for motif in self.motifs:
            regex = rf'(?=({motif.regex}))'
            if match := list(re.finditer(regex, self.sequence.sequence.upper())):
                positions = [m.start() for m in match]
                motif.get_position(positions)
            else:
                motif.get_position(None)

    def find_exon(self):
        '''This method finds the location of the exon in the transcript's sequence and stores it as an exon attribute.'''
        res = [idx for idx in range(len(self.sequence.sequence)) if self.sequence.sequence[idx].isupper()]
        exon = Exon(res[0], (res[-1] - res[0]))
        self.exon = exon


            
class Read:
    def __init__(self, header):
        '''This method initializes a Read class object with a header as an attribute.'''
        self.header = header
    def get_sequence(self, sequence):
        '''This method adds the sequence and sequence length to the Read object as attributes.
        It also adds a label attribute which is an f string of the header and the length of sequence.'''
        self.sequence = sequence
        self.length = len(sequence)
        self.label = f'{self.header} ({self.length} bases)'



class Motif:
    def __init__(self, sequence, regex, length, color, count):
        '''This method initializes a Motif class object with a sequence, regular expression, length, and color as attributes.'''
        self.sequence = sequence
        self.regex = regex
        self.length = length
        self.color = color
        self.count = count
    def __iter__(self):
        '''Returns an iterator for the Motif class object, allowing these objects to be iterated over.'''
        return self
    def get_position(self, position):
        '''Assigns the start position of a Motif as an attribute of the object.'''
        self.position = position

       

class Exon:
    def __init__(self, position, length):
        '''Initializes an Exon class object with a position and length as attributes.'''
        self.position = position
        self.length = length


class Image:
    def __init__(self, title):
        '''Initializes an Image class object.'''
        self.surface = cairo.SVGSurface(f'{title}.svg', 1100, 1100)
        self.context = cairo.Context(self.surface)
        self.title = title
        
        #set background color as white
        self.context.save()
        self.context.set_source_rgb(1, 1, 1)
        self.context.paint()
        self.context.restore()
    

    def write_title(self):
        '''Writes the title of the Image onto the surface.'''
        self.context.set_source_rgb(0, 0, 0)
        self.context.set_font_size(40)
        self.context.select_font_face('Arial')
        self.context.move_to(100, 75)
        self.context.show_text(self.title)

    def draw_sequence(self, transcript: Transcript):
        '''Assigns a transcript as an attribute of the Image object and draws the sequence of the transcript onto the image along with the header of the sequence as a label.'''
        self.transcript = transcript
        
        #draw sequence
        self.context.set_line_width(10)
        self.context.set_source_rgb(0, 0, 0)
        self.context.rectangle(100, self.transcript.count * 200, len(self.transcript.sequence.sequence), 1)
        self.context.stroke()
        self.context.save()

        #write label/header of sequence
        self.context.set_source_rgb(0, 0, 0)
        self.context.set_font_size(25)
        self.context.select_font_face('Arial')
        self.context.move_to(100, (self.transcript.count * 200) - 30)
        self.context.show_text(self.transcript.sequence.label)
         
    def draw_legend(self):
        '''Draws the legend of the Image object denoting which Motif sequences correspond to which colors drawn on the transcript's sequence.'''
        count = 1
        #draw legend for motifs
        for motif in self.transcript.motifs:
            self.context.set_source_rgb(*motif.color)
            self.context.rectangle(825, 20 * (count * 2), 10, 10)
            self.context.fill()
            self.context.stroke()
            
            self.context.move_to(850, 20 * (count * 2) + 10)
            self.context.set_source_rgb(0, 0, 0)
            self.context.set_font_size(30)
            self.context.show_text(motif.sequence)
            count += 1
        #draw legend for exon
        self.context.set_source_rgb(0, 0, 0)
        self.context.rectangle(825, 20 * (count * 2), 10, 10)
        self.context.fill()
        self.context.stroke()

        self.context.rectangle(820, 20 * (count * 2) + 10, 20, 5)
        self.context.fill()
        self.context.stroke()

        self.context.move_to(850, 20 * (count * 2) + 10)
        self.context.set_font_size(30)
        self.context.show_text('Exon')
        count += 1

        #draw legend for intron
        self.context.rectangle(820, 20 * (count * 2) + 10, 20, 5)
        self.context.fill()
        self.context.stroke()

        self.context.move_to(850, 20 * (count * 2) + 10)
        self.context.set_font_size(30)
        self.context.show_text('Intron')

    def draw_exon(self):
        '''Draws the Exon object on the correct position of the sequence in the Image.'''
        self.context.rectangle(self.transcript.exon.position + 100, self.transcript.count * 200 - 10, self.transcript.exon.length, 10)
        self.context.stroke()



    def draw_motifs(self):
        '''Draws the Motif objects onto the correct positions of the sequence of the transcript in the Image.'''
        for motif in self.transcript.motifs:
            self.context.set_source_rgb(*motif.color)
            if motif.position != None:
                for position in motif.position: 
                    self.context.set_line_width(motif.length)
                    self.context.move_to(position + 100, self.transcript.count * 200 + 5)
                    self.context.line_to(position + 100, self.transcript.count * 200 + 25)
                    self.context.stroke()
                    self.context.save()

        

    def write_to_png(self, title):
        '''Writes the Image to a .png file.'''
        self.surface.write_to_png(f'{title}.png')


    
    
###################################################################################################################################################################################################################
#Functions
###################################################################################################################################################################################################################       
        
    


def get_args():
    '''This function parses the command line arguments inputting FASTA file and motifs file.'''
    parser = argparse.ArgumentParser(description='This program takes a FASTA file and a text file with motifs and returns a png image diagramming the location of motifs, introns, and exons on the sequence')
    parser.add_argument('-f', '--fasta_file', help='What is the name of the FASTA file?')
    parser.add_argument('-m', '--motifs_file', help='What is the name of the file with motifs?')
    return parser.parse_args()

def load_motifs(motif_file):
    '''This function parses the motif file inputted, and creates motif objects contaning a regex, length, and count attribute for each motif in the file.'''
    degenerate_bases = {
    'A': '[A]',
    'C': '[C]',
    'G': '[G]',
    'T': '[TU]',
    'U': '[UT]',
    'W': '[ATU]',
    'S': '[CG]',
    'M': '[AC]',
    'K': '[GTU]',
    'R': '[AG]',
    'Y': '[CTU]',
    'B': '[CGTU]',
    'D': '[AGTU]',
    'H': '[ACTU]',
    'V': '[ACGU]',
    'N': '[ACGTU]'}

    colors = {
        1: (1, 0, 0),   #Red
        2: (0, 1, 0),   #Green
        3: (0, 0, 1),   #Blue
        4: (0, .75, 1), #Light Blue
        5: (1, 0, 1)    #Pink
    }
    motifs = []
    with open(motif_file) as file:
        count = 0
        for line in file:
            count += 1
            line = line.strip()
            m = ''
            for c in line:
                c = c.upper()
                c = degenerate_bases[c]
                m = m + c
            motif = Motif(line, m, len(line), colors[count], count)
            motifs.append(motif)
        return motifs


###################################################################################################################################################################################################################       

def main():

    args = get_args()

    #convert input FASTA file so each read is two lines: header and sequence
    oneline_fasta(args.fasta_file, f'{args.fasta_file}.oneline')

    match = re.search(r'\/(.+?)\.[^\.]+$', args.fasta_file)
    title = match.group(1)

    motifs = load_motifs(args.motifs_file)
    image = Image(title)

    with open(f'{args.fasta_file}.oneline') as input:
        count = 0
        for line in input:
            line = line.strip()
            if line.startswith('>'):
                header = re.search(r'\>(\S+)\s\S+(?:\(.+\))?', line)
                sequence = Read(header.group(1))
                
            else: 
                count += 1
                sequence.get_sequence(line)
                transcript = Transcript(sequence, count, motifs)
                transcript.find_motifs()
                transcript.find_exon()
                image.draw_sequence(transcript)
                image.draw_exon()
                image.draw_motifs()
                        

            
    image.draw_legend()
    image.write_title()
    image.write_to_png(title)
        


if __name__ == '__main__':
    main()



