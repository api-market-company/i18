from lark import Lark, Tree, Transformer, Visitor, Token

def compile(grammar):
    parser = Parser(grammar)
    return parser

def sub(grammar,replace,text):
   parser = Parser(grammar)
   return parser.sub(replace,text)

def search(grammar,text):
   parser = Parser(grammar)
   return parser.search(text)


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

