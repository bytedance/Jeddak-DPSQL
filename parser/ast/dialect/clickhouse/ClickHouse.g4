grammar ClickHouse;


query
    : selectUnionStmt
    ;


// SELECT statement
selectUnionStmt: selectStmtWithParens (stmtUnionFlag selectStmtWithParens)*;

stmtUnionFlag
    : UNION ALL                             # StmtUnionAll
    | UNION DISTINCT                        # StmtUnionDistinct
    | UNION                                 # StmtUnion
    ;

selectStmtWithParens: selectStmt | LPAREN selectUnionStmt RPAREN;
selectStmt:
    withClause?
    selectClause
    fromClause?
    arrayJoinClause?
    prewhereClause?
    whereClause?
    groupByClause?
    havingClause?
    orderByClause?
    limitByClause?
    limitClause?
    tealimitClause?
    settingsClause?
    formatClause?
    ;

formatClause: FORMAT identifier;
selectClause: SELECT DISTINCT? topClause? columnExprList;
withClause: WITH columnExprList;
topClause: TOP DECIMAL_LITERAL (WITH TIES)?;
fromClause: FROM joinExpr;
arrayJoinClause: (LEFT | INNER)? ARRAY JOIN columnExprList;
prewhereClause: PREWHERE columnExpr;
whereClause: WHERE columnExpr;
groupByClause
    : GROUP BY (CUBE | ROLLUP) LPAREN columnExprList RPAREN groupByTailFlag?      # GroupFrontCr
    | GROUP BY columnExprList groupByTailFlag?                                    # GroupNoFrontCr
    ;
havingClause: HAVING columnExpr;
orderByClause: ORDER BY orderExprList;
limitByClause: LIMIT limitExpr BY columnExprList;
limitClause: LIMIT limitExpr (WITH TIES)?;
tealimitClause : TEALIMIT n=numberLiteral GROUP groupExp=columnExprList ORDER orderExp=columnExprList ordering=(ASCENDING | DESC)?;
settingsClause: SETTINGS settingExprList;

groupByTailFlag
    : WITH CUBE                                                              # GroupWithCube
    | WITH ROLLUP                                                            # GroupWithRollup
    | WITH TOTALS                                                            # GroupWithTotals
    ;
joinExpr
    : joinExpr (GLOBAL | LOCAL)? joinOp? JOIN joinExpr joinConstraintClause  # JoinExprOp
    | joinExpr joinOpCross joinExpr                                          # JoinExprCrossOp
    | tableExpr FINAL? sampleClause?                                         # JoinExprTable
    | LPAREN joinExpr RPAREN                                                 # JoinExprParens
    ;
joinOp
    : (ALL | ANY | ASOF)? INNER                                             # JoinOpInner1
    | INNER (ALL | ANY | ASOF)?                                             # JoinOpInner2
    | (ALL | ANY | ASOF)                                                    # JoinOpInner3
    | (SEMI | ALL | ANTI | ANY | ASOF)? (LEFT | RIGHT) OUTER?               # JoinOpLeftRight1
    | (LEFT | RIGHT) OUTER? (SEMI | ALL | ANTI | ANY | ASOF)?               # JoinOpLeftRight2
    | (ALL | ANY)? FULL OUTER?                                              # JoinOpFull1
    | FULL OUTER? (ALL | ANY)?                                              # JoinOpFull2
    ;
joinOpCross
    : (GLOBAL|LOCAL)? CROSS JOIN
    | COMMA
    ;
joinConstraintClause
    : ON columnExprList
    | USING LPAREN columnExprList RPAREN
    | USING columnExprList
    ;

sampleClause: SAMPLE ratioExpr (OFFSET ratioExpr)?;
limitExpr: columnExpr ((COMMA | OFFSET) columnExpr)?;
orderExprList: orderExpr (COMMA orderExpr)*;
orderExpr: columnExpr (ASCENDING | DESCENDING | DESC)? (NULLS (FIRST | LAST))? (COLLATE STRING_LITERAL)?;
ratioExpr: numberLiteral (SLASH numberLiteral)?;
settingExprList: settingExpr (COMMA settingExpr)*;
settingExpr: identifier EQ_SINGLE literal;


// Columns

columnTypeExpr
    : identifier                                                                             # ColumnTypeExprSimple   // UInt64
    | identifier LPAREN identifier columnTypeExpr (COMMA columnDefinitionExpr)* RPAREN       # ColumnTypeExprNested   // Nested
    | identifier LPAREN enumValue (COMMA enumValue)* RPAREN                                  # ColumnTypeExprEnum     // Enum
    | ttype=tupleOrArrayName LPAREN columnExprList? RPAREN                                   # ColumnTypeExprComplex  // Array, Tuple
    | decimaltype=decimalTypeName LPAREN columnExprList? RPAREN                              # ColumnTypeDecimal
    | identifier LPAREN columnExprList? RPAREN                                               # ColumnTypeExprParam    // FixedString(N)
    ;
columnDefinitionExpr: identifier columnTypeExpr;
columnExprList: columnsExpr (COMMA columnsExpr)*;
columnExprWhen : WHEN columnExpr THEN columnExpr;
columnsExpr
    : (tableIdentifier DOT)? ASTERISK  # ColumnsExprAsterisk
    | LPAREN selectUnionStmt RPAREN    # ColumnsExprSubquery
    // NOTE: asterisk and subquery goes before |columnExpr| so that we can mark them as multi-column expressions.
    | columnExpr                       # ColumnsExprColumn
    ;
caseExpr
    : CASE case_expr=columnExpr? columnExprWhen+ (ELSE else_expr=columnExpr)? END
    ;
columnExpr
    : caseExpr                                                                            # ColumnExprCase
    | CAST LPAREN columnExpr AS columnTypeExpr RPAREN                                     # ColumnExprCast
    | DATE STRING_LITERAL                                                                 # ColumnExprDate
    | EXTRACT LPAREN interval FROM columnExpr RPAREN                                      # ColumnExprExtract
    | INTERVAL columnExpr interval                                                        # ColumnExprInterval
    | SUBSTRING LPAREN columnExpr FROM columnExpr (FOR columnExpr)? RPAREN                # ColumnExprSubstring
    | TIMESTAMP STRING_LITERAL                                                            # ColumnExprTimestamp
    | TRIM LPAREN (BOTH | LEADING | TRAILING) STRING_LITERAL FROM columnExpr RPAREN       # ColumnExprTrim
    | SUM LPAREN caseExpr RPAREN                                                          # ColumnExprSumCaseFunction
    | function=aggregateFunctionName LPAREN DISTINCT? ALL? columnArgList? RPAREN          # ColumnExprAggFunction
    | (IF|IIF) LPAREN cond=columnExpr COMMA trueExpr=columnExpr COMMA falseExpr=columnExpr RPAREN   # ColumnExprIfExpr
    | MULTIIF LPAREN columnArgList RPAREN                                                 # ColumnExprMultiIfExpr
    | (POW|POWER) LPAREN columnExpr COMMA (numberLiteral|NULL_SQL) RPAREN                 # ColumnExprPowFunction
    | identifier (LPAREN columnExprList? RPAREN)? LPAREN DISTINCT? columnArgList? RPAREN  # ColumnExprFunction
    | columnExpr LBRACE STRING_LITERAL RBRACE                                             # ColumnQuoteExpr
    | literal                                                                             # ColumnExprLiteral

    // FIXME(ilezhankin): this part looks very ugly, maybe there is another way to express it
    | columnExpr LBRACKET columnExpr RBRACKET                                             # ColumnExprArrayAccess
    | columnExpr DOT DECIMAL_LITERAL                                                      # ColumnExprTupleAccess
    | DASH columnExpr                                                                     # ColumnExprNegate
    | columnExpr ( ASTERISK                                                               // multiply
                 | SLASH                                                                  // divide
                 | PERCENT                                                                // modulo
                 ) columnExpr                                                             # ColumnExprPrecedence1
    | columnExpr ( PLUS                                                                   // plus
                 | DASH                                                                   // minus
                 | CONCAT                                                                 // concat
                 ) columnExpr                                                             # ColumnExprPrecedence2
    | columnExpr ( EQ_DOUBLE                                                              // equals
                 | EQ_SINGLE                                                              // equals
                 | NOT_EQ                                                                 // notEquals
                 | LE                                                                     // lessOrEquals
                 | GE                                                                     // greaterOrEquals
                 | LT                                                                     // less
                 | GT                                                                     // greater
                 | GLOBAL? NOT? IN                                                        // in, notIn, globalIn, globalNotIn
                 | NOT? (LIKE | ILIKE)                                                    // like, notLike, ilike, notILike
                 ) columnExpr                                                             # ColumnExprPrecedence3
    | columnExpr IS NOT? NULL_SQL                                                         # ColumnExprIsNull
    | NOT columnExpr                                                                      # ColumnExprNot
    | columnExpr AND columnExpr                                                           # ColumnExprAnd
    | columnExpr OR columnExpr                                                            # ColumnExprOr
    // TODO(ilezhankin): `BETWEEN a AND b AND c` is parsed in a wrong way: `BETWEEN (a AND b) AND c`
    | columnExpr NOT? BETWEEN columnExpr AND columnExpr                                   # ColumnExprBetween
    | <assoc=right> columnExpr QUERY columnExpr COLON columnExpr                          # ColumnExprTernaryOp
    | columnExpr (alias | AS identifier)                                                  # ColumnExprAlias
    | identifier AS LPAREN selectUnionStmt RPAREN                                         # ColumnExprAliasSubquery
    | (tableIdentifier DOT)? ASTERISK                                                     # ColumnExprAsterisk  // single-column only
    | LPAREN selectUnionStmt RPAREN                                                       # ColumnExprSubquery  // single-column only
    | LPAREN columnExpr RPAREN                                                            # ColumnExprParens    // single-column only
    | LPAREN columnExprList RPAREN                                                        # ColumnExprTuple
    | LBRACKET columnExprList? RBRACKET                                                   # ColumnExprArray
    | columnIdentifier                                                                    # ColumnExprIdentifier
    | columnExpr DOUBLECOLON columnTypeExpr                                               # ColumnTypeDefinition
    ;
columnArgList: columnArgExpr (COMMA columnArgExpr)*;
columnArgExpr: columnLambdaExpr | columnExpr;
columnLambdaExpr:
    ( LPAREN identifier (COMMA identifier)* RPAREN
    |        identifier (COMMA identifier)*
    )
    ARROW columnExpr
    ;
columnIdentifier: (tableIdentifier DOT)? nestedIdentifier;
nestedIdentifier: identifier (DOT identifier)?;

// Tables

tableExpr
    : tableIdentifier                    # TableExprIdentifier
    | tableFunctionExpr                  # TableExprFunction
    | LPAREN selectUnionStmt RPAREN      # TableExprSubquery
    | tableExpr (alias | AS identifier)  # TableExprAlias
    | fushionMerge                       # TableFushionMerge
    ;
fushionMerge
    : FUSIONMERGE LPAREN db=databaseIdentifier COMMA table1=tableIdentifier COMMA table2=tableIdentifier COMMA splitcolumn=columnExpr COMMA splitinfo=columnExpr COMMA frange=columnExpr COMMA srange=columnExpr RPAREN (alias | AS identifier)?
    ;
tableFunctionExpr: identifier LPAREN tableArgList? RPAREN;
tableIdentifier: (databaseIdentifier DOT)? identifier;
tableArgList: tableArgExpr (COMMA tableArgExpr)*;
tableArgExpr
    : tableIdentifier
    | tableFunctionExpr
    | literal
    ;

// Databases

databaseIdentifier: identifier;

// Basics

floatingLiteral
    : FLOATING_LITERAL
    | DOT (DECIMAL_LITERAL | OCTAL_LITERAL)
    | DECIMAL_LITERAL DOT (DECIMAL_LITERAL | OCTAL_LITERAL)?  // can't move this to the lexer or it will break nested tuple access: t.1.2
    ;
numberLiteral: (PLUS | DASH)? (floatingLiteral | OCTAL_LITERAL | DECIMAL_LITERAL | HEXADECIMAL_LITERAL | INF | NAN_SQL);
literal
    : numberLiteral     #numliteral
    | STRING_LITERAL    #stringliteral
    | NULL_SQL          #nullliteral
    ;
interval: SECOND | MINUTE | HOUR | DAY | WEEK | MONTH | QUARTER | YEAR;
aggregateFunctionName : COUNT | SUM | AVG | VAR | VARPOP | VARIANCE | STD | STDDEV | STDDEVPOP | MIN | MAX | PERCENTILE_DISC | PERCENTILE_CONT;
decimalTypeName : 'Decimal' | 'Decimal32' | 'Decimal64' | 'Decimal128' | 'Decimal256';
tupleOrArrayName : TUPLE | ARRAY;
keyword
    // except NULL_SQL, INF, NAN_SQL
    : AFTER | ALIAS | ALL | ALTER | AND | ANTI | ANY | ARRAY | AS | ASCENDING | ASOF | ASYNC | ATTACH | BETWEEN | BOTH | BY | CASE | CAST
    | CHECK | CLEAR | CLUSTER | CODEC | COLLATE | COLUMN | COMMENT | CONSTRAINT | CREATE | CROSS | CUBE | DATABASE | DATABASES | DATE
    | DEDUPLICATE | DEFAULT | DELAY | DELETE | DESCRIBE | DESC | DESCENDING | DETACH | DICTIONARIES | DICTIONARY | DISK | DISTINCT
    | DISTRIBUTED | DROP | ELSE | END | ENGINE | EVENTS | EXISTS | EXPLAIN | EXPRESSION | EXTRACT | FETCHES | FINAL | FIRST | FLUSH | FOR
    | FORMAT | FREEZE | FROM | FULL | FUNCTION | GLOBAL | GRANULARITY | GROUP | HAVING | HIERARCHICAL | ID | IF | ILIKE | IN | INDEX
    | INJECTIVE | INNER | INSERT | INTERVAL | INTO | IS | IS_OBJECT_ID | JOIN | JSON_FALSE | JSON_TRUE | KEY | KILL | LAST | LAYOUT
    | LEADING | LEFT | LIFETIME | LIKE | LIMIT | LIVE | LOCAL | LOGS | MATERIALIZED | MAX | MERGES | MIN | MODIFY | MOVE | MUTATION | NO
    | NOT | NULLS | OFFSET | ON | OPTIMIZE | OR | ORDER | OUTER | OUTFILE | PARTITION | POPULATE | PREWHERE | PRIMARY | RANGE | RELOAD
    | REMOVE | RENAME | REPLACE | REPLICA | REPLICATED | RIGHT | ROLLUP | SAMPLE | SELECT | SEMI | SENDS | SET | SETTINGS | SHOW | SOURCE
    | START | STOP | SUBSTRING | SYNC | SYNTAX | SYSTEM | TABLE | TABLES | TEMPORARY | TEST | THEN | TIES | TIMEOUT | TIMESTAMP | TOTALS
    | TRAILING | TRIM | TRUNCATE | TO | TOP | TTL | TYPE | UNION | UPDATE | USE | USING | UUID | VALUES | VIEW | VOLUME | WATCH | WHEN
    | WHERE | WITH
    ;
keywordForAlias
    : DATE | FIRST | ID | KEY
    ;
alias: IDENTIFIER | keywordForAlias;  // |interval| can't be an alias, otherwise 'INTERVAL 1 SOMETHING' becomes ambiguous.
identifier: IDENTIFIER | interval | keyword;
identifierOrNull: identifier | NULL_SQL;  // NULL_SQL can be only 'Null' here.
enumValue: STRING_LITERAL EQ_SINGLE numberLiteral;

ADD: A D D;
AFTER: A F T E R;
ALIAS: A L I A S;
ALL: A L L;
ALTER: A L T E R;
AND: A N D;
ANTI: A N T I;
ANY: A N Y;
ARRAY: A R R A Y;
AS: A S;
ASCENDING: A S C | A S C E N D I N G;
ASOF: A S O F;
ASYNC: A S Y N C;
ATTACH: A T T A C H;
AVG: A V G;
BETWEEN: B E T W E E N;
BOTH: B O T H;
BY: B Y;
CASE: C A S E;
CAST: C A S T;
CHECK: C H E C K;
CLEAR: C L E A R;
CLUSTER: C L U S T E R;
CODEC: C O D E C;
COLLATE: C O L L A T E;
COLUMN: C O L U M N;
COMMENT: C O M M E N T;
CONSTRAINT: C O N S T R A I N T;
COUNT: C O U N T;
CREATE: C R E A T E;
CROSS: C R O S S;
CUBE: C U B E;
DATABASE: D A T A B A S E;
DATABASES: D A T A B A S E S;
DATE: D A T E;
DAY: D A Y;
DEDUPLICATE: D E D U P L I C A T E;
DEFAULT: D E F A U L T;
DELAY: D E L A Y;
DELETE: D E L E T E;
DESC: D E S C;
DESCENDING: D E S C E N D I N G;
DESCRIBE: D E S C R I B E;
DETACH: D E T A C H;
DICTIONARIES: D I C T I O N A R I E S;
DICTIONARY: D I C T I O N A R Y;
DISK: D I S K;
DISTINCT: D I S T I N C T;
DISTRIBUTED: D I S T R I B U T E D;
DROP: D R O P;
ELSE: E L S E;
END: E N D;
ENGINE: E N G I N E;
EVENTS: E V E N T S;
EXISTS: E X I S T S;
EXPLAIN: E X P L A I N;
EXPRESSION: E X P R E S S I O N;
EXTRACT: E X T R A C T;
FETCHES: F E T C H E S;
FINAL: F I N A L;
FIRST: F I R S T;
FLUSH: F L U S H;
FOR: F O R;
FORMAT: F O R M A T;
FREEZE: F R E E Z E;
FROM: F R O M;
FULL: F U L L;
FUNCTION: F U N C T I O N;
FUSIONMERGE : F U S I O N M E R G E;
GLOBAL: G L O B A L;
GRANULARITY: G R A N U L A R I T Y;
GROUP: G R O U P;
HAVING: H A V I N G;
HIERARCHICAL: H I E R A R C H I C A L;
HOUR: H O U R;
ID: I D;
IF: I F;
IIF: I I F;
ILIKE: I L I K E;
IN: I N;
INDEX: I N D E X;
INF: I N F | I N F I N I T Y;
INJECTIVE: I N J E C T I V E;
INNER: I N N E R;
INSERT: I N S E R T;
INTERVAL: I N T E R V A L;
INTO: I N T O;
IS: I S;
IS_OBJECT_ID: I S UNDERSCORE O B J E C T UNDERSCORE I D;
JOIN: J O I N;
KEY: K E Y;
KILL: K I L L;
LAST: L A S T;
LAYOUT: L A Y O U T;
LEADING: L E A D I N G;
LEFT: L E F T;
LIFETIME: L I F E T I M E;
LIKE: L I K E;
LIMIT: L I M I T;
LIVE: L I V E;
LOCAL: L O C A L;
LOGS: L O G S;
MATERIALIZED: M A T E R I A L I Z E D;
MAX: M A X;
MERGES: M E R G E S;
MIN: M I N;
MINUTE: M I N U T E;
MODIFY: M O D I F Y;
MONTH: M O N T H;
MOVE: M O V E;
MUTATION: M U T A T I O N;
MULTIIF : M U L T I I F;
NAN_SQL: N A N; // conflicts with macro NAN
NO: N O;
NOT: N O T;
NULL_SQL: N U L L; // conflicts with macro NULL
NULLS: N U L L S;
OFFSET: O F F S E T;
ON: O N;
OPTIMIZE: O P T I M I Z E;
OR: O R;
ORDER: O R D E R;
OUTER: O U T E R;
OUTFILE: O U T F I L E;
PARTITION: P A R T I T I O N;
PERCENTILE_CONT: P E R C E N T I L E '_' C O N T;
PERCENTILE_DISC: P E R C E N T I L E '_' D I S C;
POPULATE: P O P U L A T E;
POW: P O W;
POWER: P O W E R;
PREWHERE: P R E W H E R E;
PRIMARY: P R I M A R Y;
QUARTER: Q U A R T E R;
RANGE: R A N G E;
RELOAD: R E L O A D;
REMOVE: R E M O V E;
RENAME: R E N A M E;
REPLACE: R E P L A C E;
REPLICA: R E P L I C A;
REPLICATED: R E P L I C A T E D;
RIGHT: R I G H T;
ROLLUP: R O L L U P;
SAMPLE: S A M P L E;
SECOND: S E C O N D;
SELECT: S E L E C T;
SEMI: S E M I;
SENDS: S E N D S;
SET: S E T;
SETTINGS: S E T T I N G S;
SHOW: S H O W;
SOURCE: S O U R C E;
START: S T A R T;
STD: S T D;
STDDEV: S T D D E V;
STDDEVPOP: S T D D E V P O P;
STOP: S T O P;
SUBSTRING: S U B S T R I N G;
SUM: S U M;
SYNC: S Y N C;
SYNTAX: S Y N T A X;
SYSTEM: S Y S T E M;
TABLE: T A B L E;
TABLES: T A B L E S;
TEALIMIT : T E A L I M I T;
TEMPORARY: T E M P O R A R Y;
TEST: T E S T;
THEN: T H E N;
TIES: T I E S;
TIMEOUT: T I M E O U T;
TIMESTAMP: T I M E S T A M P;
TO: T O;
TOP: T O P;
TOTALS: T O T A L S;
TRAILING: T R A I L I N G;
TRIM: T R I M;
TRUNCATE: T R U N C A T E;
TTL: T T L;
TUPLE : T U P L E;
TYPE: T Y P E;
UNION: U N I O N;
UPDATE: U P D A T E;
USE: U S E;
USING: U S I N G;
UUID: U U I D;
VALUES: V A L U E S;
VIEW: V I E W;
VOLUME: V O L U M E;
WATCH: W A T C H;
WEEK: W E E K;
VAR: V A R;
VARPOP: V A R P O P;
VARIANCE: V A R I A N C E;
WHEN: W H E N;
WHERE: W H E R E;
WITH: W I T H;
YEAR: Y E A R | Y Y Y Y;

JSON_FALSE: 'false';
JSON_TRUE: 'true';

// Tokens

IDENTIFIER
    : (LETTER | UNDERSCORE) (LETTER | UNDERSCORE | DEC_DIGIT)*
    | BACKQUOTE ( ~([\\`]) | (BACKSLASH .) | (BACKQUOTE BACKQUOTE) )* BACKQUOTE
    | QUOTE_DOUBLE ( ~([\\"]) | (BACKSLASH .) | (QUOTE_DOUBLE QUOTE_DOUBLE) )* QUOTE_DOUBLE
    ;
FLOATING_LITERAL
    : HEXADECIMAL_LITERAL DOT HEX_DIGIT* (P | E) (PLUS | DASH)? DEC_DIGIT+
    | HEXADECIMAL_LITERAL (P | E) (PLUS | DASH)? DEC_DIGIT+
    | DECIMAL_LITERAL DOT DEC_DIGIT* E (PLUS | DASH)? DEC_DIGIT+
    | DOT DECIMAL_LITERAL E (PLUS | DASH)? DEC_DIGIT+
    | DECIMAL_LITERAL E (PLUS | DASH)? DEC_DIGIT+
    ;
OCTAL_LITERAL: '0' OCT_DIGIT+;
DECIMAL_LITERAL: DEC_DIGIT+;
HEXADECIMAL_LITERAL: '0' X HEX_DIGIT+;

// It's important that quote-symbol is a single character.
STRING_LITERAL: QUOTE_SINGLE ( ~([\\']) | (BACKSLASH .) | (QUOTE_SINGLE QUOTE_SINGLE) )* QUOTE_SINGLE;

// Alphabet and allowed symbols

fragment A: [aA];
fragment B: [bB];
fragment C: [cC];
fragment D: [dD];
fragment E: [eE];
fragment F: [fF];
fragment G: [gG];
fragment H: [hH];
fragment I: [iI];
fragment J: [jJ];
fragment K: [kK];
fragment L: [lL];
fragment M: [mM];
fragment N: [nN];
fragment O: [oO];
fragment P: [pP];
fragment Q: [qQ];
fragment R: [rR];
fragment S: [sS];
fragment T: [tT];
fragment U: [uU];
fragment V: [vV];
fragment W: [wW];
fragment X: [xX];
fragment Y: [yY];
fragment Z: [zZ];

fragment LETTER: [a-zA-Z];
fragment OCT_DIGIT: [0-7];
fragment DEC_DIGIT: [0-9];
fragment HEX_DIGIT: [0-9a-fA-F];

ARROW: '->';
ASTERISK: '*';
BACKQUOTE: '`';
BACKSLASH: '\\';
COLON: ':';
DOUBLECOLON: '::';
COMMA: ',';
CONCAT: '||';
DASH: '-';
DOT: '.';
EQ_DOUBLE: '==';
EQ_SINGLE: '=';
GE: '>=';
GT: '>';
LBRACE: '{';
LBRACKET: '[';
LE: '<=';
LPAREN: '(';
LT: '<';
NOT_EQ: '!=' | '<>';
PERCENT: '%';
PLUS: '+';
QUERY: '?';
QUOTE_DOUBLE: '"';
QUOTE_SINGLE: '\'';
RBRACE: '}';
RBRACKET: ']';
RPAREN: ')';
SEMICOLON: ';';
SLASH: '/';
UNDERSCORE: '_';

// Comments and whitespace

MULTI_LINE_COMMENT: '/*' .*? '*/' -> skip;
SINGLE_LINE_COMMENT: '--' ~('\n'|'\r')* ('\n' | '\r' | EOF) -> skip;
WHITESPACE: [ \u000B\u000C\t\r\n] -> skip;  // '\n' can be part of multiline single query