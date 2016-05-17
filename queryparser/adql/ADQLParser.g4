parser grammar ADQLParser;

options
   { tokenVocab = ADQLLexer; }

catalog_name:                   identifier ;
correlation_name:               identifier ;
column_name:                    identifier ;
schema_name:                    ( catalog_name DOT )? unqualified_schema_name ;
table_name:                     ( schema_name DOT )? identifier;
user_defined_function_name:     identifier ;
unqualified_schema_name:        identifier ;

area:                           AREA LPAREN geometry_value_expression RPAREN ;
as_clause:                      ( AS )? column_name ;
between_predicate:              value_expression ( NOT )? BETWEEN value_expression AND value_expression ;
boolean_factor:                 ( NOT )? boolean_primary ;
boolean_primary:                LPAREN search_condition RPAREN | predicate ;
boolean_term:                   boolean_factor | boolean_term AND boolean_factor ;
box:                            BOX LPAREN coord_sys COMMA coordinates COMMA numeric_value_expression COMMA numeric_value_expression RPAREN ;
centroid:                       CENTROID LPAREN geometry_value_expression RPAREN ;
character_string_literal:		ID ;
character_value_expression:     character_value_expression CONCAT character_factor | character_factor ;
character_factor:               character_primary ;
character_primary:              value_expression_primary | string_value_function ;
circle:                         CIRCLE LPAREN coord_sys COMMA coordinates COMMA radius RPAREN ;
column_name_list:               column_name ( COMMA column_name )* ;
column_reference:               ( qualifier DOT )? column_name ;
comp_op:                        EQ | NOT_EQ | LTH | GTH | LEET | GRET ;
comparison_predicate:           value_expression comp_op value_expression ;
contains:                       CONTAINS LPAREN geometry_value_expression COMMA geometry_value_expression RPAREN ;
coord1:                         COORD1 LPAREN coord_value RPAREN ;
coord2:                         COORD2 LPAREN coord_value RPAREN ;
coord_sys:                      string_value_expression ;
coord_value:                    point | column_reference ;
coordinate1:                    numeric_value_expression ;
coordinate2:                    numeric_value_expression ;
coordinates:                    coordinate1 COMMA coordinate2 ;
correlation_specification:      ( AS )? correlation_name ;
//delimited_identifier:           DID ;
derived_column:                 value_expression ( as_clause )? ;
derived_table:                  table_subquery ;
distance:                       DISTANCE LPAREN coord_value COMMA coord_value RPAREN ;
exists_predicate:               EXISTS table_subquery ;
extract_coordsys:               COORDSYS LPAREN geometry_value_expression RPAREN ;
factor:                         ( PLUS | MINUS )? numeric_primary ;
from_clause:                    FROM table_reference ( COMMA table_reference )*;
general_literal:                character_string_literal ;
general_set_function:           set_function_type LPAREN ( set_quantifier )? value_expression RPAREN ;
geometry_value_expression:      value_expression_primary | geometry_value_function ;
geometry_value_function:        box | centroid | circle | point | polygon | region ;
group_by_clause:                GROUP BY grouping_column_reference_list ;
grouping_column_reference:      column_reference ;
grouping_column_reference_list: grouping_column_reference ( COMMA grouping_column_reference )* ;
having_clause:                  HAVING search_condition ;
identifier:                     regular_identifier ;//| delimited_identifier ;
in_predicate:                   value_expression ( NOT )? IN in_predicate_value ;
in_predicate_value:             table_subquery | LPAREN in_value_list LPAREN ;
in_value_list:                  value_expression ( COMMA value_expression )* ;
intersects:                     INTERSECTS LPAREN geometry_value_expression COMMA geometry_value_expression RPAREN ;
join_column_list:               column_name_list ;
join_condition:                 ON search_condition ;
join_specification:             join_condition | named_columns_join ;
join_type:                      INNER | outer_join_type ( OUTER )? ;
joined_table:                   qualified_join | LPAREN joined_table RPAREN ;
//joined_table:                   table_reference ( NATURAL )? ( join_type )? JOIN table_reference ( join_specification )? | LPAREN joined_table RPAREN ;
like_predicate:                 match_value ( NOT )? LIKE pattern ;
math_function:                    ABS LPAREN numeric_value_expression RPAREN
                                | CEILING LPAREN numeric_value_expression RPAREN
                                | EXP LPAREN numeric_value_expression RPAREN
                                | FLOOR LPAREN numeric_value_expression RPAREN
                                | LOG LPAREN numeric_value_expression RPAREN
                                | LOG10 LPAREN numeric_value_expression RPAREN
                                | MOD LPAREN numeric_value_expression RPAREN
                                | PI LPAREN numeric_value_expression RPAREN
                                | POWER LPAREN numeric_value_expression RPAREN
                                | RADIANS LPAREN numeric_value_expression RPAREN
                                | RAND LPAREN numeric_value_expression RPAREN
                                | ROUND LPAREN numeric_value_expression RPAREN
                                | SQRT LPAREN numeric_value_expression RPAREN
                                | TRUNCATE LPAREN numeric_value_expression RPAREN
;
match_value:                    character_value_expression ;
named_columns_join:             USING LPAREN join_column_list RPAREN ;
non_predicate_geometry_function:area | coord1 | coord2 | distance ;
null_predicate:                 column_reference IS ( NOT )? NULL ;
numeric_geometry_function:      predicate_geometry_function | non_predicate_geometry_function ;
numeric_primary:                value_expression_primary | numeric_value_function ;
numeric_value_expression:       term | numeric_value_expression PLUS term | numeric_value_expression MINUS ;
numeric_value_function:         trig_function | math_function | numeric_geometry_function | user_defined_function ;
order_by_clause:                ORDER BY sort_specification_list;
ordering_specification:         ASC | DESC ;
outer_join_type:                LEFT | RIGHT | FULL ;
pattern:                        character_value_expression ;
point:                          POINT LPAREN coord_sys COMMA coordinates RPAREN ;
polygon:                        POLYGON LPAREN coord_sys COMMA coordinates COMMA coordinates ( COMMA coordinates )? RPAREN ;
predicate:                      comparison_predicate | between_predicate | in_predicate | like_predicate | null_predicate | exists_predicate ;
predicate_geometry_function:    contains | intersects ;
qualifier:                      table_name | correlation_name ;
qualified_join:                 table_reference ( NATURAL )? ( join_type )? JOIN table_reference ( join_specification )? ;
query_expression:               query_specification | joined_table ;
query_specification:            SELECT ( set_quantifier )? ( set_limit )? select_list table_expression ;
radius:                         numeric_value_expression ;
region:                         REGION LPAREN string_value_expression RPAREN ;
regular_identifier:             ID ;
search_condition:               boolean_term | search_condition OR boolean_term ;
select_list:                    ASTERISK | select_sublist ( COMMA select_sublist )* ;
select_sublist:                 derived_column | qualifier DOT ASTERISK ;
set_function_specification:     COUNT LPAREN ASTERISK RPAREN | general_set_function ;
set_function_type:              AVG | MAX | MIN | SUM | COUNT ;
set_limit:                      TOP INT ;
set_quantifier:                 DISTINCT | ALL ;
sort_key:                       column_name | INT ;
sort_specification:             sort_key ( ordering_specification )? ;
sort_specification_list:        sort_specification ( COMMA sort_specification )* ;
string_geometry_function:       extract_coordsys ;
string_value_expression:        character_value_expression ;
string_value_function:          string_geometry_function | user_defined_function ;
subquery:                       LPAREN query_expression RPAREN ;
table_expression:               from_clause ( where_clause )? ( group_by_clause )? ( having_clause )? ( order_by_clause )? ;
//table_reference:                table_name ( correlation_specification )? | derived_table correlation_specification | joined_table ;
table_reference:                table_name ( correlation_specification )? | derived_table correlation_specification | table_reference ( NATURAL )? ( join_type )? JOIN table_reference ( join_specification )? ;
table_subquery:                 subquery ;
term:                           factor | term ASTERISK factor | term SOLIDUS factor ;
trig_function:                    ACOS LPAREN numeric_value_expression RPAREN
                                | ASIN LPAREN numeric_value_expression RPAREN
                                | ATAN LPAREN numeric_value_expression RPAREN
                                | ATAN2 LPAREN numeric_value_expression COMMA numeric_value_expression RPAREN
                                | COS LPAREN numeric_value_expression RPAREN
                                | COT LPAREN numeric_value_expression RPAREN
                                | SIN LPAREN numeric_value_expression RPAREN
                                | TAN LPAREN numeric_value_expression RPAREN
;
unsigned_literal:               unsigned_numeric_literal | general_literal ;
unsigned_numeric_literal:       ( INT | REAL ) ;
unsigned_value_specification:   unsigned_literal ;
user_defined_function:          user_defined_function_name LPAREN ( user_defined_function_param ( COMMA user_defined_function_param )* )? RPAREN ;
user_defined_function_param:    value_expression;
value_expression:               numeric_value_expression | string_value_expression | geometry_value_expression ;
value_expression_primary:       unsigned_value_specification | column_reference | set_function_specification | LPAREN value_expression RPAREN ;
where_clause:                   WHERE search_condition ;