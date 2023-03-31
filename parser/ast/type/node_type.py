from enum import Enum


class NodeType(Enum):
    # base statement, 1-9
    Union_SQLSTATEMENT = 1
    Common_SQLSTATEMENT = 2
    Clickhouse_SQLSTATEMENT = 3
    Byte_Clickhouse_SQLSTATEMENT = 4
    Hive_SQLSTATEMENT = 5
    # block statement, 10-49
    BLOCKSTATEMENT = 10
    Select_BLOCKSTATEMENT = 11
    From_BLOCKSTATEMENT = 12
    Where_BLOCKSTATEMENT = 13
    GroupBy_BLOCKSTATEMENT = 14
    Having_BLOCKSTATEMENT = 15
    OrderBy_BLOCKSTATEMENT = 16
    LimitBy_BLOCKSTATEMENT = 17
    Limit_BLOCKSTATEMENT = 18
    TeaLimit_BLOCKSTATEMENT = 19
    With_BLOCKSTATEMENT = 20
    PreWhere_BLOCKSTATEMENT = 21
    Settings_BLOCKSTATEMENT = 22
    Sample_BLOCKSTATEMENT = 23
    ArrayJoin_BLOCKSTATEMENT = 24
    ClusterBy_BLOCKSTATEMENT = 25
    DistributeBy_BLOCKSTATEMENT = 26
    SortBy_BLOCKSTATEMENT = 27
    # base expr, 50-99
    EXPR = 50
    Literal_EXPR = 51
    Identifier_EXPR = 52
    Number_EXPR = 53
    Column_EXPR = 54
    AllColumns_EXPR = 55
    ArrayAccess_EXPR = 56
    TupleAccess_EXPR = 57
    Arrays_EXPR = 58
    Tuples_EXPR = 59
    MapExpression_EXPR = 60
    Table_EXPR = 61
    TableFunction_EXPR = 62
    Maps_EXPR = 63
    # complex expression, 100-119
    NameExpression_EXPR = 100
    NestedExpression_EXPR = 101
    Interval_EXPR = 102
    LambdaExpression_EXPR = 103
    CastExpr_EXPR = 104
    RatioExpr_EXPR = 105
    TopExpr_EXPR = 106
    LimitExpr_EXPR = 107
    JoinConstraintExpr_EXPR = 108
    OrderExpr_EXPR = 109
    EnumExpr_EXPR = 110
    DateExpr_EXPR = 111
    TokenDefinitionExpr_EXPR = 112
    SelectItem_EXPR = 113
    SampleExpr_EXPR = 114
    ValueTypeDefinitionExpr_EXPR = 115
    FormatExpr_EXPR = 116
    Hive_BinaryExpr_EXPR = 117
    # agg function, 120-149
    SqlAggFunction_EXPR = 120
    SqlCountFunction_EXPR = 121
    SqlMinFunction_EXPR = 122
    SqlMaxFunction_EXPR = 123
    SqlSumFunction_EXPR = 124
    SqlAvgFunction_EXPR = 125
    SqlVarPopFunction_EXPR = 126
    SqlVarSampFunction_EXPR = 127
    SqlStdPopFunction_EXPR = 128
    SqlStdSampFunction_EXPR = 129
    # arithmetic, 150-179
    ArithmeticExpression_EXPR = 150
    NegateExpression_EXPR = 151
    MultiplyExpression_EXPR = 152
    DivideExpression_EXPR = 153
    ModuloExpression_EXPR = 154
    AdditionExpression_EXPR = 155
    SubtractionExpression_EXPR = 156
    DivExpression_EXPR = 157
    # cond expression, 180-199
    CondExpression_EXPR = 180
    IfExpression_EXPR = 181
    IIFFunction_EXPR = 182
    MultiIfExpression_EXPR = 183
    CaseExpression_EXPR = 184
    WhenExpression_EXPR = 185
    TernaryExpression_EXPR = 186
    Hive_NVLExpression_EXPR = 187
    CoalesceFunction_EXPR = 188
    Hive_NullIfFunction_EXPR = 189
    Hive_AssertTrueFunction_EXPR = 190
    # common and special func, 200-499
    Function_EXPR = 200
    CommonFunction_EXPR = 201
    ExtractFunction_EXPR = 202
    MathFunction_EXPR = 203
    BareFunction_EXPR = 204
    RoundFunction_EXPR = 205
    PowerFunction_EXPR = 206
    QuantilesFunction_EXPR = 207
    Quantiles2Function_EXPR = 208
    Quantiles3Function_EXPR = 209
    ClickHouseCommonFunction_EXPR = 210
    TrimFunction_EXPR = 211
    ColumnsFunction_EXPR = 212
    ToTypeNameFunction_EXPR = 213
    # logical bool, 500-549
    BooleanCompare_EXPR = 500
    BinaryEqual_EXPR = 501
    LogicalEqual_EXPR = 502
    LogicalNot_EXPR = 503
    LogicalAnd_EXPR = 504
    LogicalOr_EXPR = 505
    LogicalConcat_EXPR = 506
    LogicalIsNull_EXPR = 507
    LogicalCompare_EXPR = 508
    LogicalIn_EXPR = 509
    LogicalLike_EXPR = 510
    LogicalBetween_EXPR = 511
    LogicalIsTrue_EXPR = 512
    LogicalExistsQuery_EXPR = 513
    # table source, 550-570
    SqlSource = 550
    SqlTableSource = 551
    SqlTableJoinSource = 552
    SqlUnionSource = 553
    SqlSubquerySource = 554
    SqlArrayJoinSource = 555
    SqlFusionMergeSource = 556

    # Other
    Seq = 900
    # error type, 1000->max
    LARGE_ERROR_NODE_TYPE = 1000


class SQLSetQuantifier(Enum):
    DISTINCT = 2001
    ALL = 2002
    UNIQUE = 2003
    DISTINCTROW = 2004


class OrderingType(Enum):
    Unspecified = 2101
    ASC = 2102
    DESC = 2103
    NULL_FIRST = 2104
    NULL_LAST = 2105


class JoinKind(Enum):
    # Leave only rows that was JOINed.
    Inner = 2201
    # If in "right" table there is no corresponding rows, use default values instead.
    Left = 2202
    Right = 2203
    Full = 2204
    # Direct product. Strictness and condition doesn't matter.
    Cross = 2205
    # Same as direct product. Intended to be converted to INNER JOIN with conditions from WHERE.
    Comma = 2206


class JoinLocality(Enum):
    Unspecified = 2251
    # Perform JOIN, using only data available on same servers (co-located data).
    Local = 2252
    # Collect and merge data from remote servers, and broadcast it to each server.
    Global = 2253


class JoinStrictness(Enum):
    Unspecified = 2261
    RightAny = 2262
    Any = 2263
    All = 2264
    Asof = 2265
    Semi = 2266
    Anti = 2267


class JoinType:
    def __init__(self):
        self.locality = None
        self.strictness = None
        self.kind = None

    def __str__(self):
        if self.locality == JoinLocality.Local:
            local_info = "LOCAL"
        elif self.locality == JoinLocality.Global:
            local_info = "GLOBAL"
        else:
            local_info = ""

        if self.strictness == JoinStrictness.Semi:
            strictness_info = "SEMI"
        elif self.strictness == JoinStrictness.All:
            strictness_info = "ALL"
        elif self.strictness == JoinStrictness.Anti:
            strictness_info = "ANTI"
        elif self.strictness == JoinStrictness.Any:
            strictness_info = "ANY"
        elif self.strictness == JoinStrictness.Asof:
            strictness_info = "ASOF"
        else:
            strictness_info = ""

        if self.kind == JoinKind.Left:
            kind_info = "LEFT"
        elif self.kind == JoinKind.Right:
            kind_info = "RIGHT"
        elif self.kind == JoinKind.Inner:
            kind_info = "INNER"
        elif self.kind == JoinKind.Full:
            kind_info = "FULL"
        else:
            kind_info = "CROSS"

        return local_info + " " + strictness_info + " " + kind_info + " JOIN "


class ExprAliasType(Enum):
    Unspecified = 2401
    alias = 2402
    AS = 2403


#
# # todo, 待补充完毕
# class JoinType(Enum):
#
#     # COMMA(",")
#     COMMA = 2201
#     # JOIN("JOIN")
#     JOIN = 2202
#     # INNER_JOIN("INNER JOIN")
#     INNER_JOIN = 2203
#     # CROSS_JOIN("CROSS JOIN")
#     CROSS_JOIN = 2204
#     # NATURAL_JOIN("NATURAL JOIN")
#     NATURAL_JOIN = 2205
#     # NATURAL_CROSS_JOIN("NATURAL CROSS JOIN")
#     NATURAL_CROSS_JOIN = 2206
#     # NATURAL_LEFT_JOIN("NATURAL LEFT JOIN")
#     NATURAL_LEFT_JOIN = 2207
#     # NATURAL_RIGHT_JOIN("NATURAL RIGHT JOIN")
#     NATURAL_RIGHT_JOIN = 2208
#     # NATURAL_INNER_JOIN("NATURAL INNER JOIN")
#     NATURAL_INNER_JOIN = 2209
#     # LEFT_OUTER_JOIN("LEFT JOIN")
#     LEFT_OUTER_JOIN = 2210
#     # LEFT_SEMI_JOIN("LEFT SEMI JOIN")
#     LEFT_SEMI_JOIN = 2211
#     # LEFT_ANTI_JOIN("LEFT ANTI JOIN")
#     LEFT_ANTI_JOIN = 2212
#     # RIGHT_OUTER_JOIN("RIGHT JOIN")
#     RIGHT_OUTER_JOIN = 2213
#     # FULL_OUTER_JOIN("FULL JOIN")
#     FULL_OUTER_JOIN = 2214
#     # STRAIGHT_JOIN("STRAIGHT_JOIN")
#     STRAIGHT_JOIN = 2215
#     # OUTER_APPLY("OUTER APPLY")
#     OUTER_APPLY = 2216
#     # CROSS_APPLY("CROSS APPLY")
#     CROSS_APPLY = 2217


# todo, 需要考虑不同类型的类型值会有等值问题
class UnionType(Enum):
    UNION = 2501
    UNION_ALL = 2502
    MINUS = 2503
    MINUS_DISTINCT = 2504
    MINUS_ALL = 2505
    EXCEPT = 2506
    EXCEPT_ALL = 2507
    EXCEPT_DISTINCT = 2508
    INTERSECT = 2509
    INTERSECT_ALL = 2510
    INTERSECT_DISTINCT = 2511
    # "UNION DISTINCT"
    UNION_DISTINCT = 2512


class OperatorType(Enum):
    EQ_DOUBLE = 2601
    EQ_SINGLE = 2602
    # !=
    NOT_EQ_1 = 2603
    # <>
    NOT_EQ_2 = 2604
    LE = 2605
    GE = 2606
    LT = 2607
    GT = 2608
    HIVE_EQ_NS = 2609


class LogicalInType(Enum):
    IN = 2701
    NOT_IN = 2702
    GLOBAL_IN = 2703
    GLOBAL_NOT_IN = 2704


class LogicalLikeType(Enum):
    LIKE = 2711
    NOT_LIKE = 2712
    ILIKE = 2713
    NOT_ILIKE = 2714


class AggSumType(Enum):
    Unspecified = 2721
    CASE_EXPR = 2722


class LiteralType(Enum):
    NUM_LITERAL = 2731
    STRING_LITERAL = 2732
    NULL_LITERAL = 2733


class DialectType(Enum):
    CLICKHOUSE = 2741
    MYSQL = 2742
    ORACLE = 2743
    HIVE = 2744
    SPARK = 2745


class GroupByType(Enum):
    Unspecified = 2801
    FRONT_CUBE = 2802
    FRONT_ROLLUP = 2803
    TAIL_CUBE = 2804
    TAIL_ROLLUP = 2805
    TAIL_TOTALS = 2806


class LimitSplitType(Enum):
    COMMA = 2821
    OFFSET = 2822


class JoinConstraintType(Enum):
    ON = 2831
    USING = 2832


class TimeIntervalType(Enum):
    SECOND = 2851
    MINUTE = 2852
    HOUR = 2853
    DAY = 2854
    WEEK = 2855
    MONTH = 2856
    QUARTER = 2857
    YEAR = 2858
    Unspecified = 2859


class TrimType(Enum):
    BOTH = 2871
    LEADING = 2872
    TRAILING = 2873


class ArrayJoinType(Enum):
    LEFT_ARRAY_JOIN = 2881
    INNER_ARRAY_JOIN = 2882
    ARRAY_JOIN = 2883
