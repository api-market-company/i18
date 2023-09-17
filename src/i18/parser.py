from lark import Lark, Tree, Transformer, Visitor, Token
import spacy
from spacy.matcher import Matcher


def compile(grammar):
    parser = Parser(grammar)
    return parser

def sub(grammar,replace,text):
   parser = Parser(grammar)
   return parser.sub(replace,text)

def search(grammar,text):
   parser = Parser(grammar)
   return parser.search(replace,text)

def compile_lexer():
    lexer = Lexer()
    return lexer


def remove_stop_words(text):
    return text.replace(" ", "_")


class Lexer:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        matcher = Matcher(nlp.vocab)
        matcher.add("Currency", [[
            {"TEXT": "MXN"}
        ]])
        matcher.add("Email", [[{'LIKE_EMAIL': True}]])
        matcher.add("Number", [[{'LIKE_NUM': True}]])
        matcher.add("Url", [[{'LIKE_URL': True}]])
        matcher.add("BladeExpresion", [[
            {"TEXT": "{{"},
            {"TEXT": {"REGEX": "\$\w+"}},
            {"TEXT": "->"},
            {"TEXT": {"REGEX": "\w+"}},
            {"TEXT": "}}"}
            ]])
        matcher.add("Text", [[
            {
                "TEXT": {"REGEX": "\w+"}
                }
        ]])
        self.translator = Translator()
        self.translation = {
                'en': {},
                'es': {}
                }
    def translate(self,text):
            key = text.value.strip()
            if len(key) <= 2:
                return self.translation
            english = self.translator.translate(key, dest="en").text
            spanish = ""
            try:
                spanish = self.translator.translate(english, dest="es").text
            except:
                spanish = english
            key = remove_stop_words(english).lower()
            self.translation['en'][key] = english
            self.translation['es'][key] = spanish
            return self.translation

    def analyze(self, text):
        doc = nlp(text)
        matches = matcher(doc)
        return matches


class Parser(Visitor):
    def __init__(self,grammar):
        super().__init__()  
        self.matches = []
        self.parser = Lark(grammar, propagate_positions=True)
    def group(self, tree):
        self.matches.extend(tree.children)
    def search(self,text):
        tree = self.parser.parse(text)
        self.visit(tree)
        matches = [*self.matches]
        self.matches = []
        return matches
    def sub(self, replace, text):
        tree = self.parser.parse(text)
        self.visit(tree)
        diff_x,diff_y = 0,0
        for match in sorted(self.matches, key=lambda token: token.start_pos):
            replacement = replace(match.value)
            start_pos = match.start_pos
            end_pos = match.end_pos
            x,y = diff_x+start_pos,diff_y+end_pos
            text = text[:x] + replacement + text[y:]
            diff = len(replacement)-(end_pos-start_pos)
            diff_x,diff_y = diff+diff_x,diff+diff_y
        self.matches = []
        return text

