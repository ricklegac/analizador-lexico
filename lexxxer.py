import ply.lex as lex 
import re 
import codecs 
import os 
import sys
"""
definimos tokens en una lista []
""" 
tokens = ['ID','NUMBER','PLUS','MINUS','TIMES','DIVIDE','ODD',
'ASSIGN','NE','LT','LTE','GT','GTE','LPARENT','RPARENT','COMMA','SEMMICOLOM',
'DOT','UPDATE']
"""
definicion de palabras reservadas en el bnf en un diccionarios
"""
reservadas={
    'begin':'BEGIN',
    'end':'END',
    'if':'IF',
    'then':'THEN',
    'while':'WHILE',
    'do':'DO',
    'call':'CALL',
    'const':'CONST',
    'int':'INT',
    'procedure':'PROCEDURE',
    'out':'OUT',
    'in':'IN',
    'else':'ELSE'

}

tokens = tokens + list(reservadas.values())

t_ignore = '\t' #token que ignoramos 
t_PLUS = r'\+' #expresion regular para la suma, el slash para que detecte que es un simbolo y no el + de la expresion regular 