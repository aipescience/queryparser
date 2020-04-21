
lexer grammar PostgreSQLLexer;
@ header { }

fragment A_ :	'a' | 'A';
fragment B_ :	'b' | 'B';
fragment C_ :	'c' | 'C';
fragment D_ :	'd' | 'D';
fragment E_ :	'e' | 'E';
fragment F_ :	'f' | 'F';
fragment G_ :	'g' | 'G';
fragment H_ :	'h' | 'H';
fragment I_ :	'i' | 'I';
fragment J_ :	'j' | 'J';
fragment K_ :	'k' | 'K';
fragment L_ :	'l' | 'L';
fragment M_ :	'm' | 'M';
fragment N_ :	'n' | 'N';
fragment O_ :	'o' | 'O';
fragment P_ :	'p' | 'P';
fragment Q_ :	'q' | 'Q';
fragment R_ :	'r' | 'R';
fragment S_ :	's' | 'S';
fragment T_ :	't' | 'T';
fragment U_ :	'u' | 'U';
fragment V_ :	'v' | 'V';
fragment W_ :	'w' | 'W';
fragment X_ :	'x' | 'X';
fragment Y_ :	'y' | 'Y';
fragment Z_ :	'z' | 'Z';

ABS				    : A_ B_ S_ ;
ACOS				: A_ C_ O_ S_ ;
ALL				    : A_ L_ L_  ;
ANY				    : A_ N_ Y_ ;
ASC				    : A_ S_ C_  ;
ASIN				: A_ S_ I_ N_  ;
AS_SYM				: A_ S_  ;
ATAN				: A_ T_ A_ N_  ;
ATAN2				: A_ T_ A_ N_ '2'  ;
AVG				    : A_ V_ G_;
BETWEEN				: B_ E_ T_ W_ E_ E_ N_  ;
BIGINT              : B_ I_ G_ I_ N_ T_ ;
BINARY				: B_ I_ N_ A_ R_ Y_  ;
BIT_AND				: B_ I_ T_ '_' A_ N_ D_  ;
BIT_COUNT           : B_ I_ T_ '_' C_ O_ U_ N_ T_  ;
BIT_LENGTH			: B_ I_ T_ '_' L_ E_ N_ G_ T_ H_;
BIT_OR				: B_ I_ T_ '_' O_ R_  ;
BIT_XOR				: B_ I_ T_ '_' X_ O_ R_  ;
BOOLEAN_SYM			: B_ O_ O_ L_ E_ A_ N_  ;
BY_SYM				: B_ Y_ ;
CASE_SYM			: C_ A_ S_ E_  ;
CAST_SYM			: C_ A_ S_ T_  ;
CBRT                : C_ B_ R_ T_ ;
CEIL				: C_ E_ I_ L_  ;
CEILING				: C_ E_ I_ L_ I_ N_ G_  ;
CHAR				: C_ H_ A_ R_  ;
CHR                 : C_ H_ R_ ;
//CHARSET				: C_ H_ A_ R_ S_ E_ T_  ;
CHAR_LENGTH			: (C_ H_ A_ R_ '_' L_ E_ N_ G_ T_ H_) | (C_ H_ A_ R_ A_ C_ T_ E_ R_ '_' L_ E_ N_ G_ T_ H_) ;
//COERCIBILITY		: C_ O_ E_ R_ C_ I_ B_ I_ L_ I_ T_ Y_  ;
//COLLATION			: C_ O_ L_ L_ A_ T_ I_ O_ N_  ;
CONCAT				: C_ O_ N_ C_ A_ T_  ;
CONCAT_WS			: C_ O_ N_ C_ A_ T_ '_' W_ S_  ;
CONVERT_SYM			: C_ O_ N_ V_ E_ R_ T_  ;
CONVERT_TZ			: C_ O_ N_ V_ E_ R_ T_ '_' T_ Z_  ;
COS				    : C_ O_ S_  ;
COT				    : C_ O_ T_  ;
COUNT				: C_ O_ U_ N_ T_  ;
CROSS				: C_ R_ O_ S_ S_  ;
CURDATE				: C_ U_ R_ R_ E_ N_ T_ '_' D_ A_ T_ E_ ;
CURTIME				: (C_ U_ R_ T_ I_ M_ E_) | (C_ U_ R_ R_ E_ N_ T_ '_' T_ I_ M_ E_) ;
DATETIME			: D_ A_ T_ E_ T_ I_ M_ E_  ;
DATE_ADD			: D_ A_ T_ E_ '_' A_ D_ D_  ;
DATE_FORMAT			: D_ A_ T_ E_ '_' F_ O_ R_ M_ A_ T_  ;
DATE_PART           : D_ A_ T_ E_ '_' P_ A_ R_ T_ ;
DATE_SYM			: D_ A_ T_ E_  ;
DAYNAME				: D_ A_ Y_ N_ A_ M_ E_  ;
DAYOFMONTH			: (D_ A_ Y_ O_ F_ M_ O_ N_ T_ H_) | (D_ A_ Y_) ;
DAYOFWEEK			: D_ A_ Y_ O_ F_ W_ E_ E_ K_  ;
DAYOFYEAR			: D_ A_ Y_ O_ F_ Y_ E_ A_ R_  ;
DAY_HOUR			: D_ A_ Y_  '_' H_ O_ U_ R_  ;
DAY_MICROSECOND		: D_ A_ Y_  '_' M_ I_ C_ R_ O_ S_ E_ C_ O_ N_ D_  ;
DAY_MINUTE			: D_ A_ Y_  '_' M_ I_ N_ U_ T_ E_  ;
DAY_SECOND			: D_ A_ Y_  '_' S_ E_ C_ O_ N_ D_  ;
DAY_SYM				: D_ A_ Y_  ;
DECIMAL_SYM			: D_ E_ C_ I_ M_ A_ L_  ;
DEGREES				: D_ E_ G_ R_ E_ E_ S_  ;
DESC				: D_ E_ S_ C_  ;
DIV                 : D_ I_ V_ ;
DISTINCT			: D_ I_ S_ T_ I_ N_ C_ T_ ;
DOUBLE_PRECISION_SYM: D_ O_ U_ B_ L_ E_ ' ' P_ R_ E_ C_ I_ S_ I_ O_ N_ ;
ELSE_SYM			: E_ L_ S_ E_  ;
ENCODE				: E_ N_ C_ O_ D_ E_  ;
END_SYM				: E_ N_ D_ ;
ESCAPE_SYM			: E_ S_ C_ A_ P_ E_  ;
EXISTS				: E_ X_ I_ S_ T_ S_ ;
EXP				    : E_ X_ P_  ;
EXPANSION_SYM		: E_ X_ P_ A_ N_ S_ I_ O_ N_  ;
EXTRACT				: E_ X_ T_ R_ A_ C_ T_  ;
FALSE_SYM			: F_ A_ L_ S_ E_ ;
FIND_IN_SET			: F_ I_ N_ D_ '_' I_ N_ '_' S_ E_ T_  ;
FIRST_SYM           : F_ I_ R_ S_ T_ ;
FLOAT               : F_ L_ O_ A_ T_ ;
FLOOR				: F_ L_ O_ O_ R_  ;
FORCE_SYM			: F_ O_ R_ C_ E_  ;
FOR_SYM				: F_ O_ R_  ;
FROM				: F_ R_ O_ M_  ;
FROM_DAYS			: F_ R_ O_ M_ '_' D_ A_ Y_ S_  ;
FROM_UNIXTIME		: F_ R_ O_ M_ '_' U_ N_ I_ X_ T_ I_ M_ E_  ;
GET_FORMAT			: G_ E_ T_ '_' F_ O_ R_ M_ A_ T_  ;
GREATEST            : G_ R_ E_ A_ T_ E_ S_ T_ ;
GROUP_CONCAT		: G_ R_ O_ U_ P_ '_' C_ O_ N_ C_ A_ T_  ;
GROUP_SYM			: G_ R_ O_ U_ P_  ;
HAVING				: H_ A_ V_ I_ N_ G_  ;
HOUR				: H_ O_ U_ R_  ;
HOUR_MICROSECOND	: H_ O_ U_ R_  '_' M_ I_ C_ R_ O_ S_ E_ C_ O_ N_ D_  ;
HOUR_MINUTE			: H_ O_ U_ R_  '_' M_ I_ N_ U_ T_ E_  ;
HOUR_SECOND			: H_ O_ U_ R_  '_' S_ E_ C_ O_ N_ D_  ;
IGNORE_SYM			: I_ G_ N_ O_ R_ E_  ;
INDEX_SYM			: I_ N_ D_ E_ X_  ;
INNER_SYM			: I_ N_ N_ E_ R_  ;
INSTR				: I_ N_ S_ T_ R_  ;
INTEGER_SYM			: I_ N_ T_ E_ G_ E_ R_  ;
INTERVAL_SYM		: I_ N_ T_ E_ R_ V_ A_ L_  ;
IN_SYM				: I_ N_  ;
ISNULL              : I_ S_ N_ U_ L_ L_ ;
IS_SYM				: I_ S_  ;
JOIN_SYM			: J_ O_ I_ N_  ;
KEY_SYM				: K_ E_ Y_  ;
LANGUAGE			: L_ A_ N_ G_ U_ A_ G_ E_ ;
LAST_SYM            : L_ A_ S_ T_ ;
LAST_DAY			: L_ A_ S_ T_ '_' D_ A_ Y_  ;
LEFT				: L_ E_ F_ T_  ;
LENGTH				: (L_ E_ N_ G_ T_ H_) | (O_ C_ T_ E_ T_ '_' L_ E_ N_ G_ T_ H_) ;
LIKE_SYM			: L_ I_ K_ E_  ;
LIMIT				: L_ I_ M_ I_ T_  ;
LN				    : L_ N_  ;
LOCK				: L_ O_ C_ K_ ;
LOG				    : L_ O_ G_  ;
LOWER				: (L_ O_ W_ E_ R_) | (L_ C_ A_ S_ E_) ;
LPAD				: L_ P_ A_ D_  ;
LTRIM				: L_ T_ R_ I_ M_  ;
MAKEDATE			: M_ A_ K_ E_ D_ A_ T_ E_  ;
MAKETIME			: M_ A_ K_ E_ T_ I_ M_ E_  ;
MAX_SYM				: M_ A_ X_  ;
MD5				    : M_ D_ '5'  ;
MICROSECOND			: M_ I_ C_ R_ O_ S_ E_ C_ O_ N_ D_  ;
MINUTE				: M_ I_ N_ U_ T_ E_  ;
MINUTE_MICROSECOND	: M_ I_ N_ U_ T_ E_  '_' M_ I_ C_ R_ O_ S_ E_ C_ O_ N_ D_  ;
MINUTE_SECOND		: M_ I_ N_ U_ T_ E_  '_' S_ E_ C_ O_ N_ D_  ;
MIN_SYM				: M_ I_ N_  ;
MOD				    : M_ O_ D_  ;
MODE_SYM			: M_ O_ D_ E_  ;
MONTH				: M_ O_ N_ T_ H_  ;
MONTHNAME			: M_ O_ N_ T_ H_ N_ A_ M_ E_  ;
NATURAL				: N_ A_ T_ U_ R_ A_ L_  ;
NOT_SYM				: (N_ O_ T_) | ('!') ;
NOTNULL             : N_ O_ T_ N_ U_ L_ L_ ;
NOW				    : (N_ O_ W_) | (L_ O_ C_ A_ L_ T_ I_ M_ E_) | (L_ O_ C_ A_ L_ T_ I_ M_ E_ S_ T_ A_ M_ P_) | (C_ U_ R_ R_ E_ N_ T_ '_' T_ I_ M_ E_ S_ T_ A_ M_ P_);
NULL_SYM			: N_ U_ L_ L_  ;
NULLS_SYM           : N_ U_ L_ L_ S_ ;
OFFSET_SYM			: O_ F_ F_ S_ E_ T_  ;
OJ_SYM				: O_ J_  ;
ON				    : O_ N_  ;
ORDER_SYM			: O_ R_ D_ E_ R_  ;
OUTER				: O_ U_ T_ E_ R_  ;
PARTITION_SYM		: P_ A_ R_ T_ I_ T_ I_ O_ N_  ;
PERIOD_ADD			: P_ E_ R_ I_ O_ D_ '_' A_ D_ D_  ;
PERIOD_DIFF			: P_ E_ R_ I_ O_ D_ '_' D_ I_ F_ F_  ;
PI				    : P_ I_  ;
POSITION_SYM        : P_ O_ S_ I_ T_ I_ O_ N_ ;
POW				    : P_ O_ W_  ;
POWER				: P_ O_ W_ E_ R_  ;
QUARTER				: Q_ U_ A_ R_ T_ E_ R_  ;
QUERY_SYM			: Q_ U_ E_ R_ Y_  ;
RADIANS				: R_ A_ D_ I_ A_ N_ S_  ;
RANDOM				: R_ A_ N_ D_ O_ M_ ;
REAL                : R_ E_ A_ L_ ;
REGEXP				: (R_ E_ G_ E_ X_ P_) | (R_ L_ I_ K_ E_);
REPEAT				: R_ E_ P_ E_ A_ T_  ;
REPLACE				: R_ E_ P_ L_ A_ C_ E_  ;
REVERSE				: R_ E_ V_ E_ R_ S_ E_  ;
RIGHT				: R_ I_ G_ H_ T_  ;
ROLLUP_SYM			: R_ O_ L_ L_ U_ P_  ;
ROUND				: R_ O_ U_ N_ D_  ;
ROW_SYM				: R_ O_ W_  ;
RPAD				: R_ P_ A_ D_  ;
RTRIM				: R_ T_ R_ I_ M_  ;
SECOND				: S_ E_ C_ O_ N_ D_  ;
SECOND_MICROSECOND	: S_ E_ C_ O_ N_ D_  '_' M_ I_ C_ R_ O_ S_ E_ C_ O_ N_ D_  ;
SEC_TO_TIME			: S_ E_ C_ '_' T_ O_ '_' T_ I_ M_ E_  ;
SELECT				: S_ E_ L_ E_ C_ T_ ;
SHARE_SYM			: S_ H_ A_ R_ E_  ;
SIGN				: S_ I_ G_ N_  ;
SIGNED_SYM			: S_ I_ G_ N_ E_ D_  ;
SIN				    : S_ I_ N_  ;
SOUNDS_SYM			: S_ O_ U_ N_ D_ S_  ;
SPACE				: S_ P_ A_ C_ E_  ;
SQRT				: S_ Q_ R_ T_  ;
STDDEV				: S_ T_ D_ D_ E_ V_  ;
STDDEV_POP			: S_ T_ D_ D_ E_ V_ '_' P_ O_ P_  ;
STDDEV_SAMP			: S_ T_ D_ D_ E_ V_ '_' S_ A_ M_ P_  ;
STRAIGHT_JOIN		: S_ T_ R_ A_ I_ G_ H_ T_  '_' J_ O_ I_ N_  ;
STRCMP				: S_ T_ R_ C_ M_ P_;
STR_TO_DATE			: S_ T_ R_ '_' T_ O_ '_' D_ A_ T_ E_  ;
SUBSTRING			: (S_ U_ B_ S_ T_ R_ I_ N_ G_) | (S_ U_ B_ S_ T_ R_) ;
SUBTIME				: S_ U_ B_ T_ I_ M_ E_  ;
SUM				    : S_ U_ M_  ;
SYMMETRIC           : S_ Y_ M_ M_ E_ T_ R_ I_ C_ ;
SYSDATE				: S_ Y_ S_ D_ A_ T_ E_  ;
TAN				    : T_ A_ N_  ;
THEN_SYM			: T_ H_ E_ N_  ;
TIMEDIFF			: T_ I_ M_ E_ D_ I_ F_ F_  ;
TIMESTAMP			: T_ I_ M_ E_ S_ T_ A_ M_ P_  ;
TIMESTAMPADD		: T_ I_ M_ E_ S_ T_ A_ M_ P_ A_ D_ D_  ;
TIMESTAMPDIFF		: T_ I_ M_ E_ S_ T_ A_ M_ P_ D_ I_ F_ F_  ;
TIME_FORMAT			: T_ I_ M_ E_ '_' F_ O_ R_ M_ A_ T_  ;
TIME_SYM			: T_ I_ M_ E_  ;
TIME_TO_SEC			: T_ I_ M_ E_ '_' T_ O_ '_' S_ E_ C_  ;
TO_BASE64			: T_ O_ '_' B_ A_ S_ E_ '64';
TO_DAYS				: T_ O_ '_' D_ A_ Y_ S_  ;
TO_SECONDS			: T_ O_ '_' S_ E_ C_ O_ N_ D_ S_;
TRIM				: T_ R_ I_ M_  ;
TRUE_SYM			: T_ R_ U_ E_ ;
TRUNCATE			: T_ R_ U_ N_ C_ A_ T_ E_  ;
UNION_SYM			: U_ N_ I_ O_ N_  ;
UNIX_TIMESTAMP		: U_ N_ I_ X_ '_' T_ I_ M_ E_ S_ T_ A_ M_ P_  ;
UNSIGNED_SYM		: U_ N_ S_ I_ G_ N_ E_ D_  ;
UPDATE				: U_ P_ D_ A_ T_ E_ ;
UPPER				: (U_ P_ P_ E_ R_) | (U_ C_ A_ S_ E_)  ;
USE_SYM				: U_ S_ E_  ;
USING_SYM			: U_ S_ I_ N_ G_ 	;
UTC_DATE			: U_ T_ C_ '_' D_ A_ T_ E_  ;
UTC_TIME			: U_ T_ C_ '_' T_ I_ M_ E_  ;
UTC_TIMESTAMP		: U_ T_ C_ '_' T_ I_ M_ E_ S_ T_ A_ M_ P_  ;
VALUES              : V_ A_ L_ U_ E_ S_ ;
VARIANCE			: V_ A_ R_ I_ A_ N_ C_ E_  ;
VAR_POP				: V_ A_ R_ '_' P_ O_ P_  ;
VAR_SAMP			: V_ A_ R_ '_' S_ A_ M_ P_  ;
WEEK				: W_ E_ E_ K_  ;
WEEKDAY				: W_ E_ E_ K_ D_ A_ Y_  ;
WEEKOFYEAR			: W_ E_ E_ K_ O_ F_ Y_ E_ A_ R_  ;
WEIGHT_STRING		: W_ E_ I_ G_ H_ T_ '_' S_ T_ R_ I_ N_ G_;
WHEN_SYM			: W_ H_ E_ N_ 	;
WHERE				: W_ H_ E_ R_ E_  ;
WITH				: W_ I_ T_ H_  ;
YEAR				: Y_ E_ A_ R_  ;
YEARWEEK			: Y_ E_ A_ R_ W_ E_ E_ K_  ;
YEAR_MONTH			: Y_ E_ A_ R_  '_' M_ O_ N_ T_ H_  ;

// character sets
//ARMSCII8			: A_ R_ M_ S_ C_ I_ I_ '8'  ;
ASCII_SYM			: A_ S_ C_ I_ I_  ;
//CP1250				: C_ P_ '1250'  ;
//CP1251				: C_ P_ '1251'  ;
//CP1256				: C_ P_ '1256'  ;
//CP1257				: C_ P_ '1257'  ;
//CP850				: C_ P_ '850'  ;
//CP852				: C_ P_ '852'  ;
//CP866				: C_ P_ '866'  ;
//DEC8				: D_ E_ C_ '8'  ;
//EUCJPMS				: E_ U_ C_ J_ P_ M_ S_ ;
//EUCKR				: E_ U_ C_ K_ R_  ;
//GB2312				: G_ B_ '2312'  ;
//GBK				    : G_ B_ K_  ;
//GEOSTD8				: G_ E_ O_ S_ T_ D_ '8'  ;
//GREEK				: G_ R_ E_ E_ K_  ;
//HEBREW				: H_ E_ B_ R_ E_ W_  ;
//HP8				    : H_ P_ '8'  ;
//KEYBCS2				: K_ E_ Y_ B_ C_ S_ '2'  ;
//KOI8R				: K_ O_ I_ '8' R_  ;
//KOI8U				: K_ O_ I_ '8' U_  ;
LATIN1				: L_ A_ T_ I_ N_ '1'  ;
//LATIN1_BIN			: L_ A_ T_ I_ N_ '1_' B_ I_ N_  ;
//LATIN1_GENERAL_CS	: L_ A_ T_ I_ N_ '1_' G_ E_ N_ E_ R_ A_ L_ '_' C_ S_  ;
//LATIN2				: L_ A_ T_ I_ N_ '2'  ;
//LATIN5				: L_ A_ T_ I_ N_ '5'  ;
//LATIN7				: L_ A_ T_ I_ N_ '7'  ;
//MACCE				: M_ A_ C_ C_ E_  ;
//MACROMAN			: M_ A_ C_ R_ O_ M_ A_ N_  ;
//SJIS				: S_ J_ I_ S_  ;
//SWE7				: S_ W_ E_ '7'  ;
//TIS620				: T_ I_ S_ '620'  ;
//UCS2				: U_ C_ S_ '2';
//UJIS				: U_ J_ I_ S_  ;
UTF8				: U_ T_ F_ '8'  ;

//pg_sphere
SPOINT              : S_ P_ O_ I_ N_ T_ ;
SCIRCLE             : S_ C_ I_ R_ C_ L_ E_ ;
SLINE               : S_ L_ I_ N_ E_ ;
SELLIPSE            : S_ E_ L_ L_ I_ P_ S_ E_ ;
SPOLY               : S_ P_ O_ L_ Y_ ;
SPATH               : S_ P_ A_ T_ H_ ;
SBOX                : S_ B_ O_ X_ ;
STRANS              : S_ T_ R_ A_ N_ S_ ;
AREA                : A_ R_ E_ A_ ;

ARRAY_LENGTH        : A_ R_ R_ A_ Y_ '_' L_ E_ N_ G_ T_ H_ ;

// basic token definition -----------------------------------------------------

DIVIDE	    : (  D_ I_ V_ ) | '/' ;
MOD_SYM	    : (  M_ O_ D_ ) | '%' ;
OR_SYM	    : (  O_ R_ ) | '||';
AND_SYM	    : (  A_ N_ D_ ) | '&&';

ABS_VAL_OR_SCONTAINS     : '@';
DFACTORIAL   : '!!';

EQ          : '=' | '<=>' ;
NOT_EQ	    : '<>' | '!=' | '~='| '^=';
LET	        : '<=' ;
GET	        : '>=' ;
SHIFT_LEFT	: '<<' ;
SHIFT_RIGHT	: '>>' ;

SEMI	    : ';' ;
COLON	    : ':' ;
DOT	        : '.' ;
COMMA	    : ',' ;
ASTERISK    : '*' ;
RPAREN	    : ')' ;
LPAREN	    : '(' ;
RBRACK	    : ']' ;
LBRACK	    : '[' ;
PLUS	    : '+' ;
MINUS	    : '-' ;
NEGATION    : '~' ;
VERTBAR	    : '|' ;
BITAND	    : '&' ;
POWER_OP    : '^' ;
GTH	        : '>' ;
LTH	        : '<' ;

// pg_sphere operators - those that are commented out are already used by postgres

//SCONTAINS           : '@' ;
SCONTAINS2          : '<@' ;
//SLEFTCONTAINS       : '~' ;
SLEFTCONTAINS2      : '@>' ;
SNOTCONTAINS        : '!@' ;
SNOTCONTAINS2       : '!<@' ;
SLEFTNOTCONTAINS    : '!~' ;
SLEFTNOTCONTAINS2   : '!@>' ;
//SOVERLAP            : '&&' ;
SNOTOVERLAP         : '!&&' ;
SCROSS              : '#' ;
SDISTANCE           : '<->' ;
SLENGTH             : '@-@' ;
SCENTER             : '@@' ;

INTEGER_NUM		: ('0'..'9')+ ;

fragment HEX_DIGIT_FRAGMENT: ( 'a'..'f' | 'A'..'F' | '0'..'9' ) ;
HEX_DIGIT:
	(  '0x'     (HEX_DIGIT_FRAGMENT)+  )
	|
	(  'X' '\'' (HEX_DIGIT_FRAGMENT)+ '\''  )
;

BIT_NUM:
	(  '0b'    ('0'|'1')+  )
	|
	(  B_ '\'' ('0'|'1')+ '\''  )
;

REAL_NUMBER:
	(  INTEGER_NUM DOT INTEGER_NUM | INTEGER_NUM DOT | DOT INTEGER_NUM | INTEGER_NUM  )
	(  ('E'|'e') ( PLUS | MINUS )? INTEGER_NUM  )?
;

TRANS:
    '\''( 'X' | 'Y' | 'Z' )( 'X' | 'Y' | 'Z' )( 'X' | 'Y' | 'Z' )'\''
;

TEXT_STRING:
	( N_ | ('_' U_ T_ F_ '8') )?
	(
		(  '\'' ( ('\\' '\\') | ('\'' '\'') | ('\\' '\'') | ~('\'') )* '\''  )

	)
;

ID:
	(( 'A'..'Z' | 'a'..'z' | '_' | '$' ) ( 'A'..'Z' | 'a'..'z' | '_' | '$' | '0'..'9' )*) |
	( '"' ( ( '\u0023' .. '\uffff' ) | ( '\u0020' ) )+ '"' )
;


COMMENT: '--' ~( '\r' | '\n' )* -> skip ;

// all unicode whitespace characters
WS
   : ( ' ' | '\t' | '\n' | '\r' | '\u000b' | '\u000c' |
   '\u0085' | '\u00a0' | '\u1680' | '\u2000' | '\u2001' | '\u2002' | '\u2003' |
   '\u2004' | '\u2005' | '\u2006' | '\u2007' | '\u2008' | '\u2009' | '\u200a' | '\u2028' |
   '\u2029' | '\u202f' | '\u205f' | '\u3000' )+ -> channel(HIDDEN)
;

