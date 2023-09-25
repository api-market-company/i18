import ply.lex as lex
from deep_translator import (GoogleTranslator,DeeplTranslator)
import re


class Lexer:
    t_BLADE_COMMENT = r'\(?{{--.*--}}\)?'
    t_BLADE_EXPRESSION = r'@[a-z]+.+'
    t_BLADE_ECHO = r'[.;,]*(({{.*?}})|(\({{.*?}}\))|({!!.+!!}))[.;,]*'
    t_SPECIAL_CHARACTERS = r'[=\/\\\%\^\&\*\-\+\[\]]+'
    t_NUMBER = r'[0-9]+(.[0-9]*)?'
    tokens = (
            'DATE',
            'WHITESPACE',
            'EMAIL',
            'BLADE_COMMENT',
            'BLADE_ECHO',
            'STRING',
            'BLADE_EXPRESSION',
            'NUMBER',
            'SPECIAL_CHARACTERS',
        )
    def __init__(self, target_languages={'es': GoogleTranslator(source='auto', target='es'), 'en': GoogleTranslator(source='auto', target='en')}, default_language='en', **kwargs):
        self.translations = {key: {} for key in target_languages.keys()}
        self.target_languages = [None]*len(target_languages)
        i = 1
        for target_language, translator in target_languages.items():
            if target_language == default_language:
                self.target_languages[0] = (target_language, translator)
            else:
                self.target_languages[i] = (target_language, translator)
                i += 1
        self.lexer = lex.lex(object=self, **kwargs)

    def t_EMAIL(self,t):
        r'[\w.-]+@([\w-]+.)+[\w-]{2,4}'
        return t

    def t_DATE(self,t):
        r"((?i)\b(mon(?:day|ady|dya|dai)?|tues(?:day|ady|dya|dai)?|wed(?:nesday|ensday|nesdai)?|thurs(?:day|ady|dya|dai)?|fri(?:day|ady|dya|dai)?|sat(?:urday|erday|urady|urday)?|sun(?:day|ady|dya|dai)?)\b.* (?i)\b(jan(?:uary|uari|uaray|uare)?|feb(?:ruary|urary|ruari|ruary)?|mar(?:ch|hc)?|apr(?:il|li)?|may|jun(?:e|e)?|jul(?:y|y)?|aug(?:ust|sut|ust)?|sep(?:tember|tembre|tembr)?|oct(?:ober|obre|ober)?|nov(?:ember|embre|embr)?|dec(?:ember|embre|embr)?)\b .* \d{1,2})|\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) (\d{1,2}), (\d{4})\b"
        t.value = "TODO: \Carbon\Carbon::parse()"
        return t

    def t_STRING(self,t):
        r'(?i)[\sA-Za-z!?,¿.\'!"$\'áéíóúñ]+'
        text =  bytes(t.value.strip(), "utf-8").decode("unicode_escape")
        if len(text) <= 2 or re.search('(?i)lorem|ipsum|aliquip', text):
            return t
        try:
            translation = self.target_languages[0][1].translate(text=text)
            translation = re.sub(r'[\n\s\r\f]{2,}', ' ', translation)
            key = translation.lower().replace(" ", "_").replace(",", "_").replace("\"", "").replace("'", "_")
            key = re.sub(r'_{2,}', '_', key)
            key = re.sub(r'[.,;]_', '_', key)
            key = re.sub(r'(_$)|(^_)', lambda x: "", key)
            self.translations[self.target_languages[0][0]][key] = translation
            for index in range(1, len(self.target_languages)):
                target_language, translator = self.target_languages[index]
                self.translations[target_language][key] = translator.translate(text=text)
            t.value = " {{__(\"" + key + "\")}} "
            return t
        except:
            return t

    def t_WHITESPACE(self,t):
        r'[\n\r\f]+'
        t.value = " "
        return t

    def t_error(self,t):
        t.type = "DEFAULT"
        t.value = t.value[0]
        t.lexer.lexpos += 1
        return t

    def tokenize(self, text):
        self.lexer.input(text)
        while True:
            token = self.lexer.token()
            if not token:
                break
            yield token

    def translate(self, inner_content):
        acc = ""
        for token in self.tokenize(inner_content.strip()):
            acc += token.value
        return acc.strip()
