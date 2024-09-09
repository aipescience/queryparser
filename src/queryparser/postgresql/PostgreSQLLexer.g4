
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
BIT_LENGTH			: B_ I_ T_ '_' L_ E_ N_ G_ T_ H_;
BIT_OR				: B_ I_ T_ '_' O_ R_  ;
BOOLEAN_SYM			: B_ O_ O_ L_ E_ A_ N_  ;
BY_SYM				: B_ Y_ ;
CASE_SYM			: C_ A_ S_ E_  ;
CAST_SYM			: C_ A_ S_ T_  ;
CBRT                : C_ B_ R_ T_ ;
CEIL				: C_ E_ I_ L_  ;
CEILING				: C_ E_ I_ L_ I_ N_ G_  ;
CHAR				: C_ H_ A_ R_  ;
CHR                 : C_ H_ R_ ;
CHAR_LENGTH			: (C_ H_ A_ R_ '_' L_ E_ N_ G_ T_ H_) | (C_ H_ A_ R_ A_ C_ T_ E_ R_ '_' L_ E_ N_ G_ T_ H_) ;
CONCAT				: C_ O_ N_ C_ A_ T_  ;
CONCAT_WS			: C_ O_ N_ C_ A_ T_ '_' W_ S_  ;
CONVERT_SYM			: C_ O_ N_ V_ E_ R_ T_  ;
COS				    : C_ O_ S_  ;
COT				    : C_ O_ T_  ;
COUNT				: C_ O_ U_ N_ T_  ;
CROSS				: C_ R_ O_ S_ S_  ;
DATE_PART           : D_ A_ T_ E_ '_' P_ A_ R_ T_ ;
DATE_SYM			: D_ A_ T_ E_  ;
DATETIME			: D_ A_ T_ E_ T_ I_ M_ E_  ;
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
FALSE_SYM			: F_ A_ L_ S_ E_ ;
FIRST_SYM           : F_ I_ R_ S_ T_ ;
FLOAT               : F_ L_ O_ A_ T_ ;
FLOOR				: F_ L_ O_ O_ R_  ;
FOR_SYM				: F_ O_ R_  ;
FORCE_SYM           : F_ O_ R_ C_ E_ ;
FROM				: F_ R_ O_ M_  ;
GAIA_HEALPIX_INDEX  : G_ A_ I_ A_ '_' H_ E_ A_ L_ P_ I_ X_ '_' I_ N_ D_ E_ X_ ;
GROUP_SYM			: G_ R_ O_ U_ P_  ;
HAVING				: H_ A_ V_ I_ N_ G_  ;
IGNORE_SYM			: I_ G_ N_ O_ R_ E_  ;
ILIKE_SYM			: I_ L_ I_ K_ E_  ;
INDEX_SYM			: I_ N_ D_ E_ X_  ;
INNER_SYM			: I_ N_ N_ E_ R_  ;
INTEGER_SYM			: I_ N_ T_ E_ G_ E_ R_  ;
INTERVAL_SYM		: I_ N_ T_ E_ R_ V_ A_ L_  ;
IN_SYM				: I_ N_  ;
ISNULL              : I_ S_ N_ U_ L_ L_ ;
IS_SYM				: I_ S_  ;
JOIN_SYM			: J_ O_ I_ N_  ;
KEY_SYM				: K_ E_ Y_  ;
LAST_SYM            : L_ A_ S_ T_ ;
LEFT				: L_ E_ F_ T_  ;
LENGTH				: (L_ E_ N_ G_ T_ H_) | (O_ C_ T_ E_ T_ '_' L_ E_ N_ G_ T_ H_) ;
LIKE_SYM			: L_ I_ K_ E_  ;
LIMIT				: L_ I_ M_ I_ T_  ;
LN				    : L_ N_  ;
LOG				    : L_ O_ G_  ;
LOWER				: (L_ O_ W_ E_ R_) | (L_ C_ A_ S_ E_) ;
LPAD				: L_ P_ A_ D_  ;
LTRIM				: L_ T_ R_ I_ M_  ;
MAX_SYM				: M_ A_ X_  ;
MD5				    : M_ D_ '5'  ;
MINUTE				: M_ I_ N_ U_ T_ E_  ;
MIN_SYM				: M_ I_ N_  ;
MOD				    : M_ O_ D_  ;
MODE_SYM			: M_ O_ D_ E_  ;
NATURAL             : N_ A_ T_ U_ R_ A_ L_ ;
NOT_SYM				: (N_ O_ T_) | ('!') ;
NOTNULL             : N_ O_ T_ N_ U_ L_ L_ ;
NOW				    : (N_ O_ W_) | (L_ O_ C_ A_ L_ T_ I_ M_ E_) | (L_ O_ C_ A_ L_ T_ I_ M_ E_ S_ T_ A_ M_ P_) | (C_ U_ R_ R_ E_ N_ T_ '_' T_ I_ M_ E_ S_ T_ A_ M_ P_);
NULL_SYM			: N_ U_ L_ L_  ;
NULLS_SYM           : N_ U_ L_ L_ S_ ;
NUMERIC             : N_ U_ M_ E_ R_ I_ C_ ;
OFFSET_SYM			: O_ F_ F_ S_ E_ T_  ;
OJ_SYM				: O_ J_  ;
ON				    : O_ N_  ;
ORDER_SYM			: O_ R_ D_ E_ R_  ;
OUTER				: O_ U_ T_ E_ R_  ;
PARTITION_SYM		: P_ A_ R_ T_ I_ T_ I_ O_ N_  ;
PDIST               : P_ D_ I_ S_ T_ ;
PI				    : P_ I_  ;
POSITION_SYM        : P_ O_ S_ I_ T_ I_ O_ N_ ;
POW				    : P_ O_ W_  ;
POWER				: P_ O_ W_ E_ R_  ;
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
SELECT				: S_ E_ L_ E_ C_ T_ ;
SHARE_SYM			: S_ H_ A_ R_ E_  ;
SIGN				: S_ I_ G_ N_  ;
SIGNED_SYM			: S_ I_ G_ N_ E_ D_  ;
SIN				    : S_ I_ N_  ;
SOUNDS_SYM          : S_ O_ U_ N_ D_ S_ ;
SQUARE_DEGREES      : S_ Q_ U_ A_ R_ E_ '_' D_ E_ G_ R_ E_ E_ S_ ;
SQRT				: S_ Q_ R_ T_  ;
STDDEV				: S_ T_ D_ D_ E_ V_  ;
STDDEV_POP			: S_ T_ D_ D_ E_ V_ '_' P_ O_ P_  ;
STDDEV_SAMP			: S_ T_ D_ D_ E_ V_ '_' S_ A_ M_ P_  ;
STERADIANS          : S_ T_ E_ R_ A_ D_ I_ A_ N_ S_ ;
STRAIGHT_JOIN		: S_ T_ R_ A_ I_ G_ H_ T_  '_' J_ O_ I_ N_  ;
SUBSTRING			: (S_ U_ B_ S_ T_ R_ I_ N_ G_) | (S_ U_ B_ S_ T_ R_) ;
SUM				    : S_ U_ M_  ;
SYMMETRIC           : S_ Y_ M_ M_ E_ T_ R_ I_ C_ ;
TAN				    : T_ A_ N_  ;
THEN_SYM			: T_ H_ E_ N_  ;
TIME_SYM			: T_ I_ M_ E_  ;
TIMESTAMP			: T_ I_ M_ E_ S_ T_ A_ M_ P_  ;
TRUE_SYM			: T_ R_ U_ E_ ;
TRUNC				: T_ R_ U_ N_ C_  ;
UNION_SYM			: U_ N_ I_ O_ N_  ;
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
WHEN_SYM			: W_ H_ E_ N_ 	;
WHERE				: W_ H_ E_ R_ E_  ;
WITH				: W_ I_ T_ H_  ;
YEAR				: Y_ E_ A_ R_  ;

// character sets
ASCII_SYM			: A_ S_ C_ I_ I_  ;
LATIN1				: L_ A_ T_ I_ N_ '1'  ;
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
SPOINT_TO_ARRAY     : S_ P_ O_ I_ N_ T_ '_' T_ O_ '_' A_ R_ R_ A_ Y_ ;
SBOX_TO_ARRAY       : S_ B_ O_ X_ '_' T_ O_ '_' A_ R_ R_ A_ Y_ ;
SCIRCLE_TO_ARRAY    : S_ C_ I_ R_ C_ L_ E_ '_' T_ O_ '_' A_ R_ R_ A_ Y_ ;
SPOLY_TO_ARRAY      : S_ P_ O_ L_ Y_ '_' T_ O_ '_' A_ R_ R_ A_ Y_ ;
SPOINT_TO_ARRAY_DEG : S_ P_ O_ I_ N_ T_ '_' T_ O_ '_' A_ R_ R_ A_ Y_ '_' D_ E_ G_ ;
SBOX_TO_ARRAY_DEG   : S_ B_ O_ X_ '_' T_ O_ '_' A_ R_ R_ A_ Y_ '_' D_ E_ G_ ;
SCIRCLE_TO_ARRAY_DEG : S_ C_ I_ R_ C_ L_ E_ '_' T_ O_ '_' A_ R_ R_ A_ Y_ '_' D_ E_ G_ ;
SPOLY_TO_ARRAY_DEG  : S_ P_ O_ L_ Y_ '_' T_ O_ '_' A_ R_ R_ A_ Y_ '_' D_ E_ G_ ;

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

