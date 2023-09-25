from string import Template

html_grammar = """
 start: element+
    
    element: /<script>((?!<\/script>).)+<\/script>/s -> script
         | /<style>((?!<\/style>).)+<\/style>/s -> style
         | "<" tag (attribute|blade_expression)* ">"
         | "<" tag (attribute|blade_expression)* "/>"
         | "@if" "(" args ")" start ("@elseif" "(" args ")" start)+ "@endif"
         | "@if" "(" args ")" start ("@elseif" "(" args ")" start)+  "@else" start "@endif"
         | switch_statement
         | "<" tag (attribute|blade_expression)* ">" element* "</" tag ">"
         | foreach
         | whitespace
         | "@if" "(" args ")" start "@endif"
         | "@if" "(" args ")" start "@else" start "@endif"
         | "@for" "(" /[^;]+;[^;]+;[^)]+/ ")" element "@endfor"
         | "@forelse"  "(" expression "as" expression ")" start "@empty" start "@endforelse"
         | "@while" "(" args? ")" start "@endwhile"
         | "@once" start "@endonce"
         | "@csrf"
         | "@push" "(" args? ")" start "@endpush"
         | "@pushOnce" "(" args? ")" start "@endPushOnce"
         | "@php" /((?!@endphp).)+/si "@endphp"
         | "@can" "(" args? ")" start "@endcan" 
         | "@auth" ( "(" args? ")" )? start "@else" start "@endauth"
         | "@guest" start "@endguest"
         | "@error" "(" args? ")" start "@enderror" 
         | "@unless" "(" args? ")" start "@endunless"
         | "@isset" "(" args? ")" start "@endisset"
         | "@component" "(" args? ")" start "@endcomponent"
         | "@break"
         | "@livewireStyles"
         | "@empty"
         | "@continue"
         | blade_expression
         | /((?!<\/?[^>]+\/?>|@elseif|@if|@for|@forelse|@endfor|@endforelse|@while|@else|@endif|@once|@crsf|@push|@pushOnce|@php|@can|@break|@continue|@case|@switch|@endswitch|@break|@default|@livewireStyles|@can|@error|@enderror|@isset|@endisset|@empty|@component|@endcomponent).)+/is -> group
    
    attribute: /[@\:]/? /[a-zA-Z][a-z:0-9A-Z.\-{}$ ]*/ /=(("{{.+?}}")|('{{.+?}}')|("[^"]*")|('[^']*'))/s? | attribute_expression
     
    attribute_expression: /[a-zA-Z@\:]+/ /\(.+\)/
    
    switch_statement: "@switch" /\([^)]+\)/ switch_cases+ "@endswitch"

    elseif_cases: "@elseif" "(" args ")" start?
    
    switch_cases: "@case" /\([^)]+\)/ start "@break" | "@default" start
    
    
    foreach: "@foreach"  "(" /((?!as).)+/ "as" /[^)]+/ ")"  start "@endforeach"
    
    blade_expression: /{{.+?}}/s | /@(?!if|for|forelse|endfor|endforelse|while|else|elseif|endif|once|crsf|push|pushOnce|php|can|break|continue|case|switch|endswitch|break|default|livewireStyles|can|error|enderror|isset|endisset|component|endcomponent)[a-z]+/si "(" args? ")" | /{!!.+?!!}/
    
    tag: /([a-z:\.\-0-9]+)/i
    
    whitespace: /[\s\r\n\t]+/x
    expression: literal
          | variable
          | unary_op expression
          | expression binary_op expression
          | method_call
          | function_call
          | "(" expression ")"
          | "[" expression "=>" expression "]"
          | variable "=>" variable
          | variable ("[" expression "]" ("[" expression "]")*)
          | expression "?" expression ":" expression

literal: ESCAPED_STRING | NUMBER |  /'.+?(?<!\\\\)'/s | /null/i | /true/i | /false/i

variable: "$" CNAME

unary_op: "!"

binary_op: "+" | "-" | "*" | "/" | "==" | "!=" | "<" | ">" | "<=" | ">=" | "%" | "===" | "!==" | "<>" | "<=>" | "&&" | "||" | "and" | "or" | "??"

method_call: (package_name "::" | variable "->" | variable "[" expression "]" | function_call "->") (CNAME "(" args? ")" | CNAME | CNAME "[" expression "]") ("->" (CNAME "(" args? ")" | CNAME | CNAME "[" expression "]"))*

 function_call: CNAME "(" args? ")"

 package_name: CNAME ("\\\\" CNAME)*

args: expression ("," expression)*

%import common.CNAME
%import common.ESCAPED_STRING
%import common.NUMBER

    COMMENT: /<!--->|<!---->|<!--.+?-->|{{--.+?--}}|<!DOCTYPE html.*?>/
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
