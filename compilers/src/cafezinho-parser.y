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

#define TRACE printf ("reduce at line %d\n", __LINE__);

extern int yylex (void);
void yyerror (const char*);
void yyerror (const char*, int);
extern int yylineno;
extern FILE* yyin;

std::string new_line_escape = "\n";
ASTNode* root;

%}

%union {
  ASTNode* node;
  DataType datatype;
  Op oper;
  std::string* lxval;
}

%token<lxval> PROGRAM
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
  DeclFuncVar DeclProg {
    root = $2;
    root->reverse ();
    root->add ($1);
  }
;

DeclFuncVar:
  Tipo ID DeclVar ';' DeclFuncVar {
    $$ = $5;
    static_cast<DeclVar*> ($3)->setDataType ($1);
    $3->add (new DeclId ($2));
    $$->add ($3);
    $$->set_location (yylineno);
  }
  | Tipo ID '[' LITINT ']' DeclVar ';' DeclFuncVar {
    $$ = $8;
    static_cast<DeclVar*> ($6)->setDataType ($1);
    $6->add (new DeclId ($2, new ConstExpr(INT_T, $4)));
    $$->add ($6);
    $$->set_location (yylineno);
  }
  | Tipo ID DeclFunc DeclFuncVar {
    $$ = $4;
    static_cast<DeclFunc*> ($3)->setFuncName ($2);
    static_cast<DeclFunc*> ($3)->setDataType ($1);
    $$->add ($3);
    $$->set_location (yylineno);
  }
  | {
    $$ = new ASTNode ();
    $$->set_location (yylineno);
    $$->set_empty_prod ();
  }
;

DeclProg:
  PROGRAM Bloco {
    $$ = new ASTNode ();
    $$->add ($2);
    $$->set_location (yylineno);
  }
;

DeclVar:
  ',' ID DeclVar {
    $$ = $3;
    $$->add (new DeclId ($2));
    $$->set_location (yylineno);
  }
  | ',' ID '[' LITINT ']' DeclVar {
    $$ = $6;
    $$->add (new DeclId ($2, new ConstExpr (INT_T, $4)));
    $$->set_location (yylineno);
  }
  | {
    $$ = new ASTNode ();
    $$->set_location (yylineno);
    $$->set_empty_prod ();
  }
;

DeclFunc:
  '(' ListaParametros ')' Bloco {
    $$ = new DeclFunc ($2, $4);
    $$->set_location (yylineno);
  }
;

ListaParametros:
  ListaParametrosCont { $$ = $1; }
  | {
    $$ = new ASTNode ();
    $$->set_location (yylineno);
    $$->set_empty_prod ();
  }
;

ListaParametrosCont:
  Tipo ID {
    $$ = new ListParam ();
    $$->add (new Param ($1, $2));
    $$->set_location (yylineno);
  }
  | Tipo ID '[' ']' {
    $$ = new ListParam ();
    $$->add (new Param( ($1==INT_T)?INT_ARRAY_T:CHAR_ARRAY_T, $2 ) );
    $$->set_location (yylineno);
  }
  | Tipo ID ',' ListaParametrosCont {
    $$ = $4;
    $$->add (new Param ($1, $2));
    $$->set_location (yylineno);
  }
  | Tipo ID '[' ']' ',' ListaParametrosCont {
    $$ = $6;
    $$->add (new Param (($1==INT_T) ? INT_ARRAY_T : CHAR_ARRAY_T, $2));
    $$->set_location (yylineno);
  }
;

Bloco:
  '{' ListaDeclVar ListaComando '}' {
    $$ = new Block (static_cast<DeclVarList*> ($2), static_cast<ListCommand*> ($3));
    $$->set_location (yylineno);
  }
  | '{' ListaDeclVar '}' {
    $$ = new Block (static_cast<DeclVarList*> ($2));
    $$->set_location (yylineno);
  }
;

ListaDeclVar:
  Tipo ID DeclVar ';' ListaDeclVar {
    $$ = $5;
    static_cast<DeclVar*> ($3)->setDataType ($1);
    $3->add (new DeclId ($2));
    $$->add ($3);
    $$->set_location (yylineno);
  }
  | Tipo ID '[' LITINT ']' DeclVar ';' ListaDeclVar {
    $$ = $8;
    static_cast<DeclVar*> ($6)->setDataType ($1);
    $6->add (new DeclId ($2, new ConstExpr(INT_T, $4)));
    $$->add ($6);
    $$->set_location (yylineno);
  }
  | {
    $$ = new ASTNode ();
    $$->set_location (yylineno);
    $$->set_empty_prod ();
  }
;

Tipo:
  INT { $$ = INT_T; }
  | CHAR { $$ = CHAR_T; }
;

ListaComando:
  Comando {
    $$ = new ListCommand ();
    $$->add ($1);
    $$->set_location (yylineno);
  }
  | Comando ListaComando {
    $$ = $1;
    $$->add ($2);
    $$->set_location (yylineno);
  }
;

Comando:
  ';' {
    $$ = new Command ();
    $$->set_location (yylineno);
  }
  | Expr ';' {
    $$ = $1;
  }
  | RETURN Expr ';' {
    $$ = new Return($2);
    $$->set_location (yylineno);
  }
  | READ LValueExpr ';' {
    Id* identifier = dynamic_cast<Id*>($2);
    $$ = new Read (identifier);
    $$->set_location (yylineno);
  }
  | WRITE Expr ';' {
    $$ = new Write ($2);
    $$->set_location (yylineno);
  }
  | WRITE LITSTRING ';' {
    $$ = new Write (new ConstExpr (CHAR_ARRAY_T, $2));
    $$->set_location (yylineno);
  }
  | WRITELN ';' {
    $$ = new Write (new ConstExpr (CHAR_ARRAY_T, &new_line_escape));
    $$->set_location (yylineno);
  }
  | IF '(' Expr ')' THEN Comando {
    $$ = new If ($3, $6);
    $$->set_location (yylineno);
  }
  | IF '(' Expr ')' THEN Comando ELSE Comando {
    $$ = new If ($3, $6, $8);
    $$->set_location (yylineno);
  }
  | WHILE '(' Expr ')' DO Comando {
    $$ = new While ($3, $6);
    $$->set_location (yylineno);
  }
  | Bloco { $$ = $1; }
;

Expr:
  AssignExpr { $$ = $1; }
;

AssignExpr:
  CondExpr { $$ = $1; }
  | LValueExpr '=' AssignExpr {
    Id* aux = dynamic_cast<Id*> ($1);
    $$ = new AssignExpr (aux, $3);
    $$->set_location (yylineno);
  }
;

CondExpr:
  OrExpr { $$ = $1; }
  | OrExpr '?' Expr ':' CondExpr {
    $$ = new TerExpr ($1, $3, $5);
    $$->set_location (yylineno);
  }
;

OrExpr:
  OrExpr OR AndExpr {
    $$ = new BinExpr (LOGICAL_OR, $1, $3);
    $$->set_location (yylineno);
  }
  | AndExpr { $$ = $1; }
;

AndExpr:
  AndExpr AND EqExpr {
    $$ = new BinExpr (LOGICAL_AND, $1, $3);
    $$->set_location (yylineno);
  }
  | EqExpr { $$ = $1; }
;

EqExpr:
  EqExpr EQUAL DesigExpr {
    $$ = new BinExpr (EQUALS, $1, $3);
    $$->set_location (yylineno);
  }
  | EqExpr NEQUAL DesigExpr {
    $$ = new BinExpr (NOT_EQUAL, $1, $3);
    $$->set_location (yylineno);
  }
  | DesigExpr { $$ = $1; }
;

DesigExpr:
  DesigExpr '<' AddExpr {
    $$ = new BinExpr (LESS, $1, $3);
    $$->set_location (yylineno);
  }
  | DesigExpr '>' AddExpr {
    $$ = new BinExpr (GREATER, $1, $3);
    $$->set_location (yylineno);
  }
  | DesigExpr GREATEREQ AddExpr {
    $$ = new BinExpr (GREATER_EQUAL, $1, $3);
    $$->set_location (yylineno);
  }
  | DesigExpr LESSEQ AddExpr {
    $$ = new BinExpr (LESS_EQUAL, $1, $3);
    $$->set_location (yylineno);
  }
  | AddExpr { $$ = $1; }
;

AddExpr:
  AddExpr '+' MulExpr {
    $$ = new BinExpr (PLUS, $1, $3);
    $$->set_location (yylineno);
  }
  | AddExpr '-' MulExpr {
    $$ = new BinExpr (MINUS, $1, $3);
    $$->set_location (yylineno);
  }
  | MulExpr { $$ = $1; }
;

MulExpr:
  MulExpr '*' UnExpr {
    $$ = new BinExpr (TIMES, $1, $3);
    $$->set_location (yylineno);
  }
  | MulExpr '/' UnExpr {
    $$ = new BinExpr (DIVIDES, $1, $3);
    $$->set_location (yylineno);
  }
  | MulExpr '%' UnExpr {
    $$ = new BinExpr (MOD, $1, $3);
    $$->set_location (yylineno);
  }
  | UnExpr { $$ = $1; }
;

UnExpr:
  '-' PrimExpr {
    $$ = new UnExpr (MINUS, $2);
    $$->set_location (yylineno);
  }
  | '!' PrimExpr {
    $$ = new UnExpr (NOT, $2);
    $$->set_location (yylineno);
  }
  | PrimExpr { $$ = $1; }
;

LValueExpr:
  ID '[' Expr ']' {
    $$ = new Id ($1, $3);
    $$->set_location (yylineno);
  }
  | ID {
    $$ = new Id ($1);
    $$->set_location (yylineno);
  }
;

PrimExpr:
  ID '(' ListExpr ')' {
    $$ = new FuncId ($1, $3);
    $$->set_location (yylineno);
  }
  | ID '(' ')' {
    $$ = new FuncId ($1);
    $$->set_location (yylineno);
  }
  | ID '[' Expr ']' {
    $$ = new Id ($1, $3);
    $$->set_location (yylineno);
  }
  | ID {
    $$ = new Id ($1);
    $$->set_location (yylineno);
  }
  | LITCHAR {
    $$ = new ConstExpr (CHAR_T, $1);
    $$->set_location (yylineno);
  }
  | LITINT {
    $$ = new ConstExpr (INT_T, $1);
    $$->set_location (yylineno);
  }
  | '(' Expr ')' { $$ = $2; }
;

ListExpr:
  AssignExpr {
    $$ = new ListArg();
    $$->add ($1);
    $$->set_location (yylineno);
  }
  | ListExpr ',' AssignExpr {
    $$ = $1;
    $$->add ($3);
    $$->set_location (yylineno);
  }
;

%%

void yyerror (const char *description)
{
  fprintf (stderr, "\033[91mErro!\033[0m %s (Linha: %d)\n\n", description, yylineno);
  exit (1);
}

void yyerror (const char *description,
              int error_line)
{
  fprintf (stderr, "\033[91mErro!\033[0m %s (Linha: %d)\n\n", description, error_line);
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
  scope_level = 0;
  var_symbol_tab.clear ();
  func_symbol_tab.clear ();
  while (!declared.empty ())
    declared.pop ();
#ifdef DEBUG
  fprintf (stdout, "Árvore de sintaxe abstrata: %s\n", argv[1]);
  root->print (0);
  fprintf (stdout, "Legenda: @ (linha de código), d (profundidade), c (filhos)\n");
#else
  root->walk (0);
#endif
  fprintf (stdout, "cafezinho: Concluído com sucesso.\n\n", argv[0]);
  return 0;
}
