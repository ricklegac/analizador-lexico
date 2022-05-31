import ply.lex as lex 
import re 
import codecs 
import os 
import sys

tokens = ['ID','NUMBER','PLUS','MINUS','TIMES','DIVIDE','ODD',
'ASSIGN','NE','LT','LTE','GT','GTE','LPARENT','RPARENT','COMMA','SEMMICOLOM',
'DOT','UPDATE']
"""
definimos tokens en una lista []
"""