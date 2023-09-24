from string import Template

html_grammar = """
   start: element+
    
    element: /<script>((?!<\/script>).)+<\/script>/s -> script
         | /<style>((?!<\/style>).)+<\/style>/s -> style
         | "<" tag (attribute|blade_expression)* ">"
         | "<" tag (attribute|blade_expression)* "/>"
         | "<" tag (attribute|blade_expression)* ">" element* "</" tag ">"
         | foreach
         | whitespace
         | "@if" /\(((?!<\/?[^>]+\/?>|@[a-z]+).)+\)/ start "@else" start "@endif"
         | "@if" /\(((?!<\/?[^>]+\/?>|@[a-z]+).)+\)/ start "@endif"
         | "@for" "(" /[^;]+;[^;]+;[^)]+/ ")" element "@endfor"
         | "@forelse"  "(" expression "as" expression ")" start "@empty" start "@endforelse"
         | switch_statement
         | "@while" "(" args? ")" start "@endwhile"
         | "@once" start "@endonce"
         | "@csrf"
         | "@push" "(" args? ")" start "@endpush"
         | "@pushOnce" "(" args? ")" start "@endPushOnce"
         | "@php" /((?!@endphp).)+/si "@endphp"
         | "@can" "(" args? ")" start "@endcan" 
         | "@break"
         | "@livewireStyles"
         | "@continue"
         | blade_expression
         | /((?!<\/?[^>]+\/?>|@if|@for|@forelse|@while|@once|@crsf|@push|@pushOnce|@php|@can|@break|@continue|@case|@switch|@endswitch|@break|@default|@livewireStyles|@can|@end).)+/is -> group
    
    attribute:  /[a-zA-Z@\:][a-z:A-Z.\-]*(="[^"]*")?/s | attribute_expression
    
    switch_statement: "@switch" /\([^)]+\)/ switch_cases+ "@endswitch"
    
    switch_cases: "@case" /\([^)]+\)/ start "@break" | "@default" start
    
    attribute_expression: /[a-zA-Z@\:]+/ /\(.+\)/
    
    foreach: "@foreach"  "(" /((?!as).)+/ "as" /[^)]+/ ")"  start "@endforeach"
    
    blade_expression: /{{.+?}}/s | /@[a-z]+\(.+?\)/si | /{!!.+?!!}/
    
    tag: /([a-z:\.\-0-9]+)/i
    
    whitespace: /[\s\r\n\t]+/x
    expression: literal
          | variable
          | unary_op expression
          | expression binary_op expression
          | function_call
          | "(" expression ")"

literal: ESCAPED_STRING | NUMBER |  /'.+?(?<!\\\\)'/s

variable: "$" CNAME

unary_op: "!"

binary_op: "+" | "-" | "*" | "/" | "==" | "!=" | "<" | ">" | "<=" | ">=" | "%"

 function_call: (package_name "::" | variable "->") (CNAME "(" args? ")" | CNAME) ("->" (CNAME "(" args? ")" | CNAME))*

 package_name: CNAME ("\\\\" CNAME)*

args: expression ("," expression)*

%import common.CNAME
%import common.ESCAPED_STRING
%import common.NUMBER

    COMMENT: /<!--.+?-->|{{--.+?--}}|<!DOCTYPE html>/
    %ignore COMMENT
    %ignore /[ \r\n\t\f]+/x

"""


json_grammar = """
  start: /"/ group /"/
         | dict
         | list
         | ESCAPED_STRING
         | SIGNED_NUMBER
         | "true" | "false" | "null"
         
    group: $GROUP

    list : "[" [start ("," start)*] "]"

    dict : "{" [pair ("," pair)*] "}"
    pair : ESCAPED_STRING ":" start

    %import common.ESCAPED_STRING
    %import common.SIGNED_NUMBER
    %import common.WS
    %ignore WS
"""

def sub_in_grammar(grammar, dictionary):
    return Template(grammar).substitute(dictionary)
