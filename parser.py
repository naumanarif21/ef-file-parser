"""
    Parse EF file to csv/xls
    keeping some parameters
    Date: 11/08/2020
    Author: S@m Sep!0L
"""
import pprint
from pyparsing import (
    Word, Literal, Forward, Group,
    ZeroOrMore, alphas, Suppress, Regex, 
    OneOrMore, alphanums, printables,
    oneOf
)

file_path = 'ef_files/1_EXT_Display_operational_configuration.ef'


def extract_fcid_from_entry(entry):
    """
        Takes an ef Entry and
        scrapes the FCL_ID from the 
        code.
        procedure: indexing and find magic.
    """
    assert entry is not None

    # get the first { index
    first_curly_index = entry.find('{')
    text_till_first_curly_index = entry[0:first_curly_index]
    
    # get the FCL_ID between the last underscore and first {
    FCL_ID = text_till_first_curly_index[text_till_first_curly_index.rfind('_') + 1: first_curly_index]
    return FCL_ID

def magic_parser(text):
    """
        Use a Grammar Based Parser
        to take out shit
    """
    EQ, LBRACE, RBRACE = map(Suppress,':{}')
    name = Word(alphas + '_ ')
    value = Forward()
    entry = Group(name + EQ + value)
    
    struct = Group(LBRACE + ZeroOrMore(entry) + RBRACE)
    value << (OneOrMore(Word(alphanums + '".,-_')) | OneOrMore(Group(LBRACE + OneOrMore(Word(alphanums + '".,-_')) + RBRACE)))

    result = struct.parseString(text)
    pprint.pprint(result)


def magic_parser_two(text):

    EQ = ':'
    LBRACE = '{'
    RBRACE = '}'
    key = Word(alphas+'_')
    value = Forward()
    value << ((OneOrMore(Word(alphas+'_"., ') | Group(LBRACE + ZeroOrMore(Word(alphas+'_"., ')) + RBRACE))) + "\n")
    entry = key + EQ + value

    struct = Group(LBRACE + ZeroOrMore(entry) + RBRACE)

    result = struct.parseString(text)
    print(result)


with open(file_path, 'r') as file:
    data = file.read()
    # print(data)

    # Break the text into a simple pattern of \n\n
    # i.e two line breaks which breaks the whole code into {} blocks
    # Also, ignoring the first block since it is not required
    # in the target sheet.
    # If the first entry (The Logical Requirement is named Entry for e.o.u) 
    # is also required
    # TODO What to do with the first entry?
    # Last, Entry is not required(Purely Assumed on the file)
    for i, entry in enumerate(data.split('\n\n')[1:-1]):
        
        # Loop Specific Variables
        ROW_ENTRY = dict()
        FCL_ID = ''
        SYSTEM_REQUIREMENTS = ''
        OH_REQ = ''
        CR_LINKED = ''
        HLR_FILE_NAME = ''
        HLR_IDENTIFIER = ''
        USED_VARIABLE = ''
        PRODUCED_VARIABLE = ''

        print(f"Parsing Entry {i+1}: \n",)

        FCL_ID = extract_fcid_from_entry(entry)
        
        text_without_fclid = entry[entry.find('{'):]
        text_without_fclid = text_without_fclid
        magic_parser_two(text_without_fclid)