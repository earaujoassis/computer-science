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

extern int yylex (void);
void yyerror (const char*);
void yyerror (const char*, int);
extern int yylineno;
extern FILE* yyin;

%}

%union {
  std::string* lxval;
}

%token<lxval> MAIN
%token INT
%token CHAR
%token RETURN
%token READ
%token WRITE
%token WRITELN
%token IF
%token THEN
%token ELSE
%token WHILE
%token DO
%token<lxval> ID
%token<lxval> LITINT
%token<lxval> LITCHAR
%token<lxval> LITSTRING

%right '='
%left OR
%left AND
%nonassoc EQUAL NEQUAL
%nonassoc '<' '>' LESSEQ GREATEREQ
%left '+' '-'
%left '*' '/' '%'

%type<datatype> Tipo
%type<node> Programa DeclFuncVar DeclProg DeclVar DeclFunc ListaParametros ListaParametrosCont Bloco ListaDeclVar ListaComando Comando Expr AssignExpr CondExpr OrExpr AndExpr EqExpr DesigExpr AddExpr MulExpr UnExpr LValueExpr PrimExpr ListExpr
%start Programa

%%

Programa:
  DeclFuncVar DeclProg { }
;

DeclFuncVar:
  Tipo ID DeclVar ';' DeclFuncVar { }
  | Tipo ID '[' LITINT ']' DeclVar ';' DeclFuncVar { }
  | Tipo ID DeclFunc DeclFuncVar { }
  | { }
;

DeclProg:
  MAIN Bloco { }
;

DeclVar:
  ',' ID DeclVar { }
  | ',' ID '[' LITINT ']' DeclVar { }
  | { }
;

DeclFunc:
  '(' ListaParametros ')' Bloco { }
;

ListaParametros:
  ListaParametrosCont { }
  | { }
;

ListaParametrosCont:
  Tipo ID { }
  | Tipo ID '[' ']' { }
  | Tipo ID ',' ListaParametrosCont { }
  | Tipo ID '[' ']' ',' ListaParametrosCont { }
;

Bloco:
  '{' ListaDeclVar ListaComando '}' { }
  | '{' ListaDeclVar '}' { }
;

ListaDeclVar:
  Tipo ID DeclVar ';' ListaDeclVar { }
  | Tipo ID '[' LITINT ']' DeclVar ';' ListaDeclVar { }
  | { }
;

Tipo:
  INT { }
  | CHAR { }
;

ListaComando:
  Comando { }
  | Comando ListaComando { }
;

Comando:
  ';' { }
  | Expr ';' { }
  | RETURN Expr ';' { }
  | READ LValueExpr ';' { }
  | WRITE Expr ';' { }
  | WRITE LITSTRING ';' { }
  | WRITELN ';' { }
  | IF '(' Expr ')' THEN Comando { }
  | IF '(' Expr ')' THEN Comando ELSE Comando { }
  | WHILE '(' Expr ')' DO Comando { }
  | Bloco { }
;

Expr:
  AssignExpr { }
;

AssignExpr:
  CondExpr { }
  | LValueExpr '=' AssignExpr { }
;

CondExpr:
  OrExpr { }
  | OrExpr '?' Expr ':' CondExpr { }
;

OrExpr:
  OrExpr OR AndExpr { }
  | AndExpr { }
;

AndExpr:
  AndExpr AND EqExpr { }
  | EqExpr { }
;

EqExpr:
  EqExpr EQUAL DesigExpr { }
  | EqExpr NEQUAL DesigExpr { }
  | DesigExpr { }
;

DesigExpr:
  DesigExpr '<' AddExpr { }
  | DesigExpr '>' AddExpr { }
  | DesigExpr GREATEREQ AddExpr { }
  | DesigExpr LESSEQ AddExpr { }
  | AddExpr { }
;

AddExpr:
  AddExpr '+' MulExpr { }
  | AddExpr '-' MulExpr { }
  | MulExpr { }
;

MulExpr:
  MulExpr '*' UnExpr { }
  | MulExpr '/' UnExpr { }
  | MulExpr '%' UnExpr { }
  | UnExpr { }
;

UnExpr:
  '-' PrimExpr { }
  | '!' PrimExpr { }
  | PrimExpr { }
;

LValueExpr:
  ID '[' Expr ']' { }
  | ID { }
;

PrimExpr:
  ID '(' ListExpr ')' { }
  | ID '(' ')' { }
  | ID '[' Expr ']' { }
  | ID { }
  | LITCHAR { }
  | LITINT { }
  | '(' Expr ')' { }
;

ListExpr:
  AssignExpr { }
  | ListExpr ',' AssignExpr { }
;

%%

void yyerror (const char *description)
{
  fprintf (stderr, "\033[91mErro!\033[0m %s (Linha: %d)\n", description, yylineno);
  exit (1);
}

void yyerror (const char *description,
              int error_line)
{
  fprintf (stderr, "\033[91mErro!\033[0m %s (Linha: %d)\n", description, error_line);
  exit (1);
}

int main (int argc,
          char** argv)
{
  if (argc > 1)
    yyin = fopen (argv[1], "r");
  else
    fprintf (stdout, "Análise de código feita pela entrada padrão (stdin).\n");
  yyparse ();
  fprintf (stdout, "Análise sintática concluída.\n\n");
  return 0;
}
