
parser grammar PostgreSQLParser;

options
   { tokenVocab = PostgreSQLLexer; }

//////////////////////////////////////////////////////////////////////////////

relational_op:
	  EQ | LTH | GTH | NOT_EQ | LET | GET;

cast_data_type:
    BINARY (LPAREN INTEGER_NUM RPAREN)?
    | CHAR (LPAREN INTEGER_NUM RPAREN)?
    | DATE_SYM
    | DATETIME
    | DECIMAL_SYM (LPAREN INTEGER_NUM (COMMA INTEGER_NUM)? RPAREN)?
    | SIGNED_SYM (INTEGER_SYM)?
    | TIME_SYM
    | UNSIGNED_SYM (INTEGER_SYM)? ;

search_modifier:
	  (IN_SYM NATURAL LANGUAGE MODE_SYM ( WITH QUERY_SYM EXPANSION_SYM )?)
	| (IN_SYM BOOLEAN_SYM MODE_SYM)
	| (WITH QUERY_SYM EXPANSION_SYM) ;

interval_unit:
	  SECOND | MINUTE | HOUR | DAY_SYM | WEEK | MONTH | QUARTER | YEAR
    | SECOND_MICROSECOND | MINUTE_MICROSECOND | MINUTE_SECOND
    | HOUR_MICROSECOND | HOUR_SECOND | HOUR_MINUTE | DAY_MICROSECOND
    | DAY_SECOND | DAY_MINUTE | DAY_HOUR | YEAR_MONTH ;

transcoding_name:
	  LATIN1 | UTF8 ;


//////////////////////////////////////////////////////////////////////////////
// LITERALS

bit_literal:		    BIT_NUM ;
boolean_literal:	    TRUE_SYM | FALSE_SYM ;
hex_literal:		    HEX_DIGIT ;
number_literal:		    ( PLUS | MINUS )? ( INTEGER_NUM | REAL_NUMBER ) ;
string_literal:		    TEXT_STRING ;


//////////////////////////////////////////////////////////////////////////////
// FUNCTIONS

char_functions:
	  ASCII_SYM | BIN | BIT_LENGTH | CHAR_LENGTH | CHAR | CONCAT_WS | CONCAT
    | ELT | EXPORT_SET | FIELD | FIND_IN_SET | FORMAT | FROM_BASE64 | HEX
    | INSERT | INSTR | LEFT | LENGTH | LOAD_FILE | LOCATE | LOWER | LPAD
    | LTRIM | MAKE_SET | MID | OCT | ORD | QUOTE | REPEAT | REPLACE | REVERSE
    | RIGHT | RPAD | RTRIM | SOUNDEX | SPACE | STRCMP | SUBSTRING_INDEX
    | SUBSTRING | TO_BASE64 | TRIM | UNHEX | UPPER | WEIGHT_STRING ;

group_functions:
	  AVG | COUNT | MAX_SYM | MIN_SYM | SUM | BIT_AND | BIT_OR | BIT_XOR
    | BIT_COUNT | GROUP_CONCAT | STD | STDDEV | STDDEV_POP | STDDEV_SAMP
    | VAR_POP | VAR_SAMP | VARIANCE ;

number_functions:
	  ABS | ACOS | ASIN | ATAN2 | ATAN | CEIL | CEILING | CONV | COS | COT
    | CRC32 | DEGREES | EXP | FLOOR | LN | LOG10 | LOG2 | LOG | MOD | PI | POW
    | POWER | RADIANS | RAND | ROUND | SIGN | SIN | SQRT | TAN | TRUNCATE ;

other_functions:
	  MAKE_SET | LOAD_FILE | IF | IFNULL | AES_ENCRYPT | AES_DECRYPT | DECODE
    | ENCODE | DES_DECRYPT | DES_ENCRYPT | ENCRYPT | MD5 | OLD_PASSWORD
    | PASSWORD | BENCHMARK | CHARSET | COERCIBILITY | COLLATION | CONNECTION_ID
	| CURRENT_USER | DATABASE | SCHEMA | USER | SESSION_USER | SYSTEM_USER
	| VERSION_SYM | FOUND_ROWS | LAST_INSERT_ID | DEFAULT | GET_LOCK
    | RELEASE_LOCK | IS_FREE_LOCK | IS_USED_LOCK | MASTER_POS_WAIT | INET_ATON
    | INET_NTOA | NAME_CONST | SLEEP | UUID | VALUES ;

time_functions:
	  ADDDATE | ADDTIME | CONVERT_TZ | CURDATE | CURTIME | DATE_ADD
    | DATE_FORMAT | DATE_SUB | DATE_SYM | DATEDIFF | DAYNAME | DAYOFMONTH
    | DAYOFWEEK | DAYOFYEAR | EXTRACT | FROM_DAYS | FROM_UNIXTIME | GET_FORMAT
    | HOUR | LAST_DAY | MAKEDATE | MAKETIME | MICROSECOND | MINUTE | MONTH
    | MONTHNAME | NOW | PERIOD_ADD | PERIOD_DIFF | QUARTER | SEC_TO_TIME
    | SECOND | STR_TO_DATE | SUBTIME | SYSDATE | TIME_FORMAT | TIME_TO_SEC
    | TIME_SYM | TIMEDIFF | TIMESTAMP | TIMESTAMPADD | TIMESTAMPDIFF | TO_DAYS
    | TO_SECONDS | UNIX_TIMESTAMP | UTC_DATE | UTC_TIME | UTC_TIMESTAMP | WEEK
    | WEEKDAY | WEEKOFYEAR | YEAR | YEARWEEK ;

//pg_sphere_data_type:
//      SPOINT | SCIRCLE | SLINE | SELLIPSE | SPOLY | SPATH | SBOX ;

pg_sphere_functions:
      AREA ;

functionList:
	  number_functions | char_functions | time_functions | other_functions
    | pg_sphere_functions ;


literal_value:
      string_literal | number_literal | hex_literal | boolean_literal
    | bit_literal | NULL_SYM ;


//////////////////////////////////////////////////////////////////////////////
// MAIN

select_expression:
	SELECT 

	( ALL | DISTINCT | DISTINCTROW )?
	( HIGH_PRIORITY )?
	( STRAIGHT_JOIN )?
	( SQL_SMALL_RESULT )? ( SQL_BIG_RESULT )? ( SQL_BUFFER_RESULT )?
	( SQL_CACHE_SYM | SQL_NO_CACHE_SYM )? ( SQL_CALC_FOUND_ROWS )?
   
    select_list
	
	(
		FROM table_references
		( partition_clause )?
		( where_clause )?
		( groupby_clause )?
		( having_clause )?
	) ?

    ( orderby_clause )?
    ( limit_clause )?
	( ( FOR_SYM UPDATE ) | ( LOCK IN_SYM SHARE_SYM MODE_SYM ) )?

    SEMI?
;


//////////////////////////////////////////////////////////////////////////////
// TOKENS

alias:                  ( AS_SYM )? ID ;
bit_expr:               factor1 ( VERTBAR factor1 )? ;

bool_primary:
      predicate ( relational_op predicate )? | ( ( NOT_SYM )? EXISTS subquery);

case_when_statement:    CASE_SYM ( case_when_statement1 | case_when_statement2 )
                            ( ELSE_SYM bit_expr )? END_SYM;
case_when_statement1:   ( WHEN_SYM expression THEN_SYM bit_expr )+ ;
case_when_statement2:   bit_expr ( WHEN_SYM bit_expr THEN_SYM bit_expr )+ ;
column_list:            LPAREN column_spec ( COMMA column_spec )* RPAREN ;
column_name:            ID ;
column_spec:            ( ( schema_name DOT )? table_name DOT )? column_name ;

displayed_column :      ( table_spec DOT ASTERISK ) | ( ( bit_expr | sbit_expr ) ( alias )? ) ;

exp_factor1:	        exp_factor2 ( XOR exp_factor2 )* ;
exp_factor2:	        exp_factor3 ( AND_SYM exp_factor3 )* ;
exp_factor3:	        ( NOT_SYM )? exp_factor4 ;
exp_factor4:	        bool_primary ( ( IS_SYM ( NOT_SYM )? (boolean_literal | NULL_SYM | ( DISTINCT FROM ) ) )?
                                     | ( ISNULL | NOTNULL )?
                                     );
expression:	            (exp_factor1 ( OR_SYM exp_factor1 )* ) | ( sbit_expr );
expression_list:        LPAREN expression ( COMMA expression )* RPAREN ;

//factor0:                (factor1 ( pg_sphere_op factor1 )? ) | (;
factor1:                factor2 ( BITAND factor2 )? ;
factor2:                factor3 ( ( SHIFT_LEFT | SHIFT_RIGHT ) factor3 )? ;
factor3:                factor4 ( ( PLUS | MINUS ) factor4 )* ;
factor4:                factor5 ( ( ASTERISK | DIVIDE | MOD_SYM | POWER_OP) factor5 )* ;
factor5:                ( PLUS | MINUS | NEGATION | BINARY )? simple_expr
                            ( ( PLUS | MINUS ) interval_expr )? ;
function_call:
	  ( functionList ( LPAREN ( expression ( COMMA expression )* )? RPAREN ) ? )
	| ( CONVERT_SYM LPAREN expression COMMA cast_data_type RPAREN )
	| ( CONVERT_SYM LPAREN expression USING_SYM transcoding_name RPAREN )
	| ( CAST_SYM LPAREN expression AS_SYM cast_data_type RPAREN ) 
	| ( group_functions LPAREN ( ASTERISK | ALL | DISTINCT )? ( bit_expr )? RPAREN ) ;

groupby_clause:         GROUP_SYM BY_SYM groupby_item ( COMMA groupby_item )* ( WITH ROLLUP_SYM )? ;
groupby_item:	        (column_spec | INTEGER_NUM | bit_expr ) ( ASC | DESC )?;

having_clause:          HAVING expression ;


index_hint:
	  USE_SYM    index_options LPAREN ( index_list )? RPAREN
	| IGNORE_SYM index_options LPAREN index_list RPAREN
	| FORCE_SYM  index_options LPAREN index_list RPAREN ;
index_hint_list:        index_hint ( COMMA index_hint )* ;
index_name:             ID ;
index_list:             index_name ( COMMA index_name )* ;
index_options:          ( INDEX_SYM | KEY_SYM ) ( FOR_SYM (( JOIN_SYM ) | ( ORDER_SYM BY_SYM ) | ( GROUP_SYM BY_SYM )) )? ;

interval_expr:          INTERVAL_SYM expression interval_unit ;

join_condition:         ( ON expression ) | ( USING_SYM column_list ) ;

limit_clause:           LIMIT (( offset COMMA )? row_count) | ( row_count OFFSET_SYM offset ) ;

match_against_statement:MATCH ( column_spec ( COMMA column_spec )* ) AGAINST ( expression ( search_modifier )? ) ;

offset:		            INTEGER_NUM ;
row_count:	            INTEGER_NUM ;

orderby_clause:         ORDER_SYM BY_SYM orderby_item ( COMMA orderby_item )* ;
orderby_item:	        groupby_item ( ( ASC | DESC )? | ( NULLS_SYM ( FIRST_SYM | LAST_SYM ) )? ) | groupby_item USING_SYM ( GTH | LTH );

partition_clause:       PARTITION_SYM LPAREN partition_names RPAREN ;
partition_name:         ID ;
partition_names:	    partition_name ( COMMA partition_name )* ;

bit_fac1:
      ( NOT_SYM )? (
          (IN_SYM ( subquery | expression_list ))
        | (LIKE_SYM simple_expr ( ESCAPE_SYM simple_expr )?)
        | (REGEXP bit_expr)
        | (BETWEEN ( SYMMETRIC )? bit_expr AND_SYM predicate)
      ) ;

bit_fac2:               SOUNDS_SYM LIKE_SYM bit_expr;
predicate:
	  bit_expr (( bit_fac1 | bit_fac2)?) ;
      /*
	| ( bit_expr ( NOT_SYM )? IN_SYM ( subquery | expression_list ) ); //done
	| ( bit_expr ( NOT_SYM )? BETWEEN bit_expr AND_SYM predicate ) //done
	| ( bit_expr SOUNDS_SYM LIKE_SYM bit_expr ) //done
	| ( bit_expr ( NOT_SYM )? LIKE_SYM simple_expr ( ESCAPE_SYM simple_expr )? ) //done
	| ( bit_expr ( NOT_SYM )? REGEXP bit_expr ) //done
	| ( bit_expr ) ; //done
    */

query:                  select_statement SEMI;

schema_name:            ID ;
select_list:            ( displayed_column ( COMMA displayed_column )* ) |
                        ( ASTERISK ( COMMA displayed_column ( COMMA displayed_column )* )? ) ;
select_statement:       select_expression ( (UNION_SYM ( ALL )? ) select_expression )* ;

simple_expr:
	  literal_value
	| expression_list
	| column_spec 
	| function_call 
	//| USER_VAR
	| (ROW_SYM expression_list)
	| subquery
	| EXISTS subquery 
	| interval_expr
	| match_against_statement 
	| case_when_statement ;

subquery:               LPAREN select_statement RPAREN ;

table_atom:
	  ( table_spec ( partition_clause )? ( alias )? ( index_hint_list )? )
	| ( subquery alias )
	| ( LPAREN table_references RPAREN )
	| ( OJ_SYM table_reference LEFT OUTER JOIN_SYM table_reference ON expression ) ;
table_name:             ID ;

table_factor1:          table_factor2 ( (INNER_SYM | CROSS)? JOIN_SYM table_atom ( join_condition )? )* ;
table_factor2:          table_factor3 (  STRAIGHT_JOIN table_atom ( ON expression )? )? ;
table_factor3:          table_factor4 ( ( LEFT | RIGHT ) ( OUTER )? JOIN_SYM table_factor4 join_condition )* ;
table_factor4:          table_atom ( NATURAL ( ( LEFT | RIGHT ) ( OUTER )? )? JOIN_SYM table_atom )? ;

table_reference:        table_factor1 | ( LPAREN values_list RPAREN ) alias ( column_list )? ;
table_references:       table_reference ( COMMA table_reference )* ;
table_spec:             ( schema_name DOT )? table_name ;

values_list:            VALUES ( expression_list ( COMMA expression_list )* );

where_clause:           WHERE expression ;

pg_sphere_op:
      SCONTAINS | SCONTAINS2 | NEGATION | SLEFTCONTAINS2 | SNOTCONTAINS
    | SNOTCONTAINS2 | SLEFTNOTCONTAINS | SLEFTNOTCONTAINS2 | AND_SYM
    | SNOTOVERLAP ;

sbit_expr:
      ( pg_sphere_object | spoint )
    | ( ( spoint | simple_expr ) pg_sphere_op pg_sphere_object)
    | ( pg_sphere_object EQ pg_sphere_object )
    | ( pg_sphere_object pg_sphere_op pg_sphere_object )
    | ( sline | simple_expr SCROSS sline | simple_expr )
    | ( ( spoint | scircle | simple_expr ) SDISTANCE ( spoint | scircle | simple_expr ) )
    | ( SLENGTH ( scircle | sbox | spoly | simple_expr ) )
    | ( SCENTER ( scircle | sellipse | simple_expr ) )
    | ( MINUS ( sline | spath | simple_expr ) )
    | ( ( spoint | scircle | sline | sellipse | spoly | spath | simple_expr )? ( ( PLUS | MINUS )? strans )+ ) ;


spoint:                 SPOINT LPAREN bit_expr COMMA bit_expr RPAREN ;
scircle:                SCIRCLE LPAREN spoint COMMA bit_expr RPAREN ;
sline:                  ( SLINE LPAREN spoint COMMA spoint RPAREN ) | ( SLINE LPAREN strans COMMA bit_expr RPAREN );
sellipse:               SELLIPSE LPAREN spoint COMMA bit_expr COMMA bit_expr COMMA bit_expr RPAREN ;
sbox:                   SBOX LPAREN spoint COMMA spoint RPAREN ;
spoly:                  SPOLY TEXT_STRING| SPOLY LPAREN column_spec RPAREN | SPOLY LPAREN TEXT_STRING RPAREN;
spath:                  SPATH TEXT_STRING | SPATH LPAREN column_spec RPAREN ;
strans:                 STRANS LPAREN bit_expr COMMA bit_expr COMMA bit_expr COMMA TRANS RPAREN ;

pg_sphere_object:       scircle | sline | sellipse | sbox | spoly | spath | simple_expr;