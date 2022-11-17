parser grammar ADQLParser;

options
   { tokenVocab = ADQLLexer; }

approximate_numeric_literal:    REAL ;
area:                           AREA LPAREN geometry_value_expression RPAREN ;
as_clause:                      ( AS )? column_name ;
between_predicate:              value_expression ( NOT )? BETWEEN value_expression AND value_expression ;
bitwise_and:                    AMPERSAND ;
bitwise_not:                    TILDE ;
bitwise_or:                     VERTBAR ;
bitwise_xor:                    CIRCUMFLEX ;
boolean_factor:                 ( NOT )? boolean_primary ;
//boolean_function:             // This is empty in the document!
boolean_literal:                TRUE | FALSE ;
boolean_primary:                LPAREN search_condition RPAREN | predicate | boolean_value_expression ;
boolean_term:                   boolean_factor | boolean_term AND boolean_factor ;
boolean_value_expression:       boolean_literal | user_defined_function ; //| boolean_function ;
box:
          BOX
          LPAREN
          coord_sys COMMA coordinates COMMA numeric_value_expression COMMA numeric_value_expression
          RPAREN ;
catalog_name:                   ID ;
centroid:                       CENTROID LPAREN geometry_value_expression RPAREN ;
//character_representation:       nonquote_character ;// | SQ SQ ;
char_function:                  LOWER LPAREN character_string_literal RPAREN ;
character_string_literal:       CSL ; //SQ ( SL )* SQ ; //SQ ( character_representation )* SQ ;
character_value_expression:
          character_value_expression concatenation_operator ( value_expression_primary | string_value_function )
        | value_expression_primary
        | string_value_function ;
circle:                         CIRCLE LPAREN coord_sys COMMA coordinates COMMA radius RPAREN ;
column_name:                    identifier ;
column_name_list:               column_name ( COMMA column_name )* ;
column_reference:               ( qualifier DOT )? column_name ;
comp_op:                        EQ | NOT_EQ | LTH | GTH | GRET | LEET ;
comparison_predicate:           value_expression comp_op value_expression ;
concatenation_operator:         CONCAT ;
contains:                       CONTAINS LPAREN geometry_value_expression COMMA geometry_value_expression RPAREN ;
coord_sys:                      string_value_expression ;
coord_value:                    point | column_reference | centroid ;
coord1:                         COORD1 LPAREN coord_value RPAREN ;
coord2:                         COORD2 LPAREN coord_value RPAREN ;
coordinate1:                    numeric_value_expression ;
coordinate2:                    numeric_value_expression ;
coordinates:                    coordinate1 COMMA coordinate2 ;
correlation_name:               identifier ;
correlation_specification:      ( AS )? correlation_name ;
//default_function_prefix:      // this is empty in the document!
delimited_identifier:           DQ ID DQ ;
derived_column:                 value_expression ( as_clause )? ;
derived_table:                  table_subquery ;
distance:
          DISTANCE
          LPAREN (
          ( coord_value COMMA coord_value ) |
          ( numeric_value_expression COMMA numeric_value_expression COMMA
            numeric_value_expression COMMA numeric_value_expression )
          ) RPAREN ;
//double_quote_symbol:            DQ DQ ;
exact_numeric_literal:          unsigned_decimal ( DOT ( unsigned_decimal )? )? | DOT unsigned_decimal;
exists_predicate:               EXISTS table_subquery ;
extract_coordsys:               COORDSYS LPAREN geometry_value_expression RPAREN ;
factor:                         ( sign )? numeric_primary ;
from_clause:                    FROM table_reference ( COMMA table_reference )* ;
general_literal:                character_string_literal ;
general_set_function:           set_function_type LPAREN ( set_quantifier )? value_expression RPAREN ;
geometry_value_expression:      box | centroid | circle | point | polygon | region | user_defined_function ;
group_by_clause:                GROUP BY grouping_column_reference_list ;
grouping_column_reference:      column_reference ;
grouping_column_reference_list: grouping_column_reference ( COMMA grouping_column_reference )* ;
having_clause:                  HAVING search_condition ;
identifier:                     regular_identifier | delimited_identifier ;
in_predicate:                   value_expression ( NOT )? IN in_predicate_value ;
in_predicate_value:             table_subquery | LPAREN in_value_list RPAREN ;
in_value_list:                  value_expression ( COMMA value_expression )* ;
intersects:                     INTERSECTS LPAREN geometry_value_expression COMMA geometry_value_expression RPAREN ;
join_column_list:               column_name_list ;
join_condition:                 ON search_condition ;
join_specification:             join_condition  | named_columns_join ;
join_type:                      INNER | outer_join_type ( OUTER )? ;
joined_table:
          table_reference ( NATURAL )? ( join_type )? JOIN table_reference ( join_specification )?
        | LPAREN joined_table RPAREN ;
like_predicate:                 match_value ( NOT )? LIKE pattern | match_value ( NOT )? ILIKE pattern ;
match_value:                    character_value_expression ;
math_function:
          ABS LPAREN numeric_value_expression RPAREN
        | CEILING LPAREN numeric_value_expression RPAREN
        | DEGREES LPAREN numeric_value_expression RPAREN
        | EXP LPAREN numeric_value_expression RPAREN
        | FLOOR LPAREN numeric_value_expression RPAREN
        | LOG LPAREN numeric_value_expression RPAREN
        | LOG10 LPAREN numeric_value_expression RPAREN
        | MOD LPAREN numeric_value_expression COMMA numeric_value_expression RPAREN
        | PI LPAREN RPAREN
        | POWER LPAREN numeric_value_expression COMMA numeric_value_expression RPAREN
        | RADIANS LPAREN numeric_value_expression RPAREN
        | RAND LPAREN ( unsigned_decimal )? RPAREN
        | ROUND LPAREN numeric_value_expression ( COMMA signed_integer )? RPAREN
        | SQRT LPAREN numeric_value_expression RPAREN
        | TRUNCATE LPAREN numeric_value_expression ( COMMA signed_integer )? RPAREN ;
named_columns_join:             USING LPAREN join_column_list RPAREN ;
non_join_query_expression:      non_join_query_term | query_expression UNION ( ALL )? query_term
        | query_expression EXCEPT ( ALL )? query_term ;
non_join_query_primary:         query_specification | LPAREN non_join_query_expression RPAREN ;
non_join_query_term:            non_join_query_primary | query_term INTERSECT ( ALL )? query_expression ;
non_predicate_geometry_function:area | coord1 | coord2 | distance ;
//nondoublequote_character:       NDQC ;
//nonquote_character:             NQC ;
null_predicate:                 column_reference IS ( NOT )? NULL ;
numeric_geometry_function:      predicate_geometry_function | non_predicate_geometry_function ;
numeric_primary:                ( sign )? value_expression_primary | numeric_value_function ;
numeric_value_expression:
          term
        | bitwise_not numeric_value_expression
        | numeric_value_expression bitwise_and numeric_value_expression
        | numeric_value_expression bitwise_or  numeric_value_expression
        | numeric_value_expression bitwise_xor numeric_value_expression
        | numeric_value_expression PLUS term
        | numeric_value_expression MINUS term ;
numeric_value_function:         trig_function | math_function | numeric_geometry_function | user_defined_function ;
offset_clause:                  OFFSET unsigned_decimal ;
order_by_clause:                ORDER BY sort_specification_list ;
ordering_specification:         ASC | DESC ;
outer_join_type:                LEFT | RIGHT | FULL ;
pattern:                        character_value_expression ;
point:                          POINT LPAREN coord_sys COMMA coordinates RPAREN ;
polygon:                        POLYGON LPAREN coord_sys COMMA coordinates COMMA
          coordinates ( COMMA coordinates )+ RPAREN ;
predicate:
          comparison_predicate
        | between_predicate
        | in_predicate
        | like_predicate
        | null_predicate
        | exists_predicate ;
predicate_geometry_function:    contains | intersects ;
qualifier:                      column_name | table_name | correlation_name ;
query_expression:
          non_join_query_term
        | query_expression UNION ( ALL )? query_term
        | query_expression EXCEPT ( ALL )? query_term
        | joined_table ;
query_name:                     ID ;
query:                          query_expression SEMI;
query_specification:            ( WITH with_query )? select_query ;
query_term:                     non_join_query_primary | query_term INTERSECT ( ALL )? query_expression | joined_table ;
radius:                         numeric_value_expression ;
region:                         REGION LPAREN string_value_expression RPAREN ;
regular_identifier:             ID ;
schema_name:                    ID ; //( catalog_name DOT )? unqualified_schema_name ;
search_condition:               boolean_term | search_condition OR boolean_term ;
select_list:                    ( select_sublist ( COMMA select_sublist )* ) | ( ASTERISK ( COMMA select_sublist ( COMMA select_sublist )* )? ) ;
select_query:                   SELECT ( set_quantifier )? ( set_limit )? select_list table_expression ;
select_sublist:                 derived_column | qualifier DOT ASTERISK ;
set_function_specification:     COUNT LPAREN ASTERISK RPAREN | general_set_function ;
set_function_type:              AVG | MAX | MIN | SUM | COUNT ;
set_limit:                      TOP unsigned_decimal ;
set_quantifier:                 DISTINCT | ALL ;
sign:                           PLUS | MINUS ;
signed_integer:                 ( sign )? unsigned_decimal ;
sort_key:                       value_expression| column_reference | unsigned_decimal ;
sort_specification:             sort_key (ordering_specification )? ;
sort_specification_list:        sort_specification ( COMMA sort_specification )* ;
string_geometry_function:       extract_coordsys ;
string_value_expression:        character_value_expression ;
string_value_function:          string_geometry_function | user_defined_function | char_function;
subquery:                       LPAREN query_expression RPAREN ;
table_expression:
          from_clause
          ( where_clause )?
          ( group_by_clause )?
          ( having_clause )?
          ( order_by_clause )?
          ( offset_clause )? ;
table_name:                     ( schema_name DOT )? identifier ;
table_reference:
          table_name ( correlation_specification )?
        | derived_table correlation_specification
        | table_reference ( NATURAL )? ( join_type )? JOIN table_reference ( join_specification )?
        | LPAREN joined_table RPAREN ;
table_subquery:                 subquery ;
term:                           factor | term ASTERISK factor | term SOLIDUS factor | term MOD_SYM factor;
trig_function:                  ACOS LPAREN numeric_value_expression RPAREN
        | ACOS LPAREN numeric_value_expression RPAREN
        | ASIN LPAREN numeric_value_expression RPAREN
        | ATAN LPAREN numeric_value_expression RPAREN
        | ATAN2 LPAREN numeric_value_expression COMMA numeric_value_expression RPAREN
        | COS LPAREN numeric_value_expression RPAREN
        | COT LPAREN numeric_value_expression RPAREN
        | SIN LPAREN numeric_value_expression RPAREN
        | TAN LPAREN numeric_value_expression RPAREN ;
unqualified_schema_name:        ID ;
unsigned_decimal:               INT ;
unsigned_hexadecimal:           HEX_DIGIT ;
unsigned_literal:               unsigned_numeric_literal | general_literal ;
unsigned_numeric_literal:       exact_numeric_literal | approximate_numeric_literal | unsigned_hexadecimal ;
unsigned_value_specification:   unsigned_literal ;
user_defined_function:
          user_defined_function_name
          LPAREN
          ( user_defined_function_param ( COMMA user_defined_function_param )* )?
          RPAREN ;
user_defined_function_name:     regular_identifier ; //( default_function_prefix )? regular_identifier ;
user_defined_function_param:    value_expression ;
value_expression:
          numeric_value_expression
        | string_value_expression
        | boolean_value_expression
        | geometry_value_expression ;
value_expression_primary:
          unsigned_value_specification
        | column_reference
        | set_function_specification
        | LPAREN value_expression RPAREN ;
where_clause:                   WHERE search_condition ;
with_query:                     query_name ( LPAREN column_name ( COMMA column_name )* RPAREN )? AS LPAREN ( query_specification )? RPAREN  ;
