html_grammar = """
    start: element
    
    element: /<script>((?!<\/script>).)+<\/script>/s -> script
         | /<style>((?!<\/style>).)+<\/style>/s -> style
         | "<" tag (attribute|blade_expression)* ">"
         | "<" tag (attribute|blade_expression)* "/>"
         | "<" tag (attribute|blade_expression)* ">" contents? "</" tag ">"
         | contents
    
    attribute:  /[a-zA-Z@\:][a-z:A-Z.\-]*(="[^"]*")?/s
    
    blade_expression: /{{.+?}}/s | /@[a-z]+\(.+?\)/
    
    ?contents: element+ | textp? element text? | text
    
    tag: /([a-z:\.\-0-9]+)/i
    
    textp: blade_directive | whitespace | group1
    text: blade_directive | whitespace | group2
    
    group1: /((?!<\/?[^>]+\/?>).)+/is -> group
    group2: /((?!<\/([a-z:\.\-0-9]+)>).)+/is -> group
    
    blade_directive: /@[a-z]+(?:\([^)]+\))?/ element? /@[a-z]+/?
    
    whitespace: /[\s\r\n\t]+/x

    COMMENT: /<!--.+?-->|{{--.+?--}}|<!DOCTYPE html>/
    %ignore COMMENT
    %ignore /[\s\r\n\t]+/x
"""
