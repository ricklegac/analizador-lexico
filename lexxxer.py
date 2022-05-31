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
t_MINUS = r'\-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_ODD = r'ODD'
t_ASSING = r'='
t_NE = r'<>'
t_LT = r'<'
t_LTE = r'<='
t_GT = r'>'
t_GTE = r'>='
t_LPARENT = r'\('
t_RPARENT = r'\)'
t_COMMA = r','
t_SEMMICOLON = r';' 
t_DOT = r'.'
t_UPDATE = r':='

#definicion de los tokens
"""
reconocer cualquier id y retornar para que pueda
ser impreso mas adelante
"""
def t_ID(t):
    #necesitamos una expresion regular mas avanzada para este token
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value.upper() in keywords: 
        t.value = t.value.upper()
        t.type = t.value
    
    return t 
"""
comentario con /* comentario cualquiera *\
no devuelve ningun valor porque no es algo 
que nos interese procesadar 
"""
def t_COMMENT(t):
    r'\/\*(\s*|.*?)*\*\/)|(\/\/.*'
