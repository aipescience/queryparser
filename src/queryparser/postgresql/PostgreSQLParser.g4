
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
    | TIME_SYM
    | TIMESTAMP
    | INTERVAL_SYM
    | DECIMAL_SYM (LPAREN INTEGER_NUM (COMMA INTEGER_NUM)? RPAREN)?
    | INTEGER_SYM
    | BIGINT
    | FLOAT
    | REAL
    | DOUBLE_PRECISION_SYM;

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
	  ASCII_SYM | BIT_LENGTH | CHAR_LENGTH | CHR | CONCAT_WS | CONCAT
    | LEFT | LENGTH | LOWER | LPAD | LTRIM | REPEAT | REPLACE | REVERSE
    | RIGHT | RPAD | RTRIM | SUBSTRING | UPPER ;

group_functions:
	  AVG | COUNT | MAX_SYM | MIN_SYM | SUM | BIT_AND | BIT_OR
	| STDDEV | STDDEV_POP | STDDEV_SAMP | VAR_POP | VAR_SAMP | VARIANCE ;

number_functions:
	  ABS | ACOS | ASIN | ATAN2 | ATAN | CBRT | CEIL | CEILING | COS | COT
    | DEGREES | DIV | EXP | FLOOR | LN | LOG | MOD | PI | POW
    | POWER | RADIANS | RANDOM | ROUND | SIGN | SIN | SQUARE_DEGREES | SQRT
    | STERADIANS | TAN | TRUNCATE ;

other_functions:
      ENCODE | MD5 ;

time_functions:
      DATE_PART | DATE_SYM | NOW | SECOND | TIME_SYM | TIMESTAMP 
    | UTC_DATE | UTC_TIME | UTC_TIMESTAMP | YEAR ;

array_functions:
      ARRAY_LENGTH ;

custom_functions:
      GAIA_HEALPIX_INDEX | PDIST | UDF_0 | UDF_1 | UDF_2 | UDF_3 | UDF_4 | UDF_5 | UDF_6 | UDF_7 | UDF_8 | UDF_9 ;

pg_sphere_functions:
      AREA ;

functionList:
	  number_functions | char_functions | time_functions | other_functions
    | pg_sphere_functions | array_functions | custom_functions;

literal_value:
      string_literal | number_literal | hex_literal | boolean_literal
    | bit_literal | NULL_SYM ;


//////////////////////////////////////////////////////////////////////////////
// MAIN

select_expression:
	SELECT 
	( ALL | DISTINCT )?
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
    ( offset_clause )?
	( FOR_SYM UPDATE )?

    SEMI?
;


//////////////////////////////////////////////////////////////////////////////
// TOKENS

alias:                  ( AS_SYM )? ID ;
bit_expr:               factor1 ( VERTBAR factor1 )? ;

bool_primary:
      predicate ( relational_op ( ANY )? predicate )? | ( ( NOT_SYM )? EXISTS subquery);

case_when_statement:    CASE_SYM ( case_when_statement1 | case_when_statement2 )
                            ( ELSE_SYM bit_expr )? END_SYM;
case_when_statement1:   ( WHEN_SYM expression THEN_SYM bit_expr )+ ;
case_when_statement2:   bit_expr ( WHEN_SYM bit_expr THEN_SYM bit_expr )+ ;
column_list:            LPAREN column_spec ( COMMA column_spec )* RPAREN ;
column_name:            ID;
column_spec:            ( ( schema_name DOT )? table_name DOT )? column_name ( slice_spec )?;

displayed_column :      ( table_spec DOT ASTERISK )
                      | ( ( bit_expr | sbit_expr | displayed_column_arr ) ( ( LIKE_SYM | ILIKE_SYM ) TEXT_STRING )? ( alias )? ) ;

displayed_column_arr :
      ( spoint_to_array_deg | spoint_to_array
      | sbox_to_array_deg | sbox_to_array
      | scircle_to_array_deg | scircle_to_array
      | spoly_to_array_deg | spoly_to_array);

exp_factor1:	        exp_factor2 ( AND_SYM exp_factor2 )* ;
exp_factor2:	        ( NOT_SYM )? exp_factor3 ;
exp_factor3:	        bool_primary ( ( IS_SYM ( NOT_SYM )? (boolean_literal | NULL_SYM | ( DISTINCT FROM ) ) )?
                                     | ( ISNULL | NOTNULL )?
                                     );
expression:	            ( exp_factor1 ( OR_SYM exp_factor1 )* ) ;
expression_list:        LPAREN expression ( COMMA expression )* RPAREN ;

factor1:                factor2 ( BITAND factor2 )? ;
factor2:                factor3 ( ( SHIFT_LEFT | SHIFT_RIGHT ) factor3 )? ;
factor3:                factor4 ( ( PLUS | MINUS ) factor4 )* ;
factor4:                factor5 ( ( ASTERISK | DIVIDE | MOD_SYM | POWER_OP) factor5 )* ;
factor5:                ( PLUS | MINUS | NEGATION | BINARY | ABS_VAL_OR_SCONTAINS | DFACTORIAL )? simple_expr ( NOT_SYM )? ( ( PLUS | MINUS ) interval_expr )? ;

function_call:
	  ( functionList ( LPAREN ( expression ( COMMA expression )* )? RPAREN ) ? )
	| ( CAST_SYM LPAREN expression AS_SYM cast_data_type RPAREN )
	| ( CONVERT_SYM LPAREN TEXT_STRING COMMA TEXT_STRING COMMA TEXT_STRING RPAREN )
	| ( POSITION_SYM LPAREN expression IN_SYM expression RPAREN )
	| ( group_functions LPAREN ( ASTERISK | ALL | DISTINCT )? ( ( bit_expr | sbit_expr ) )? RPAREN ) ;

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

interval_expr:          INTERVAL_SYM string_literal;

join_condition:         ( ON expression ) | ( USING_SYM column_list ) ;

limit_clause:           ( LIMIT row_count ( OFFSET_SYM offset )? ) | ( OFFSET_SYM offset LIMIT row_count );

offset:		            INTEGER_NUM ;
offset_clause:          OFFSET_SYM offset ;
row_count:	            INTEGER_NUM ;

orderby_clause:         ORDER_SYM BY_SYM orderby_item ( COMMA orderby_item )* ;
orderby_item:	        groupby_item ( ( ASC | DESC )? | ( NULLS_SYM ( FIRST_SYM | LAST_SYM ) )? ) | groupby_item USING_SYM ( GTH | LTH );

partition_clause:       PARTITION_SYM LPAREN partition_names RPAREN ;
partition_name:         ID ;
partition_names:	    partition_name ( COMMA partition_name )* ;

bit_fac1:
      ( NOT_SYM )? (
          (IN_SYM ( subquery | expression_list ))
        | ((LIKE_SYM | ILIKE_SYM) simple_expr ( ESCAPE_SYM simple_expr )?)
        | (REGEXP ( bit_expr | sbit_expr ))
        | (BETWEEN ( SYMMETRIC )? ( bit_expr | sbit_expr ) AND_SYM predicate)
      ) ;

bit_fac2:               (SOUNDS_SYM ( LIKE_SYM | ILIKE_SYM ) ( bit_expr | sbit_expr ));
predicate:
	  ( bit_expr | sbit_expr ) (( bit_fac1 | bit_fac2)?) ;

query:                  select_statement SEMI;

schema_name:            ID ;
select_list:            ( displayed_column ( COMMA displayed_column )* ) |
                        ( ASTERISK ( COMMA displayed_column ( COMMA displayed_column )* )? ) |
                        ( ON (subselect_list) ( COMMA displayed_column )* );
subselect_list:         ( displayed_column ( COMMA displayed_column )* );
select_statement:       select_expression ( (UNION_SYM ( ALL )? ) select_expression )* ;

simple_expr:
      literal_value
    | expression_list
    | column_spec
    | function_call
    | (ROW_SYM expression_list)
    | subquery
    | EXISTS subquery
    | interval_expr
    | case_when_statement ;

slice_spec:             ( LBRACK INTEGER_NUM ( COLON INTEGER_NUM )? RBRACK )+;

subquery:               LPAREN select_statement RPAREN ;

table_atom:
	  ( table_spec ( partition_clause )? ( alias )? ( index_hint_list )? )
	| ( subquery alias )
	| ( LPAREN table_references RPAREN )
	| ( OJ_SYM table_reference LEFT OUTER JOIN_SYM table_reference ON expression ) ;
table_name:             ID ;

table_factor1:          table_factor2 ( (INNER_SYM | CROSS | LEFT | RIGHT)? JOIN_SYM table_atom ( join_condition )? )* ;
table_factor2:          table_factor3 (  STRAIGHT_JOIN table_atom ( ON expression )? )? ;
table_factor3:          table_factor4 ( ( LEFT | RIGHT ) ( OUTER )? JOIN_SYM table_factor4 join_condition )* ;
table_factor4:          table_atom ( NATURAL ( ( LEFT | RIGHT ) ( OUTER )? )? JOIN_SYM table_atom )? ;

table_reference:        table_factor1 | ( LPAREN values_list RPAREN ) alias ( column_list )? ;
table_references:       table_reference ( COMMA table_reference )* ;
table_spec:             ( schema_name DOT )? table_name ;

values_list:            VALUES ( expression_list ( COMMA expression_list )* );

where_clause:           WHERE expression ;

pg_sphere_op:
      ABS_VAL_OR_SCONTAINS | SCONTAINS2 | NEGATION | SLEFTCONTAINS2 | SNOTCONTAINS
    | SNOTCONTAINS2 | SLEFTNOTCONTAINS | SLEFTNOTCONTAINS2 | AND_SYM
    | SNOTOVERLAP ;


sbit_expr:
      ( polygon SLEFTCONTAINS2 point )
    | ( point SCONTAINS2 polygon )
    | ( pg_sphere_object | spoint )
    | ( ( spoint | simple_expr ) pg_sphere_op pg_sphere_object)
    | ( pg_sphere_object EQ pg_sphere_object )
    | ( pg_sphere_object pg_sphere_op pg_sphere_object )
    | ( sline | simple_expr SCROSS sline | simple_expr )
    | ( ( spoint | scircle | simple_expr ) SDISTANCE ( spoint | scircle | simple_expr ) )
    | ( SLENGTH ( scircle | sbox | spoly | simple_expr ) )
    | ( SCENTER ( scircle | sellipse | simple_expr ) )
    | ( MINUS ( sline | spath | simple_expr ) )
    | ( ( spoint | scircle | sline | sellipse | spoly | spath | simple_expr ) ( ( PLUS | MINUS )? strans )+ ) ;


polygon:                POLYGON string_literal ;
point:                  POINT LPAREN bit_expr COMMA bit_expr RPAREN ;
spoint:                 SPOINT LPAREN bit_expr COMMA bit_expr RPAREN ;
scircle:                SCIRCLE LPAREN spoint COMMA bit_expr RPAREN ;
sline:                  ( SLINE LPAREN spoint COMMA spoint RPAREN ) | ( SLINE LPAREN strans COMMA bit_expr RPAREN );
sellipse:               SELLIPSE LPAREN spoint COMMA bit_expr COMMA bit_expr COMMA bit_expr RPAREN ;
sbox:                   SBOX LPAREN spoint COMMA spoint RPAREN ;
spoly:                  SPOLY TEXT_STRING| SPOLY LPAREN column_spec RPAREN | SPOLY LPAREN TEXT_STRING RPAREN;
spath:                  SPATH TEXT_STRING | SPATH LPAREN column_spec RPAREN ;
strans:                 STRANS LPAREN bit_expr COMMA bit_expr COMMA bit_expr COMMA TRANS RPAREN ;
spoint_to_array:        SPOINT_TO_ARRAY LPAREN spoint RPAREN ;
spoint_to_array_deg:    SPOINT_TO_ARRAY_DEG LPAREN spoint RPAREN ;
sbox_to_array:          SBOX_TO_ARRAY LPAREN sbox RPAREN ;
sbox_to_array_deg:      SBOX_TO_ARRAY_DEG LPAREN sbox RPAREN ;
scircle_to_array:       SCIRCLE_TO_ARRAY LPAREN scircle RPAREN ;
scircle_to_array_deg:   SCIRCLE_TO_ARRAY_DEG LPAREN scircle RPAREN ;
spoly_to_array:         SPOLY_TO_ARRAY LPAREN spoly RPAREN ;
spoly_to_array_deg:     SPOLY_TO_ARRAY_DEG LPAREN spoly RPAREN ;

pg_sphere_object:       scircle | sline | sellipse | sbox | spoly | spath | simple_expr;
