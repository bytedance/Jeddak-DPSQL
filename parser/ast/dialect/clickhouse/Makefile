PYTHON := python3

# ANTLR := java -Xmx500M -cp "/usr/local/lib/antlr-4.9-complete.jar:.:/usr/local/lib/antlr-4.9-complete.jar" org.antlr.v4.Tool
# GRUN := java -Xmx500M -cp "/usr/local/lib/antlr-4.9-complete.jar:.:/usr/local/lib/antlr-4.9-complete.jar" org.antlr.v4.gui.TestRig
ANTLR := java -Xmx500M -cp "/usr/local/lib/antlr-4.9.2-complete.jar:.:/usr/local/lib/antlr-4.9.2-complete.jar" org.antlr.v4.Tool
GRUN := java -Xmx500M -cp "/usr/local/lib/antlr-4.9.2-complete.jar:.:/usr/local/lib/antlr-4.9.2-complete.jar" org.antlr.v4.gui.TestRig

genpython: clickhouse_visitor.py

clickhouse_visitor.py: ClickHouse.g4
	$(ANTLR) -visitor -Dlanguage=Python3 ClickHouse.g4

ClickHouseParser.java: ClickHouse.g4
	$(ANTLR) -visitor ClickHouse.g4


ClickHouseParser.class: ClickHouseParser.java
	javac *.java

gui: ClickHouseParser.class
	$(GRUN) ClickHouse query -tokens -gui -diagnostics  test.sql

clean:
	# rm ClickHouseSmallListener* || true
	# rm ClickHouseSmallVisitor* || true
	# rm ClickHouseSmallLexer* || true
	# rm ClickHouseSmallParser* || true
	# rm ClickHouseSmallBase* || true
	rm *.interp || true
	rm *.tokens || true
	rm *.class || true
	rm *.java || true