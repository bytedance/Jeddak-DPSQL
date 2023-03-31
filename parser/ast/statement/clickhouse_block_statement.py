from parser.ast.statement.block_statement import SqlBlockStatement


# https://clickhouse.tech/docs/zh/sql-reference/statements/select/with/
# WITH <expression> AS <identifier>
# WITH <identifier> AS <subquery expression>


# # WITH <expression> AS <identifier>
# class WithFromExpressionBlockStatement(WithBlockStatement):
#     def __init__(self):
#         super(WithFromExpressionBlockStatement, self).__init__()
#         self.expr_list = Seq(self)
#
#     def __str__(self):
#         return "WITH " + ", ".join(str(c) for c in self.expr_list)
#
#
# # WITH <identifier> AS <subquery expression>
# class WithAsQueryBlockStatement(WithBlockStatement):
#     def __init__(self):
#         super(WithAsQueryBlockStatement, self).__init__()
#         self.identifier = None
#         self.sub_query = None


# https://clickhouse.tech/docs/zh/sql-reference/statements/select/prewhere/
# clickhouse 独有
class PrewhereBlockStatement(SqlBlockStatement):
    def __init__(self):
        super(PrewhereBlockStatement, self).__init__()


class SettingBlockStatement(SqlBlockStatement):
    def __init__(self):
        super(SettingBlockStatement, self).__init__()


# https://clickhouse.tech/docs/en/sql-reference/statements/select/sample/
class SampleBlockStatement(SqlBlockStatement):
    def __init__(self):
        super(SampleBlockStatement, self).__init__()


# https://clickhouse.com/docs/zh/sql-reference/statements/select/format/
class FormatBlockStatement(SqlBlockStatement):
    def __init__(self):
        super(FormatBlockStatement, self).__init__()
        self.format_expr = None
