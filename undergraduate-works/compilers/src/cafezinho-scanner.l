/*
 * Copyright 2013 Ewerton Assis.
 * Use intended for the course of Compilers under the Computer Science
 * undergraduate program at the Universidade Federal de Goias, Brazil.
 * UFG Enrollment: 060194.
 *
 */

%{

#include <cstdio>
#include <cstdlib>
#include <string>
#include <cstring>

#include "ast/ast.hpp"
#include "cafezinho-parser.hpp"

void yyerror (const char *);
std::string buffer;
char invalid_char[30] = "Caractere inválido: ";

%}
%x STRING COMMENT RCHAR ESCP ENDCHAR

DELIM  [ \t\r]
WS     {DELIM}+
DIGIT  [0-9]
LETTER [A-Za-z_]

%%

{WS}        { ; }
\n          { yylineno++; }
"programa"  { yylval.lxval = new std::string (yytext); return PROGRAM; }
"int"       { return INT; }
"car"       { return CHAR; }
"retorne"   { return RETURN; }
"leia"      { return READ; }
"escreva"   { return WRITE; }
"novalinha" { return WRITELN; }
"se"        { return IF; }
"entao"     { return THEN; }
"senao"     { return ELSE; }
"enquanto"  { return WHILE; }
"execute"   { return DO; }

[-!(){}<>+*/%=?:;,] { return *yytext; }
"["  { return *yytext; }
"]"  { return *yytext; }
"==" { return EQUAL; }
"!=" { return NEQUAL; }
"<=" { return LESSEQ; }
">=" { return GREATEREQ; }
"ou" { return OR; }
"e"  { return AND; }

{LETTER}({LETTER}|{DIGIT})* { yylval.lxval = new std::string (yytext); return ID; }
{DIGIT}+ { yylval.lxval = new std::string (yytext); return LITINT; }

' { BEGIN RCHAR; }
<RCHAR>\\ { BEGIN ESCP; }
<RCHAR>. { buffer = ""; buffer += *yytext; BEGIN ENDCHAR; }
<ESCP>{
  [0ntarbf\\'] { buffer = "\\"; buffer += *yytext; BEGIN ENDCHAR; }
}
<ESCP>. { yyerror ("Delimitador ' obrigatório em constante do tipo caractere (car)."); }
<ENDCHAR>' { BEGIN INITIAL; yylval.lxval = new std::string (buffer); return LITCHAR; }
<ENDCHAR>. { yyerror( "Delimitador ' obrigatório em constante do tipo caractere (car)." ); };

\" { BEGIN STRING; buffer = ""; }
<STRING>\" { BEGIN INITIAL; yylval.lxval = new std::string (buffer); return LITSTRING; }
<STRING>\n { yylineno++; yyerror ("Cadeia de caracteres ocupa mais de uma linha."); }
<STRING>{
  "\\n"   { buffer += '\n'; }
  "\\t"   { buffer += '\t'; }
  "\\a"   { buffer += '\a'; }
  "\\r"   { buffer += '\r'; }
  "\\b"   { buffer += '\b'; }
  "\\f"   { buffer += '\f'; }
  "\\\""    { buffer += '\\'; }
}
<STRING><<EOF>> { yyerror ("Cadeia de caracteres não finalizada."); }
<STRING>. { buffer += *yytext; }

"/*" { BEGIN COMMENT; }
<COMMENT>"*"+"/" { BEGIN INITIAL; }
<COMMENT>"*"+[^*/\n] {;}
<COMMENT>\n { yylineno++; }
<COMMENT>[^*\n]  { ; }
<COMMENT><<EOF>> { yyerror ("Comentário não termina."); }

. { yyerror (strcat (invalid_char, yytext)); }

%%
int yywrap () { return 1; }
