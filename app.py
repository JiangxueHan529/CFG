import streamlit as st
from nltk import CFG
from PIL import Image
import nltk
from nltk.draw.util import CanvasFrame
import os
import io
import webbrowser
from nltk.draw.tree import TreeView, TreeWidget
from nltk.parse.generate import generate, demo_grammar
wug = Image.open('wugsgiving.png')

def save_tree(tree):
    cf = CanvasFrame()
    tc = TreeWidget(cf.canvas(),tree)
    cf.add_widget(tc,10,10) # (10,10) offsets
    cf.print_to_file('tree.ps')
    cf.destroy()
    os.system('convert tree.ps output.jpg')


st.title("Intro to Syntax Project Demo")
st.image(wug, caption="Thanksgiving has passed, but the wugs welcome you to Jiangxue's project demo !!!",
        use_column_width=True)
st.header("Generating sentences with CFG and Vocabularies")
cfg_vocab = st.sidebar.selectbox("Choose a set of context free grammar with vocabularies", ["long","short"])
text_input = st.text_input("Enter your own set of CFG:")
s = ""
if text_input:
        s = text_input
        # s = """S -> NP VP \n                 NP -> Det N \n                 PP -> P NP \n                 VP -> 'slept' | 'walked' PP| 'saw' NP\n                 Det -> ' the' | 'a' \nN -> 'man' | 'park' | 'dog' \n                 P -> 'in' | 'with'"""
        check = st.checkbox("Show me my set of CFG")
        if check:
                st.write("Your input CFG:", s)
elif cfg_vocab == "long":
        s = """
        S -> NP VP
        S -> Aux NP VP 
        S -> VP
        NP -> Pronoun
        NP -> Proper-Noun
        NP -> Det Nominal
        Aux -> 'does'
        Nominal -> Noun 
        Nominal -> Nominal PP 
        VP -> Verb
        VP -> Verb NP 
        VP -> Verb NP PP
        VP -> Verb PP
        VP -> VP PP
        PP -> Preposition NP
        Preposition -> 'from' | 'to' | 'on' | 'near' | 'through'
        Det -> 'that' | 'this' | 'the' | 'a'
        Proper-Noun -> 'Houston' | 'NWA'
        Noun -> 'book' | 'flight' | 'meal' | 'money'
        Verb -> 'book' | 'include' | 'prefer'
        Pronoun -> 'I' | 'she' | 'me'
        """
        show = st.checkbox("Show me the set of CFG")
        if show:
                st.write("Your chosen set of CFG and vocab:", """\n
        S -> NP VP\n
        S -> Aux NP VP \n
        S -> VP\n
        NP -> Pronoun\n
        NP -> Proper-Noun\n
        NP -> Det Nominal\n
        Aux -> 'does'\n
        Nominal -> Noun \n
        Nominal -> Nominal PP \n
        VP -> Verb\n
        VP -> Verb NP \n
        VP -> Verb NP PP\n
        VP -> Verb PP\n
        VP -> VP PP\n
        PP -> Preposition NP\n
        Preposition -> 'from' | 'to' | 'on' | 'near' | 'through'\n
        Det -> 'that' | 'this' | 'the' | 'a'\n
        Proper-Noun -> 'Houston' | 'NWA'\n
        Noun -> 'book' | 'flight' | 'meal' | 'money'\n
        Verb -> 'book' | 'include' | 'prefer'\n
        Pronoun -> 'I' | 'she' | 'me'\n
        """)

elif cfg_vocab == "short":
        s = """
        S -> NP VP 
        NP -> Det N 
        PP -> P NP 
        VP -> 'slept' | 'walked' PP | 'saw' NP
        Det -> 'the' | 'a' 
        N -> 'man' | 'park' | 'dog' 
        P -> 'in' | 'with'
        """
        show = st.checkbox("Show me the set of CFG")
        if show:
                st.write("Your chosen set of CFG and vocab:", """\n
                S -> NP VP \n
                NP -> Det N \n
                PP -> P NP \n
                VP -> 'slept' | 'walked' PP| 'saw' NP\n
                Det -> 'the' | 'a' \n
                N -> 'man' | 'park' | 'dog' \n
                P -> 'in' | 'with'
                """)

g = CFG.fromstring(s)
parser = nltk.ChartParser(g)

#generate valid sentences from grammar
show_sentences = st.checkbox("Show me all sentences generated by this set of CFG and vocabularies")
if show_sentences:
        for sentence in generate(g):
           st.write((' '.join(sentence)))

st.header("Parsing sentences into tree structures")
user_input =st.text_input("Enter the sentence you would like to parse:")
example_sen = st.sidebar.selectbox("Choose an example sentence to parse", ["does she prefer Houston","I book the flight from Houston to NWA"])
st.write("The sentence you chose is: ", example_sen)
if user_input:
    st.write("The sentence you entered is: ", user_input)
    st.markdown("Please make sure all the words you entered are in the vocabulary you selected.")
    sent = user_input.split()
    st.markdown("This is the parsing of the sentence you entered:")
    for tree in parser.parse(sent):
            st.markdown(tree)
sent = example_sen.split()
st.markdown("This is the parsing of the sentence you selected:")
for tree in parser.parse(sent):
    st.markdown(tree)
if example_sen == "does she prefer Houston":
    img = Image.open('does she prefer houston.png')
    st.image(img, caption = "Syntax tree for sentence 'does she prefer Houston'",  width = 400)
else:
    st.markdown("I'm showing one of the possible parsing's syntax tree")
    img = Image.open('book the flight.png')
    st.image(img, caption="Syntax tree for sentence 'I book the flight from Houston to NWA'", width = 600)



st.markdown("Use this link to create your own tree using the parsing above:")
url = 'http://mshang.ca/syntree/'
if st.button('Open browser'):
    webbrowser.open_new_tab(url)
