/*
 * Copyright 2013 Ewerton Assis.
 * Use intended for the course of Compilers under the Computer Science
 * undergraduate program at the Universidade Federal de Goias, Brazil.
 * UFG Enrollment: 060194.
 *
 */

#ifndef __CAFEZINHO_AST_HPP__
#define __CAFEZINHO_AST_HPP__

#include <iostream>
#include <vector>
#include <algorithm>
#include <string>
#include <map>
#include <stack>
#include <set>
#include <sstream>

#define PRINT_DESLOCATION 3

void yyerror (const char *);
void yyerror (const char *, int);

enum DataType 
{
  INT_T = 0x0,
  CHAR_T = 0x1,
  INT_ARRAY_T = 0x2,
  CHAR_ARRAY_T = 0x3,
};

enum Op
{
  PLUS,
  MINUS,
  TIMES,
  DIVIDES,
  MOD,
  GREATER,
  LESS,
  EQUALS,
  NOT_EQUAL,
  LESS_EQUAL,
  GREATER_EQUAL,
  LOGICAL_OR,
  LOGICAL_AND,
  NOT
};

class DeclFunc;

typedef std::map< std::string, std::stack< std::pair< DataType,int > > > VarSymTab;
typedef std::map< std::string, DeclFunc* > FuncSymTab;

static VarSymTab var_symbol_tab;
static FuncSymTab func_symbol_tab;
static std::stack< std::string > declared;
static int scope_level = 0;

inline std::string getTextType (DataType type)
{
  switch (type)
    {
      case CHAR_T: return "car";
      case INT_T: return "int";
      case CHAR_ARRAY_T: return "car[]";
      case INT_ARRAY_T: return "int[]";
    }
}

inline std::string getTextOperand (Op operand)
{
  switch (operand)
    {
      case PLUS: return "+";
      case MINUS: return "-";
      case TIMES: return "*";
      case DIVIDES: return "/";
      case MOD: return "%";
      case GREATER: return ">";
      case LESS: return "<";
      case EQUALS: return "==";
      case NOT_EQUAL: return "!=";
      case LESS_EQUAL: return "<=";
      case GREATER_EQUAL: return ">=";
      case LOGICAL_OR: return "||";
      case LOGICAL_AND: return "&&";
      case NOT: return "!";
    }
}

class ASTNode
{
  protected:
    std::vector< ASTNode* > child;
    int code_location;
    bool is_empty_prod;
  public:
    ASTNode () { child.clear(); }
    virtual void add (ASTNode *node) { child.push_back (node); }
    void set_location (int line_number) { code_location = line_number; }
    void set_empty_prod () { is_empty_prod = true; }
    void reverse () { std::reverse (child.begin (), child.end ()); }
    virtual void walk (int depth)
      {
        for (size_t i = 0; i < child.size (); i++)
          child[i]->walk (depth + 1);
      }
#ifdef DEBUG
    virtual std::string getNodeName ()
      {
        return "Ordinary";
      }
    virtual void print (int depth)
      {
        for (size_t i = 0; i < depth * (PRINT_DESLOCATION + 2); i++)
          {
            if (i % 5 == 0)
              std::cout << "│";
            std::cout << " ";
          }
        std::cout << "├";
        for (size_t i = 0; i < PRINT_DESLOCATION; i++)
          std::cout << "─";
        std::cout << " " << getNodeName() << ":";
        std::cout << " @" << code_location;
        std::cout << " d:" << depth;
        std::cout << " c:" << child.size ();
        std::cout << std::endl;
        if (child.size () > 0)
          for (size_t i = 0; i < child.size (); i++)
            if (child[i] != NULL)
              child[i]->print (depth + 1);
      }
#endif
};

class Expr : public ASTNode
{
  protected:
    DataType expr_type;
  public:
    Expr (DataType data_type) : expr_type (data_type) { }
    Expr () : expr_type (INT_T) { }
    DataType getType () { return expr_type; }
    void walk (int depth)
      {
        for (size_t i = 0; i < child.size (); i++)
          child[i]->walk (depth + 1);
      }
#ifdef DEBUG
    virtual std::string getNodeName ()
      {
        return "Expr";
      }
#endif
};

class Id : public ASTNode
{
  protected:
    DataType var_type;
    std::string *var_name;
  public:
    Id (std::string *identifier, ASTNode *array_pos = NULL) : var_name (identifier)
      {
        child.resize (1);
        child[0] = array_pos;
      }
    DataType getVarType () { return var_type; }
    std::string *getVarName () { return this->var_name; }
    void walk (int depth)
      {
        DataType type;
        if (!var_symbol_tab[*var_name].empty ()
            && var_symbol_tab.find (*var_name) != var_symbol_tab.end ())
          type = var_symbol_tab[*var_name].top ().first;
        else
          {
            std::string message = "Não declarado em escopo: " + *var_name + ".";
            yyerror (message.c_str (), code_location);
          }
        if (type == INT_ARRAY_T || type == CHAR_ARRAY_T)
          {
            if (child[0] == NULL)
              {
                std::string message = "Vetor não indexado: " + *var_name + ".";
                yyerror (message.c_str (), code_location);
              }
            else
              {
                Expr *position = static_cast<Expr*>(child[0]);
                position->walk (depth + 1);
                if (position->getType () != INT_T)
                  {
                    std::string message = "Indexação deve ser feita em número natural: " +
                      *var_name + ".";
                    yyerror (message.c_str (), code_location);
                  }
              }
              // For the nodes above
              if (type == INT_ARRAY_T)
                type = INT_T;
              if (type == CHAR_ARRAY_T)
                type = CHAR_T;
          }
          this->var_type = type;
      }
#ifdef DEBUG
    virtual std::string getNodeName ()
      {
        return "Id";
      }
#endif
};

class ListCommand : public ASTNode
{
  public:
    const std::vector<ASTNode*>& getChildren ()
      {
        return this->child;
      }
    void walk (int depth)
      {
        for (size_t i = 0; i < child.size (); i++)
          child[i]->walk (depth + 1);
      }
#ifdef DEBUG
    virtual std::string getNodeName ()
      {
        return "ListCommand";
      }
#endif
};

class DeclVarList : public ASTNode {
  public:
    void walk (int depth)
      {
        for (size_t i = 0; i < child.size (); i++)
          child[i]->walk (depth + 1);
      }
#ifdef DEBUG
    virtual std::string getNodeName ()
      {
        return "DeclVarList";
      }
#endif
};

class Command : public ASTNode {
  public:
    void walk (int depth)
      { }
#ifdef DEBUG
    virtual std::string getNodeName ()
      {
        return "Command";
      }
#endif
};

class Return : public Command
{
  protected:
    Expr *return_value;
    DataType return_type;
  public:
    Return (ASTNode *expr) : return_value (static_cast<Expr*> (expr)) { }
    DataType getReturnType () { return this->return_type; }
    void walk (int depth)
      {
        return_value->walk (depth + 1);
        this->return_type = return_value->getType();
      }
#ifdef DEBUG
    virtual std::string getNodeName ()
      {
        return "Return";
      }
#endif
};

class BlockStructure
{
  protected:
    bool has_return;
    DataType return_type;
    bool return_error;
  public: 
    BlockStructure () : has_return (false), return_error (false) { }
    bool hasReturn () { return has_return; }
    DataType getReturnType () { return return_type; }
    bool hasError () { return return_error; }
};

class Block : public Command, public BlockStructure
{  
  public:
    Block (DeclVarList *var_decl, ListCommand *statements = NULL)
      {
        child.resize (2);
        child[0] = var_decl;
        child[1] = statements;
      }
    Block (ListCommand *statements)
      {
        child.resize (2);
        child[0] = NULL;
        child[1] = statements;
      }
    void walk (int depth)
      {
        scope_level++;
        declared.push ("#");
        this->has_return = false;
        if (child[0] != NULL)
          child[0]->walk (depth + 1);
        if (child[1] != NULL)
          {
            child[1]->walk (depth + 1);
            Return* returnee;
            BlockStructure* block;
            ListCommand* statement = static_cast<ListCommand*>(child[1]);
            const std::vector<ASTNode*> children = statement->getChildren ();
            for (size_t i = 0; i < children.size (); ++i)
              {
                returnee = dynamic_cast<Return*>(children[i]);
                if (returnee != NULL)
                  if (!has_return)
                    {
                      this->has_return = true;
                      this->return_type = returnee->getReturnType ();
                    }
                  else if (return_type != returnee->getReturnType ())
                    this->return_error = true;
                else
                  {
                    block = dynamic_cast<BlockStructure*>(children[i]);
                    if (block != NULL)
                      {
                        if (block->hasReturn ())
                          {
                            if (this->has_return && this->return_type != block->getReturnType ())
                                this->return_error = true;
                            else
                              {
                                this->return_error |= block->hasError ();
                                this->return_type = block->getReturnType ();
                              }
                            this->has_return = true;
                          }
                      }
                  }
              }
          }
        scope_level--;
        while (declared.top () != "#")
          {
            std::string var_ident = declared.top ();
            declared.pop ();
            var_symbol_tab[var_ident].pop ();
            if (var_symbol_tab[var_ident].empty ())
              var_symbol_tab.erase (var_ident);
          }
        declared.pop ();
      }
#ifdef DEBUG
    virtual std::string getNodeName ()
      {
        return "Block";
      }
#endif
};

class ConstExpr : public Expr
{
  protected:
    std::string *value;
  public:
    ConstExpr (DataType data_type, std::string *lvalue) : Expr (data_type), value (lvalue) { }
    int getIntValue ()
      {
        std::istringstream iss(*value);
        int value;
        iss >> value;
        return value;
      }
    std::string getStringValue()
      {
        return *value;
      }
    char getCharValue ()
      {
        if (value->at (0) == '\\')
          {
            switch (value->at (1))
              {
                case '0': return '\0';
                case 'n': return '\n';
                case 't': return '\t';
                case 'a': return '\a';
                case 'r': return '\r';
                case 'b': return '\b'; 
                case 'f': return '\f';
                case '\\': return '\\';
              }
          }
        return value->at (0);
      }
#ifdef DEBUG
    virtual std::string getNodeName ()
      {
        return "ConstExpr";
      }
#endif
};

class DeclId : public ASTNode
{
  protected:
    ConstExpr *var_size;
    std::string *var_name;
  public:
    DeclId (std::string *identifier) : var_name(identifier) { var_size = NULL; }
    DeclId (std::string *identifier, ASTNode *array_size) : var_name (identifier), var_size (static_cast<ConstExpr*> (array_size)) { }
    DeclId (std::string *identifier, ConstExpr *array_size) : var_name (identifier), var_size (array_size) { }
    std::string *getVarName () { return this->var_name; }
    int getVarSize () { return this->var_size->getIntValue(); }
    bool isArray () { return (var_size != NULL); }
    void walk (int depth, DataType var_type)
      {
        if (func_symbol_tab.find (*var_name) != func_symbol_tab.end ())
          {
            std::string message = "Redeclaração: " + *var_name + ".";
            yyerror (message.c_str (), code_location);
          }
        if (var_symbol_tab.find (*var_name) != var_symbol_tab.end ()
            && var_symbol_tab[*var_name].top ().second == scope_level)
          {
            std::string message = "Redeclaração: " + *var_name + "."; 
            yyerror (message.c_str (), code_location);
          }
        if (var_size != NULL)
          {
            if (var_size->getType () != INT_T)
              {
                std::string message = "Declaração de vetor: " + *var_name +
                  ": o tamanho do vetor deve ser um número natural.";
                yyerror (message.c_str (), code_location);
              }
            if (var_type == INT_T)
              var_type = INT_ARRAY_T;
            if (var_type == CHAR_T)
              var_type = CHAR_ARRAY_T;
          }
          var_symbol_tab[*var_name].push (std::make_pair (var_type, scope_level));
          declared.push (*var_name);
      }
#ifdef DEBUG
    virtual std::string getNodeName ()
      {
        return "DeclId";
      }
#endif
};

class DeclVar : public ASTNode
{
  protected:
    DataType var_type;
  public:
    void setDataType (DataType data_type) { var_type = data_type; }
    void walk (int depth)
      {
        for (size_t i = 0; i < child.size (); i++)
          ((DeclId*) child[i])->walk (depth + 1, var_type);
      }
#ifdef DEBUG
    virtual std::string getNodeName ()
      {
        return "DeclVar";
      }
#endif
};

class Read : public Command
{
  protected:
    Id *var_id;
  public:
    Read (Id *identifier) : var_id (identifier) { }
    void walk (int depth)
      {
        var_id->walk (depth + 1);
      }
#ifdef DEBUG
    virtual std::string getNodeName ()
      {
        return "Read";
      }
#endif
};

class Write : public Command
{
  public:
    Write () { }
    Write (ASTNode *expr)
      {
        child.resize (1);
        child[0] = expr;
      }
    void walk (int depth)
      {
        child[0]->walk (depth + 1);
      }
#ifdef DEBUG
    virtual std::string getNodeName ()
      {
        return "Write";
      }
#endif
};

class If : public Command, public BlockStructure
{
  public:
    If (ASTNode *expr, ASTNode *statement, ASTNode *else_block = NULL)
      {
        child.resize (3);
        child[0] = expr; 
        child[1] = statement;
        child[2] = else_block;
      }
    void walk (int depth)
      {
        for (size_t i = 0; i < 2; i++)
          child[i]->walk (depth + 1);
        Block *block = dynamic_cast<Block*>(child[1]);
        if (block != NULL)
          {
            this->has_return = block->hasReturn ();
            this->return_error = block->hasError ();
            this->return_type = block->getReturnType ();
          }
        else if (dynamic_cast<Return*>(child[1]) != NULL)
          {
            Return *returnee = static_cast<Return*>(child[1]);
            if (this->has_return && returnee->getReturnType () != this->return_type)
                this->return_error = true;
            this->has_return = true;
            this->return_type = returnee->getReturnType ();
          }
        if (child[2] != NULL)
          {
            child[2]->walk (depth + 1);
            block = dynamic_cast<Block*>(child[2]);
            if (block != NULL)
              {
                if (this->has_return && block->getReturnType () != this->return_type)
                  this->return_error = true;
                this->has_return |= block->hasReturn ();
                this->return_error |= block->hasError ();
                this->return_type = block->getReturnType ();
              }
            else if (dynamic_cast<Return*>(child[2]) != NULL)
              {
                Return * returnee = static_cast<Return*>(child[2]);
                if (this->has_return && returnee->getReturnType () != this->return_type)
                  this->return_error = true;
                this->has_return = true;
                this->return_type = returnee->getReturnType ();
              }
          }
      }
#ifdef DEBUG
    virtual std::string getNodeName ()
      {
        return "If";
      }
#endif
};

class While : public Command, public BlockStructure
{
  public:
    While (ASTNode *expr, ASTNode *statement)
      {
        child.resize (2);
        child[0] = expr;
        child[1] = statement;
      }
    void walk (int depth)
      {
        for (size_t i = 0; i < child.size (); i++)
          child[i]->walk (depth + 1);
        Block *block = dynamic_cast<Block*>(child[1]);
        if (block != NULL)
          {
            this->has_return = block->hasReturn ();
            this->return_error = block->hasError ();
            this->return_type = block->getReturnType ();
          }
        else if (dynamic_cast<Return*>(child[1]) != NULL)
          {
            Return *returnee = static_cast<Return*>(child[1]);
            this->has_return = true;
            this->return_type = returnee->getReturnType ();
          }
      }
#ifdef DEBUG
    virtual std::string getNodeName ()
      {
        return "While";
      }
#endif
};

class AssignExpr : public Expr
{
  public:
    AssignExpr (ASTNode *left, ASTNode *right) : Expr (static_cast<Id*>(left)->getVarType ())
      {
        child.resize (2);
        child[0] = left;
        child[1] = right;
      }
    void walk (int depth)
      {
        for (size_t i = 0; i < child.size (); i++)
          child[i]->walk (depth + 1);
        Id *left = static_cast<Id*>(child[0]);
        Expr *right = static_cast<Expr*>(child[1]);
        if (left->getVarType () != right->getType ())
          {
            //TODO An error occurs when one expression is made
            std::string message = "Atribuição feita entre identificador e ";
            message = message + "expressão de tipos diferentes: ";
            message = message + getTextType (left->getVarType ());
            message = message + " e ";
            message = message + getTextType (right->getType ()) + ".";
            yyerror (message.c_str (), code_location);
          }
        else
          this->expr_type = left->getVarType ();
      }
#ifdef DEBUG
    virtual std::string getNodeName ()
      {
        return "AssignExpr";
      }
#endif
};

class TerExpr : public Expr
{
  public:
    TerExpr (ASTNode *expr, ASTNode *left_statement, ASTNode *right_statement)
      {
        child.resize (3);
        child[0] = expr; 
        child[1] = left_statement;
        child[2] = right_statement;
      }
    void walk (int depth)
      {
        for (size_t i = 0; i < child.size (); i++)
          child[i]->walk (depth + 1);
        if (static_cast<Expr*>(child[1])->getType () != static_cast<Expr*>(child[2])->getType ())
          {
            std::string message = "Retorno de operador ternário ambíguo: " +
              getTextType (static_cast<Expr*>(child[0])->getType ()) +
              " e " +
              getTextType (static_cast<Expr*>(child[1])->getType ()) +
              ".";
            yyerror (message.c_str (), code_location);
          }
        else
          this->expr_type = static_cast<Expr*>(child[0])->getType();
        printf ("oi, TerExpr\n");
      }
#ifdef DEBUG
    virtual std::string getNodeName ()
      {
        return "TerExpr";
      }
#endif
};

class BinExpr : public Expr
{
  protected:
    Op operand;
  public:
    BinExpr (Op op, ASTNode *left, ASTNode *right) : Expr (static_cast<Expr*> (left)->getType ()), operand (op)
      {
        child.resize (2);
        child[0] = left;
        child[1] = right;
      }
    void walk (int depth)
      {
        for (size_t i = 0; i < child.size (); i++)
          child[i]->walk (depth + 1);
        if (operand != LOGICAL_AND && operand != LOGICAL_OR &&
            static_cast<Expr*>(child[0])->getType () != static_cast<Expr*>(child[1])->getType ())
          {
            std::string message = "Operação incompatível entre " +
              getTextType (static_cast<Expr*>(child[0])->getType ()) +
              " e " +
              getTextType (static_cast<Expr*>(child[1])->getType ()) +
              ".";
            yyerror (message.c_str (), code_location);
          }
        else
          this->expr_type = static_cast<Expr*>(child[0])->getType();
      }
#ifdef DEBUG
    virtual std::string getNodeName ()
      {
        return "BinExpr";
      }
#endif
};

class UnExpr : public Expr
{
  protected:
    Op operand;
  public:
    UnExpr (Op op, ASTNode *expr) : Expr (static_cast<Expr*> (expr)->getType ()), operand (op)
      {
        child.resize (1);
        child[0] = expr;
      }
    void walk (int depth)
      {
        child[0]->walk (depth + 1);
        this->expr_type = ((Expr *) child[0])->getType();
        if (this->expr_type == CHAR_T && operand == MINUS)
          yyerror ("Negativo não aplicável sobre caracteres.", code_location);
      }
#ifdef DEBUG
    virtual std::string getNodeName ()
      {
        return "UnExpr";
      }
#endif
};

class Param : public ASTNode
{ 
  protected:
    DataType param_type;
    std::string *param_name;
  public:
    Param (DataType data_type, std::string *param_ident) : param_type (data_type), param_name (param_ident) { }
    const std::string *getParamName () { return param_name; }
    DataType getParamType () { return param_type; }
    DataType getType () { return this->param_type; }
    void walk (int depth) { }
#ifdef DEBUG
    virtual std::string getNodeName ()
      {
        return "Param";
      }
#endif
};

class ListParam : public ASTNode
{
  public:
    const std::vector<ASTNode*>& getChild ()
      {
        return this->child;
      }
    void walk (int depth)
      {
        Param *param;
        for (size_t i = 0; i < child.size (); i++)
          {
            child[i]->walk (depth + 1);
            param = static_cast<Param*>(child[i]);
            if (var_symbol_tab.find (*param->getParamName ()) != var_symbol_tab.end ())
              {
                std::string message = "Redeclaração de parâmetro: " +
                  *param->getParamName () + ".";
                yyerror (message.c_str (), code_location);
              }
            declared.push (*param->getParamName ());
            var_symbol_tab [*param->getParamName()].push (std::make_pair (param->getParamType (), scope_level));
          }
      }
#ifdef DEBUG
    virtual std::string getNodeName ()
      {
        return "ListParam";
      }
#endif
};

class ListArg : public ASTNode
{
  public:
    std::vector<ASTNode*>& getChild()
      {
        return this->child;
      }
    void walk (int depth)
      {
        for (size_t i = 0; i < child.size (); i++)
          child[i]->walk (depth + 1);
      }
#ifdef DEBUG
    virtual std::string getNodeName ()
      {
        return "ListArg";
      }
#endif
};

class DeclFunc : public ASTNode
{
  protected:
    DataType func_type;
    std::string *func_name;
  public:
    DeclFunc (ASTNode *params, ASTNode *block)
      {
        child.resize (2);
        child[0] = params;
        child[1] = block;
      }
    void setFuncName (std::string *func_ident)
      {
        func_name = func_ident;
      }
    void setDataType (DataType data_type) { func_type = data_type; }
    DataType getType () { return this->func_type; }
    ListParam *getListParam () { return static_cast<ListParam*> (this->child[0]); }
    void walk (int depth)
      {
        if (var_symbol_tab.find (*func_name) != var_symbol_tab.end ())
          {
            std::string message = "Nome de função já associado a variável: " + *func_name + ".";
            yyerror (message.c_str (), code_location);
          }
      
        if (func_symbol_tab.find (*func_name) != func_symbol_tab.end ())
          {
            std::string message = "Redeclaração de função: " + *func_name + ".";
            yyerror (message.c_str(), code_location);
          }
        else
          func_symbol_tab[*func_name] = this;
        scope_level++;
        declared.push ("#");
        if (child[0] != NULL)
          child[0]->walk (depth + 1);
        scope_level--;
        Block* block = static_cast<Block*>(child[1]);
        block->walk (depth + 1);
      
        if (block->hasReturn ())
          {
            if (block->hasError())
              {
                std::string message = "Tipo de retorno e assinatura de função conflitantes: " + *func_name + ".";
                yyerror (message.c_str (), code_location);
              }
            else if (block->getReturnType() != this->func_type)
              {
                std::string message = "Tipo de retorno e assinatura de função conflitantes: " + *func_name + ".";
                yyerror (message.c_str (), code_location);
              }
          }
        else
          {
            std::string message = "Tipo de retorno " + getTextType (this->func_type) + " faltante: " + *func_name + ".";
            yyerror (message.c_str (), code_location);
          }
        while (declared.top () != "#")
          {
            std::string var_ident = declared.top();
            declared.pop();
            var_symbol_tab[var_ident].pop();
            if (var_symbol_tab[var_ident].empty ())
              var_symbol_tab.erase (var_ident);
          }
        declared.pop();
      }
#ifdef DEBUG
    virtual std::string getNodeName ()
      {
        return "DeclFunc";
      }
#endif
};

class FuncId : public Expr
{
  protected:
    std::string *func_identifier;
  public:
    FuncId (std::string *func_name, ASTNode *args = NULL)
      {
        child.resize(1);
        child[0] = args;
        this->func_identifier = func_name;
      }
    void walk (int depth)
      {
        if (func_symbol_tab.find (*func_identifier) != func_symbol_tab.end ())
          {
            DeclFunc* func = func_symbol_tab[*func_identifier];
            ListArg* args = static_cast<ListArg*>(child[0]);
            if (func->getListParam () == NULL && args != NULL)
              {
                std::string message = "Função sem argumentos: " + *func_identifier + ".";
                yyerror (message.c_str (), code_location);
              }
            else if (func->getListParam () != NULL && args == NULL)
              {
                std::string message = "Nenhum argumento fornecido: " + *func_identifier + "." ;
                yyerror (message.c_str (), code_location);
              }
            else if ((func->getListParam () != NULL && args != NULL)
                && (func->getListParam ()->getChild ().size () != args->getChild ().size ()))
              {
                std::string message = "Número de argumentos conflitante com assinatura da função: " + *func_identifier + ".";
                yyerror (message.c_str (), code_location);
              }
            else if (func->getListParam () != NULL && args != NULL)
              {
                child[0]->walk (depth + 1);
                const std::vector<ASTNode*>& paramChildren = func->getListParam ()->getChild ();
                const std::vector<ASTNode*>& argChildren = args->getChild ();
                Expr* argument;
                Param* parameter;
                for (int i = 0; i < paramChildren.size(); ++i)
                  {
                    parameter = static_cast<Param*>(paramChildren[i]);
                    argument = static_cast<Expr*>(argChildren[i]);
                    if (parameter->getParamType () != argument->getType ())
                      {
                        std::string message = "Tipo de argumento e parâmetro incompatíveis em função: " + *func_identifier + ".";
                        yyerror (message.c_str (), code_location);
                      }
                  }
              }
            this->expr_type = func->getType();
          }
        else
          {
            std::string message = "Função não declarada: " + *func_identifier + ".";
            yyerror (message.c_str (), code_location);
          }
      }
#ifdef DEBUG
    virtual std::string getNodeName ()
      {
        return "FuncId";
      }
#endif
};

#endif
  