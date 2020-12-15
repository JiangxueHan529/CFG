from nltk import CFG
import nltk
import os
from nltk.draw.tree import TreeView, TreeWidget
from nltk.parse.generate import generate, demo_grammar
from nltk.draw.util import CanvasFrame


def save_tree(tree):
    cf = CanvasFrame()
    tc = TreeWidget(cf.canvas(),tree)
    cf.add_widget(tc,10,10) # (10,10) offsets
    cf.print_to_file('tree.ps')
    cf.destroy()
    os.system('convert tree.ps output.png')

s = """
S -> S conj S
S -> NP VP
S -> Aux NP VP 
S -> VP
NP -> Pronoun
NP -> Proper-Noun
NP -> Det Nominal
NP -> NP conj NP
NP_obj -> Proper-Noun
NP_obj -> Det Nominal
NP_obj -> NP conj NP
NP_obj -> Pronoun_obj
Aux -> 'does'
Aux -> PP
Nominal -> Noun 
Nominal -> Nominal conj Nominal
Nominal -> Nominal PP 
VP -> Verb
VP -> Verb NP_obj
VP -> Verb NP_obj PP
VP -> Verb PP
VP -> VP PP
PP -> Preposition Noun
PP -> Preposition Pronoun_obj
Preposition -> 'from' | 'to' | 'on' | 'near' | 'through' | 'with'
Det -> 'that' | 'this' | 'the' | 'a'
Proper-Noun -> 'Houston' | 'NWA'
Noun -> 'book' | 'flight' | 'meal' | 'money' | 'hotel'
Verb -> 'book' | 'include' | 'prefer'
Pronoun -> 'I' | 'she' | 'he' | 'they' 
Pronoun_obj -> 'me' | 'her' | 'him' |'them'
conj -> 'and' | 'or'
"""

g = CFG.fromstring(s)
parser = nltk.ChartParser(g)

#generate valid sentences from grammar
for sentence in generate(g, n=200, depth = 4):
   print(' '.join(sentence))

sent = 'I prefer the hotel'.split()
#print all possible parses of sentence
for tree in parser.parse(sent):
    print(tree)
    tree.draw()
    TreeView(tree)._cframe.print_to_file('output.ps')
    save_tree(tree)
