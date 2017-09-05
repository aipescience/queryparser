
parser grammar MySQLParser;

options
   { tokenVocab = MySQLLexer; }

//////////////////////////////////////////////////////////////////////////////

relational_op:
	  EQ | LTH | GTH | NOT_EQ | LET | GET ;

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



// LITERALS

bit_literal:		    BIT_NUM ;
boolean_literal:	    TRUE_SYM | FALSE_SYM ;
hex_literal:		    HEX_DIGIT ;
number_literal:		    ( PLUS | MINUS )? ( INTEGER_NUM | REAL_NUMBER ) ;
string_literal:		    TEXT_STRING ;



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

mysql_sphere_functions:
      SDIST | SAREA | SCENTER | SCIRCUM | SLENGTH | SSWAP | SNPOINTS | SSTR
    | MYSQL_SPHERE_VERSION | SRCONTAINSL | SLCONTAINSR | SRNOTCONTAINSL
    | SLNOTCONTAINSR | SOVERLAPS | SNOTOVERLAPS | SEQUAL | SNOTEQUAL
    | STRANSFORM | SINVERSE | SPOINT | SPOINT_LONG | SPOINT_LAT | SPOINT_X
    | SPOINT_Y | SPOINT_Z | SPOINT_EQUAL | STRANS | STRANS_POINT
    | STRANS_POINT_INVERSE | STRANS_EQUAL | STRANS_EQUAL_NEG | STRANS_PHI
    | STRANS_THETA | STRANS_PSI | STRANS_AXES | STRANS_INVERT | STRANS_ZXZ
    | STRANS_TRANS | STRANS_TRANS_INV | SCIRCLE | SCIRCLE_RADIUS
    | SCIRCLE_EQUAL | SCIRCLE_EQUAL_NEG | SCIRCLE_OVERLAP
    | SCIRCLE_OVERLAP_NEG | SCIRCLE_CONTAINED_BY_CIRCLE
    | SCIRCLE_CONTAINED_BY_CIRCLE_NEG | SCIRCLE_CONTAINS_CIRCLE
    | SCIRCLE_CONTAINS_CIRCLE_NEG | SPOINT_CONTAINED_BY_CIRCLE
    | SPOINT_CONTAINED_BY_CIRCLE_NEG | SPOINT_CONTAINED_BY_CIRCLE_COM
    | SPOINT_CONTAINED_BY_CIRCLE_COM_NEG | STRANS_CIRCLE
    | STRANS_CIRCLE_INVERSE | SLINE | SMERIDIAN | SLINE_BEG | SLINE_END
    | SLINE_EQUAL | SLINE_EQUAL_NEG | SLINE_TURN | SLINE_CROSSES
    | SLINE_CROSSES_NEG | SLINE_OVERLAP | SLINE_CONTAINS_POINT
    | SLINE_CONTAINS_POINT_COM | SLINE_CONTAINS_POINT_NEG
    | SLINE_CONTAINS_POINT_COM_NEG | STRANS_LINE | STRANS_LINE_INVERSE
    | SLINE_OVERLAP_CIRCLE | SLINE_OVERLAP_CIRCLE_COM
    | SLINE_OVERLAP_CIRCLE_NEG | SLINE_OVERLAP_CIRCLE_COM_NEG
    | SCIRCLE_CONTAINS_LINE | SCIRCLE_CONTAINS_LINE_COM
    | SCIRCLE_CONTAINS_LINE_NEG | SCIRCLE_CONTAINS_LINE_COM_NEG | SELLIPSE
    | SELLIPSE_INC | SELLIPSE_LRAD | SELLIPSE_SRAD | SELLIPSE_EQUAL
    | SELLIPSE_EQUAL_NEG | SELLIPSE_CONTAINS_ELLIPSE
    | SELLIPSE_CONTAINS_ELLIPSE_NEG | SELLIPSE_CONTAINS_ELLIPSE_COM
    | SELLIPSE_CONTAINS_ELLIPSE_COM_NEG | SELLIPSE_OVERLAP_ELLIPSE
    | SELLIPSE_OVERLAP_ELLIPSE_NEG | SELLIPSE_CONTAINS_POINT
    | SELLIPSE_CONTAINS_POINT_NEG | SELLIPSE_CONTAINS_POINT_COM
    | SELLIPSE_CONTAINS_POINT_COM_NEG | SELLIPSE_CONTAINS_CIRCLE
    | SELLIPSE_CONTAINS_CIRCLE_NEG | SELLIPSE_CONTAINS_CIRCLE_COM
    | SELLIPSE_CONTAINS_CIRCLE_COM_NEG | SCIRCLE_CONTAINS_ELLIPSE
    | SCIRCLE_CONTAINS_ELLIPSE_NEG | SCIRCLE_CONTAINS_ELLIPSE_COM
    | SCIRCLE_CONTAINS_ELLIPSE_COM_NEG | SELLIPSE_OVERLAP_CIRCLE
    | SELLIPSE_OVERLAP_CIRCLE_NEG | SELLIPSE_OVERLAP_CIRCLE_COM
    | SELLIPSE_OVERLAP_CIRCLE_COM_NEG | SELLIPSE_OVERLAP_LINE
    | SELLIPSE_OVERLAP_LINE_NEG | SELLIPSE_OVERLAP_LINE_COM
    | SELLIPSE_OVERLAP_LINE_COM_NEG | SELLIPSE_CONTAINS_LINE
    | SELLIPSE_CONTAINS_LINE_NEG | SELLIPSE_CONTAINS_LINE_COM
    | SELLIPSE_CONTAINS_LINE_COM_NEG | STRANS_ELLIPSE
    | STRANS_ELLIPSE_INVERSE | SPOLY | SPOLY_EQUAL | SPOLY_EQUAL_NEG
    | SPOLY_CONTAINS_POLYGON | SPOLY_CONTAINS_POLYGON_NEG
    | SPOLY_CONTAINS_POLYGON_COM | SPOLY_CONTAINS_POLYGON_COM_NEG
    | SPOLY_OVERLAP_POLYGON | SPOLY_OVERLAP_POLYGON_NEG
    | SPOLY_CONTAINS_POINT | SPOLY_CONTAINS_POINT_NEG
    | SPOLY_CONTAINS_POINT_COM | SPOLY_CONTAINS_POINT_COM_NEG
    | SPOLY_CONTAINS_CIRCLE | SPOLY_CONTAINS_CIRCLE_NEG
    | SPOLY_CONTAINS_CIRCLE_COM | SPOLY_CONTAINS_CIRCLE_COM_NEG
    | SCIRCLE_CONTAINS_POLYGON | SCIRCLE_CONTAINS_POLYGON_NEG
    | SCIRCLE_CONTAINS_POLYGON_COM | SCIRCLE_CONTAINS_POLYGON_COM_NEG
    | SPOLY_OVERLAP_CIRCLE | SPOLY_OVERLAP_CIRCLE_NEG
    | SPOLY_OVERLAP_CIRCLE_COM | SPOLY_OVERLAP_CIRCLE_COM_NEG
    | SPOLY_CONTAINS_LINE | SPOLY_CONTAINS_LINE_NEG | SPOLY_CONTAINS_LINE_COM
    | SPOLY_CONTAINS_LINE_COM_NEG | SPOLY_OVERLAP_LINE
    | SPOLY_OVERLAP_LINE_NEG | SPOLY_OVERLAP_LINE_COM
    | SPOLY_OVERLAP_LINE_COM_NEG | SPOLY_CONTAINS_ELLIPSE
    | SPOLY_CONTAINS_ELLIPSE_NEG | SPOLY_CONTAINS_ELLIPSE_COM
    | SPOLY_CONTAINS_ELLIPSE_COM_NEG | SELLIPSE_CONTAINS_POLYGON
    | SELLIPSE_CONTAINS_POLYGON_NEG | SELLIPSE_CONTAINS_POLYGON_COM
    | SELLIPSE_CONTAINS_POLYGON_COM_NEG | SPOLY_OVERLAP_ELLIPSE
    | SPOLY_OVERLAP_ELLIPSE_NEG | SPOLY_OVERLAP_ELLIPSE_COM
    | SPOLY_OVERLAP_ELLIPSE_COM_NEG | STRANS_POLY | STRANS_POLY_INVERSE
    | SPOLY_ADD_POINT_AGGR | SPOLY_AGGR | SPATH | SPATH_EQUAL
    | SPATH_EQUAL_NEG | SPATH_OVERLAP_PATH | SPATH_OVERLAP_PATH_NEG
    | SPATH_CONTAINS_POINT | SPATH_CONTAINS_POINT_NEG
    | SPATH_CONTAINS_POINT_COM | SPATH_CONTAINS_POINT_COM_NEG
    | SCIRCLE_CONTAINS_PATH | SCIRCLE_CONTAINS_PATH_NEG
    | SCIRCLE_CONTAINS_PATH_COM | SCIRCLE_CONTAINS_PATH_COM_NEG
    | SCIRCLE_OVERLAP_PATH | SCIRCLE_OVERLAP_PATH_NEG
    | SCIRCLE_OVERLAP_PATH_COM | SCIRCLE_OVERLAP_PATH_COM_NEG
    | SPATH_OVERLAP_LINE | SPATH_OVERLAP_LINE_NEG | SPATH_OVERLAP_LINE_COM
    | SPATH_OVERLAP_LINE_COM_NEG | SELLIPSE_CONTAINS_PATH
    | SELLIPSE_CONTAINS_PATH_NEG | SELLIPSE_CONTAINS_PATH_COM
    | SELLIPSE_CONTAINS_PATH_COM_NEG | SELLIPSE_OVERLAP_PATH
    | SELLIPSE_OVERLAP_PATH_NEG | SELLIPSE_OVERLAP_PATH_COM
    | SELLIPSE_OVERLAP_PATH_COM_NEG | SPOLY_CONTAINS_PATH
    | SPOLY_CONTAINS_PATH_NEG | SPOLY_CONTAINS_PATH_COM
    | SPOLY_CONTAINS_PATH_COM_NEG | SPOLY_OVERLAP_PATH
    | SPOLY_OVERLAP_PATH_NEG | SPOLY_OVERLAP_PATH_COM
    | SPOLY_OVERLAP_PATH_COM_NEG | STRANS_PATH | STRANS_PATH_INVERSE
    | SPATH_ADD_POINT_AGGR | SPATH_AGGR | SBOX | SBOX_SW | SBOX_SE | SBOX_NW
    | SBOX_NE | SBOX_EQUAL | SBOX_EQUAL_NEG | SBOX_CONTAINS_BOX
    | SBOX_CONTAINS_BOX_NEG | SBOX_CONTAINS_BOX_COM
    | SBOX_CONTAINS_BOX_COM_NEG | SBOX_OVERLAP_BOX | SBOX_OVERLAP_BOX_NEG
    | SBOX_CONTAINS_POINT | SBOX_CONTAINS_POINT_NEG | SBOX_CONTAINS_POINT_COM
    | SBOX_CONTAINS_POINT_COM_NEG | SBOX_CONTAINS_CIRCLE
    | SBOX_CONTAINS_CIRCLE_NEG | SBOX_CONTAINS_CIRCLE_COM
    | SBOX_CONTAINS_CIRCLE_COM_NEG | SCIRCLE_CONTAINS_BOX
    | SCIRCLE_CONTAINS_BOX_NEG | SCIRCLE_CONTAINS_BOX_COM
    | SCIRCLE_CONTAINS_BOX_COM_NEG | SBOX_OVERLAP_CIRCLE
    | SBOX_OVERLAP_CIRCLE_NEG | SBOX_OVERLAP_CIRCLE_COM
    | SBOX_OVERLAP_CIRCLE_COM_NEG | SBOX_CONTAINS_LINE
    | SBOX_CONTAINS_LINE_NEG | SBOX_CONTAINS_LINE_COM
    | SBOX_CONTAINS_LINE_COM_NEG | SBOX_OVERLAP_LINE | SBOX_OVERLAP_LINE_NEG
    | SBOX_OVERLAP_LINE_COM | SBOX_OVERLAP_LINE_COM_NEG
    | SBOX_CONTAINS_ELLIPSE | SBOX_CONTAINS_ELLIPSE_NEG
    | SBOX_CONTAINS_ELLIPSE_COM | SBOX_CONTAINS_ELLIPSE_COM_NEG
    | SELLIPSE_CONTAINS_BOX | SELLIPSE_CONTAINS_BOX_NEG
    | SELLIPSE_CONTAINS_BOX_COM | SELLIPSE_CONTAINS_BOX_COM_NEG
    | SBOX_OVERLAP_ELLIPSE | SBOX_OVERLAP_ELLIPSE_NEG
    | SBOX_OVERLAP_ELLIPSE_COM | SBOX_OVERLAP_ELLIPSE_COM_NEG
    | SBOX_CONTAINS_POLY | SBOX_CONTAINS_POLY_NEG | SBOX_CONTAINS_POLY_COM
    | SBOX_CONTAINS_POLY_COM_NEG | SPOLY_CONTAINS_BOX
    | SPOLY_CONTAINS_BOX_NEG | SPOLY_CONTAINS_BOX_COM
    | SPOLY_CONTAINS_BOX_COM_NEG | SBOX_OVERLAP_POLY | SBOX_OVERLAP_POLY_NEG
    | SBOX_OVERLAP_POLY_COM | SBOX_OVERLAP_POLY_COM_NEG | SBOX_CONTAINS_PATH
    | SBOX_CONTAINS_PATH_NEG | SBOX_CONTAINS_PATH_COM
    | SBOX_CONTAINS_PATH_COM_NEG | SBOX_OVERLAP_PATH | SBOX_OVERLAP_PATH_NEG
    | SBOX_OVERLAP_PATH_COM | SBOX_OVERLAP_PATH_COM_NEG ;

mysql_udf_functions:
      STRRPOS | IDLE | ANGDIST | HILBERTKEY | COORDFROMHILBERTKEY
    | SUM_OF_SQUARES | PARTITADD_SUM_OF_SQARES ;

functionList:
	  number_functions | char_functions | time_functions | other_functions
    | mysql_sphere_functions | mysql_udf_functions;


literal_value:
      string_literal | number_literal | hex_literal | boolean_literal
    | bit_literal | NULL_SYM ;



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

alias:                  ( AS_SYM )? ID ;
bit_expr:               factor1 ( VERTBAR factor1 )? ;

bool_primary:
      // Make sure this really work!!!
      predicate ( relational_op predicate )? | ( ( NOT_SYM )? EXISTS subquery);
      //predicate ( relational_op (predicate | (( ALL | ANY )? subquery)) )?
/* done
	  ( predicate relational_op predicate )
	| ( predicate relational_op ( ALL | ANY )? subquery )
	| ( ( NOT_SYM )? EXISTS subquery )
	| predicate ;
*/

case_when_statement:    CASE_SYM (case_when_statement1 | case_when_statement2) ( ELSE_SYM bit_expr )? END_SYM;
case_when_statement1:   ( WHEN_SYM expression THEN_SYM bit_expr )+ ;
case_when_statement2:   bit_expr ( WHEN_SYM bit_expr THEN_SYM bit_expr )+ ;

//case_when_statement:    case_when_statement1 | case_when_statement2 ;
//case_when_statement1:   CASE_SYM        ( WHEN_SYM expression THEN_SYM bit_expr )+ ( ELSE_SYM bit_expr )? END_SYM ;
//case_when_statement2:   CASE_SYM bit_expr ( WHEN_SYM bit_expr THEN_SYM bit_expr )+ ( ELSE_SYM bit_expr )? END_SYM ;

column_list:            LPAREN column_spec ( COMMA column_spec )* RPAREN ;
column_name:            ID ;
column_spec:            ( ( schema_name DOT )? table_name DOT )? column_name ;

//displayed_column :      ( table_spec DOT ASTERISK ) | ( column_spec ( alias )? ) | ( bit_expr ( alias )? ) ;
displayed_column :      ( table_spec DOT ASTERISK ) | ( bit_expr ( alias )? ) ;
//displayed_column :      ( table_spec DOT ASTERISK ) | ( column_spec ( alias )? ) ;

exp_factor1:	        exp_factor2 ( XOR exp_factor2 )* ;
exp_factor2:	        exp_factor3 ( AND_SYM exp_factor3 )* ;
exp_factor3:	        ( NOT_SYM )? exp_factor4 ;
exp_factor4:	        bool_primary ( IS_SYM ( NOT_SYM )? (boolean_literal | NULL_SYM) )? ;
// expression:	            ( LPAREN )? exp_factor1 ( OR_SYM exp_factor1 )* ( RPAREN )? ;
expression:	            exp_factor1 ( OR_SYM exp_factor1 )* ;
expression_list:        LPAREN expression ( COMMA expression )* RPAREN ;

factor1:                factor2 ( BITAND factor2 )? ;
factor2:                factor3 ( ( SHIFT_LEFT | SHIFT_RIGHT ) factor3 )? ;
factor3:                factor4 ( ( PLUS | MINUS ) factor4 )* ;
factor4:                factor5 ( ( ASTERISK | DIVIDE | MOD_SYM | POWER_OP ) factor5 )* ;
factor5:                ( PLUS | MINUS | NEGATION | BINARY )? simple_expr ( ( PLUS | MINUS ) interval_expr )? ;


function_call:
	  ( functionList ( LPAREN ( expression ( COMMA expression )* )? RPAREN ) ? )
	| ( CONVERT_SYM LPAREN expression COMMA cast_data_type RPAREN )
	| ( CONVERT_SYM LPAREN expression USING_SYM transcoding_name RPAREN )
	| ( CAST_SYM LPAREN expression AS_SYM cast_data_type RPAREN ) 
	| ( group_functions LPAREN ( ASTERISK | ALL | DISTINCT )? ( bit_expr )? RPAREN ) ;
	//| ( group_functions LPAREN ( ASTERISK | ALL | DISTINCT )? ( bit_expr )* RPAREN ) ;

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
orderby_item:	        groupby_item ( ASC | DESC )? ;

partition_clause:       PARTITION_SYM LPAREN partition_names RPAREN ;
partition_name:         ID ;
partition_names:	    partition_name ( COMMA partition_name )* ;

bit_fac1:               ( NOT_SYM )? ( (IN_SYM ( subquery | expression_list )) | (LIKE_SYM simple_expr ( ESCAPE_SYM simple_expr )?) | (REGEXP bit_expr) | (BETWEEN bit_expr AND_SYM predicate)) ;
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
select_list:            ( ( displayed_column ( COMMA displayed_column )* ) | ASTERISK ) ;
select_statement:       select_expression ( (UNION_SYM ( ALL )? ) select_expression )* ;

simple_expr:
	  literal_value
	| expression_list
	| column_spec 
	| function_call 
	| USER_VAR
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

table_reference:        table_factor1 ; //| table_atom ;
table_references:       table_reference ( COMMA table_reference )* ;
table_spec:             ( schema_name DOT )? table_name ;

where_clause:           WHERE expression ;
