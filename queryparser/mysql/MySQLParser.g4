
parser grammar MySQLParser;

options
   { tokenVocab = MySQLLexer; }


// basic type definition -----------------------------------------------------------------------
relational_op:
	EQ_SYM | LTH | GTH | NOT_EQ | LET | GET
;

charset_name:
	  ARMSCII8
	| ASCII_SYM
	| BIG5
	| BINARY
	| CP1250
	| CP1251
	| CP1256
	| CP1257
	| CP850
	| CP852
	| CP866
	| CP932
	| DEC8
	| EUCJPMS
	| EUCKR
	| GB2312
	| GBK
	| GEOSTD8
	| GREEK
	| HEBREW
	| HP8
	| KEYBCS2
	| KOI8R
	| KOI8U
	| LATIN1
	| LATIN2
	| LATIN5
	| LATIN7
	| MACCE
	| MACROMAN
	| SJIS
	| SWE7
	| TIS620
	| UCS2
	| UJIS
	| UTF8
;

cast_data_type:
	BINARY (INTEGER_NUM)?
	| CHAR (INTEGER_NUM)?
	| DATE_SYM
	| DATETIME
	| DECIMAL_SYM ( INTEGER_NUM (COMMA INTEGER_NUM)? )?
	| SIGNED_SYM (INTEGER_SYM)?
	| TIME_SYM
	| UNSIGNED_SYM (INTEGER_SYM)?
;

search_modifier:
	(IN_SYM NATURAL LANGUAGE MODE_SYM)
	| (IN_SYM NATURAL LANGUAGE MODE_SYM WITH QUERY_SYM EXPANSION_SYM)
	| (IN_SYM BOOLEAN_SYM MODE_SYM)
	| (WITH QUERY_SYM EXPANSION_SYM)
;

transcoding_name:
	  LATIN1
	| UTF8
;

interval_unit:
	  SECOND
	| MINUTE
	| HOUR
	| DAY_SYM
	| WEEK
	| MONTH
	| QUARTER
	| YEAR
	| SECOND_MICROSECOND
	| MINUTE_MICROSECOND
	| MINUTE_SECOND
	| HOUR_MICROSECOND
	| HOUR_SECOND
	| HOUR_MINUTE
	| DAY_MICROSECOND
	| DAY_SECOND
	| DAY_MINUTE
	| DAY_HOUR
	| YEAR_MONTH
;

collation_names:
	LATIN1_GENERAL_CS | LATIN1_BIN
;

// basic const data definition ---------------------------------------------------------------
string_literal:		TEXT_STRING ;
number_literal:		(PLUS | MINUS)? (INTEGER_NUM | REAL_NUMBER) ;
//date_time_literal: 	;
hex_literal:		HEX_DIGIT;
boolean_literal:	TRUE_SYM | FALSE_SYM ;
bit_literal:		BIT_NUM;

literal_value:
        ( string_literal | number_literal | hex_literal | boolean_literal | bit_literal | NULL_SYM ) ;

functionList:
	  number_functions
	| char_functions
	| time_functions
	| other_functions
	| custom_functions
;

number_functions:
	  ABS
	| ACOS
	| ASIN
	| ATAN2
	| ATAN
	| CEIL
	| CEILING
	| CONV
	| COS
	| COT
	| CRC32
	| DEGREES
	| EXP
	| FLOOR
	| LN
	| LOG10
	| LOG2
	| LOG
	| MOD
	| PI
	| POW
	| POWER
	| RADIANS
	| RAND
	| ROUND
	| SIGN
	| SIN
	| SQRT
	| TAN
	| TRUNCATE
;

char_functions:
	  ASCII_SYM
	| BIN
	| BIT_LENGTH
	| CHAR_LENGTH
	| CHAR
	| CONCAT_WS
	| CONCAT
	| ELT
	| EXPORT_SET
	| FIELD
	| FIND_IN_SET
	| FORMAT
	| FROM_BASE64
	| HEX
	| INSERT
	| INSTR
	| LEFT
	| LENGTH
	| LOAD_FILE
	| LOCATE
	| LOWER
	| LPAD
	| LTRIM
	| MAKE_SET
	| MID
	| OCT
	| ORD
	| QUOTE
	| REPEAT
	| REPLACE
	| REVERSE
	| RIGHT
	| RPAD
	| RTRIM
	| SOUNDEX
	| SPACE
	| STRCMP
	| SUBSTRING_INDEX
	| SUBSTRING
	| TO_BASE64
	| TRIM
	| UNHEX
	| UPPER
	| WEIGHT_STRING
;

time_functions:
	  ADDDATE
	| ADDTIME
	| CONVERT_TZ
	| CURDATE
	| CURTIME
	| DATE_ADD
	| DATE_FORMAT
	| DATE_SUB
	| DATE_SYM
	| DATEDIFF
	| DAYNAME
	| DAYOFMONTH
	| DAYOFWEEK
	| DAYOFYEAR
	| EXTRACT
	| FROM_DAYS
	| FROM_UNIXTIME
	| GET_FORMAT
	| HOUR
	| LAST_DAY
	| MAKEDATE
	| MAKETIME
	| MICROSECOND
	| MINUTE
	| MONTH
	| MONTHNAME
	| NOW
	| PERIOD_ADD
	| PERIOD_DIFF
	| QUARTER
	| SEC_TO_TIME
	| SECOND
	| STR_TO_DATE
	| SUBTIME
	| SYSDATE
	| TIME_FORMAT
	| TIME_TO_SEC
	| TIME_SYM
	| TIMEDIFF
	| TIMESTAMP
	| TIMESTAMPADD
	| TIMESTAMPDIFF
	| TO_DAYS
	| TO_SECONDS
	| UNIX_TIMESTAMP
	| UTC_DATE
	| UTC_TIME
	| UTC_TIMESTAMP
	| WEEK
	| WEEKDAY
	| WEEKOFYEAR
	| YEAR
	| YEARWEEK
;

other_functions:
	MAKE_SET | LOAD_FILE
	| IF | IFNULL
	| AES_ENCRYPT | AES_DECRYPT
	| DECODE | ENCODE
	| DES_DECRYPT | DES_ENCRYPT
	| ENCRYPT | MD5
	| OLD_PASSWORD | PASSWORD
	| BENCHMARK | CHARSET | COERCIBILITY | COLLATION | CONNECTION_ID
	| CURRENT_USER | DATABASE | SCHEMA | USER | SESSION_USER | SYSTEM_USER
	| VERSION_SYM
	| FOUND_ROWS | LAST_INSERT_ID | DEFAULT
	| GET_LOCK | RELEASE_LOCK | IS_FREE_LOCK | IS_USED_LOCK | MASTER_POS_WAIT
	| INET_ATON | INET_NTOA
	| NAME_CONST
	| SLEEP
	| UUID
	| VALUES
;

group_functions:
	  AVG | COUNT | MAX_SYM | MIN_SYM | SUM
	| BIT_AND | BIT_OR | BIT_XOR | BIT_COUNT
	| GROUP_CONCAT
	| STD | STDDEV | STDDEV_POP | STDDEV_SAMP
	| VAR_POP | VAR_SAMP | VARIANCE
;

/* Add any additional function definitions here and don't forget to add a token.*/
custom_functions:
      SPRNG_DBL
;

/* ------------------------------------------------------------------------------------------------------------------ */

/* java version */
/*
schema_name			: tmpName=ID {strlen((const char *)$tmpName.text->chars) <= 64}? {printf("schema name = \%s \n",(char*)($tmpName.text->chars));};
table_name			: tmpName=ID {strlen((const char *)$tmpName.text->chars) <= 64}? {printf("table name = \%s \n",(char*)($tmpName.text->chars));};
column_name			: tmpName=ID {strlen((const char *)$tmpName.text->chars) <= 64}? {printf("column name = \%s \n",(char*)($tmpName.text->chars));};
alias				: ( AS_SYM )? tmpName=ID {strlen((const char *)$tmpName.text->chars) <= 256}? {printf("alias = \%s \n",(char*)($tmpName.text->chars));};
index_name			: tmpName=ID {strlen((const char *)$tmpName.text->chars) <= 64}? {printf("index name = \%s \n",(char*)($tmpName.text->chars));};
partition_name		: tmpName=ID {strlen((const char *)$tmpName.text->chars) <= 64}? {printf("partition name = \%s \n",(char*)($tmpName.text->chars));};
/*
/* python3 version */
/*
schema_name         : tmpName=ID; //{len($tmpName.text) <= 64}? {print("schema name = %s" % $tmpName)};
table_name          : tmpName=ID; // {len($tmpName.text) <= 64}? {print("table name = %s" % $tmpName)};
column_name         : tmpName=ID; //{len($tmpName.text) <= 64}? {print("column name = %s" % $tmpName)};
alias               : ( AS_SYM )? tmpName=ID; //{len($tmpName.text) <= 256}? {print("alias = %s" % $tmpName)};
index_name          : tmpName=ID; //{len($tmpName.text) <= 64}? {print("index name = %s" % $tmpName)};
partition_name      : tmpName=ID; //{len($tmpName.text) <= 64}? {print("partition name = %s" % $tmpName)};
*/

schema_name         : ID; //{len($tmpName.text) <= 64}? {print("schema name = %s" % $tmpName)};
table_name          : ID; // {len($tmpName.text) <= 64}? {print("table name = %s" % $tmpName)};
column_name         : ID; //{len($tmpName.text) <= 64}? {print("column name = %s" % $tmpName)};
alias               : ( AS_SYM )? ID; //{len($tmpName.text) <= 256}? {print("alias = %s" % $tmpName)};
index_name          : ID; //{len($tmpName.text) <= 64}? {print("index name = %s" % $tmpName)};
partition_name      : ID; //{len($tmpName.text) <= 64}? {print("partition name = %s" % $tmpName)};


/* ------------------------------------------------------------------------------------------------------------------ */



expression:	    (LPAREN)? exp_factor1 ( OR_SYM exp_factor1 )* (RPAREN)?;
exp_factor1:	exp_factor2 ( XOR exp_factor2 )* ;
exp_factor2:	exp_factor3 ( AND_SYM exp_factor3 )* ;
exp_factor3:	(NOT_SYM)? exp_factor4 ;
exp_factor4:	bool_primary ( IS_SYM (NOT_SYM)? (boolean_literal|NULL_SYM) )? ;
bool_primary:
	  ( predicate relational_op predicate )
	| ( predicate relational_op ( ALL | ANY )? subquery )
	| ( NOT_SYM? EXISTS subquery )
	| predicate
;
predicate:
	  ( bit_expr (NOT_SYM)? IN_SYM (subquery | expression_list) )
	| ( bit_expr (NOT_SYM)? BETWEEN bit_expr AND_SYM predicate )
	| ( bit_expr SOUNDS_SYM LIKE_SYM bit_expr )
	| ( bit_expr (NOT_SYM)? LIKE_SYM simple_expr (ESCAPE_SYM simple_expr)? )
	| ( bit_expr (NOT_SYM)? REGEXP bit_expr )
	| ( bit_expr )
;

bit_expr:
	factor1 ( VERTBAR factor1 )? ;
factor1:
	factor2 ( BITAND factor2 )? ;
factor2:
	factor3 ( (SHIFT_LEFT|SHIFT_RIGHT) factor3 )? ;
factor3:
	factor4 ( (PLUS|MINUS) factor4 )* ;
factor4:
	factor5 ( (ASTERISK|DIVIDE|MOD_SYM|POWER_OP) factor5 )* ;
factor5:
	factor6 ( (PLUS|MINUS) interval_expr )? ;
factor6:
	(PLUS | MINUS | NEGATION | BINARY) simple_expr
	| simple_expr ;
factor7:
	simple_expr (COLLATE_SYM collation_names)?;
simple_expr:
	literal_value
	| column_spec
	| function_call
	//| param_marker
	| USER_VAR
	| expression_list
	| (ROW_SYM expression_list)
	| subquery
	| EXISTS subquery
	//| {identifier expression}
	| match_against_statement
	| case_when_statement
	| interval_expr
;

function_call:
	  (  functionList ( LPAREN (expression (COMMA expression)*)? RPAREN ) ?  )
	| (  CAST_SYM LPAREN expression AS_SYM cast_data_type RPAREN  )
	| (  CONVERT_SYM LPAREN expression COMMA cast_data_type RPAREN  )
	| (  CONVERT_SYM LPAREN expression USING_SYM transcoding_name RPAREN  )
	| (  group_functions LPAREN ( ASTERISK | ALL | DISTINCT )? (bit_expr)* RPAREN  )
;

case_when_statement:
        case_when_statement1 | case_when_statement2
;
case_when_statement1:
        CASE_SYM
        ( WHEN_SYM expression THEN_SYM bit_expr )+
        ( ELSE_SYM bit_expr )?
        END_SYM
;
case_when_statement2:
        CASE_SYM bit_expr
        ( WHEN_SYM bit_expr THEN_SYM bit_expr )+
        ( ELSE_SYM bit_expr )?
        END_SYM
;

match_against_statement:
	MATCH (column_spec (COMMA column_spec)* ) AGAINST (expression (search_modifier)? )
;

column_spec:
	( ( schema_name DOT )? table_name DOT )? column_name ;

expression_list:
	LPAREN expression ( COMMA expression )* RPAREN ;

interval_expr:
	INTERVAL_SYM expression interval_unit
;




// JOIN ----------  http://dev.mysql.com/doc/refman/5.6/en/join.html  ---------------
table_references:
        table_reference ( COMMA table_reference )*
;
table_reference:
	table_factor1 | table_atom
;
table_factor1:
	table_factor2 (  (INNER_SYM | CROSS)? JOIN_SYM table_atom (join_condition)?  )*
;
table_factor2:
	table_factor3 (  STRAIGHT_JOIN table_atom (ON expression)?  )?
;
table_factor3:
	table_factor4 (  (LEFT|RIGHT) (OUTER)? JOIN_SYM table_factor4 join_condition  )*
;
table_factor4:
	table_atom (  NATURAL ( (LEFT|RIGHT) (OUTER)? )? JOIN_SYM table_atom )?
;
table_atom:
	  ( table_spec (partition_clause)? (alias)? (index_hint_list)? )
	| ( subquery alias )
	| ( LPAREN table_references RPAREN )
	| ( OJ_SYM table_reference LEFT OUTER JOIN_SYM table_reference ON expression )
;
join_condition:
	  (ON expression) | (USING_SYM column_list)
;
index_hint_list:
	index_hint (COMMA index_hint)*
;
index_options:
	(INDEX_SYM | KEY_SYM) (  FOR_SYM ((JOIN_SYM) | (ORDER_SYM BY_SYM) | (GROUP_SYM BY_SYM))  )?
;
index_hint:
	  USE_SYM    index_options LPAREN (index_list)? RPAREN
	| IGNORE_SYM index_options LPAREN index_list RPAREN
	| FORCE_SYM  index_options LPAREN index_list RPAREN
;
index_list:
	index_name (COMMA index_name)*
;
partition_clause:
	PARTITION_SYM LPAREN partition_names RPAREN
;
partition_names:	partition_name (COMMA partition_name)* ;




// SELECT ------  http://dev.mysql.com/doc/refman/5.6/en/select.html  -------------------------------
select_statement:
        select_expression ( (UNION_SYM (ALL)?) select_expression )*
;

select_expression:
	SELECT

	( ALL | DISTINCT | DISTINCTROW )?
	(HIGH_PRIORITY)?
	(STRAIGHT_JOIN)?
	(SQL_SMALL_RESULT)? (SQL_BIG_RESULT)? (SQL_BUFFER_RESULT)?
	(SQL_CACHE_SYM | SQL_NO_CACHE_SYM)? (SQL_CALC_FOUND_ROWS)?

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
	( ( FOR_SYM UPDATE) | (LOCK IN_SYM SHARE_SYM MODE_SYM) )?

	SEMI?
;

where_clause:
	WHERE expression
;

groupby_clause:
	GROUP_SYM BY_SYM groupby_item (COMMA groupby_item)* (WITH ROLLUP_SYM)?
;
groupby_item:	column_spec | INTEGER_NUM | bit_expr ;

having_clause:
	HAVING expression
;

orderby_clause:
	ORDER_SYM BY_SYM orderby_item (COMMA orderby_item)*
;
orderby_item:	groupby_item (ASC | DESC)? ;

limit_clause:
	LIMIT ((offset COMMA)? row_count) | (row_count OFFSET_SYM offset)
;
offset:		INTEGER_NUM ;
row_count:	INTEGER_NUM ;

select_list:
	( ( displayed_column ( COMMA displayed_column )*)
	| ASTERISK)
;

column_list:
	LPAREN column_spec (COMMA column_spec)* RPAREN
;

subquery:
	LPAREN select_statement RPAREN
;

table_spec:
	( schema_name DOT )? table_name
;

displayed_column :
	( table_spec DOT ASTERISK )
	|
	( column_spec (alias)? )
	|
	( bit_expr (alias)? )
;




// USE
use_statement:
    USE schema_name SEMI
;




// QUERY
query:
    (use_statement ?) select_statement
;
