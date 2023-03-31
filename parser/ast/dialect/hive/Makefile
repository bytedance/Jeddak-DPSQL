PYTHON := python3

# ANTLR := java -Xmx500M -cp "/usr/local/lib/antlr-4.9-complete.jar:.:/usr/local/lib/antlr-4.9-complete.jar" org.antlr.v4.Tool
# GRUN := java -Xmx500M -cp "/usr/local/lib/antlr-4.9-complete.jar:.:/usr/local/lib/antlr-4.9-complete.jar" org.antlr.v4.gui.TestRig
ANTLR := java -Xmx500M -cp "/usr/local/lib/antlr-4.9.2-complete.jar:.:/usr/local/lib/antlr-4.9.2-complete.jar" org.antlr.v4.Tool
GRUN := java -Xmx500M -cp "/usr/local/lib/antlr-4.9.2-complete.jar:.:/usr/local/lib/antlr-4.9.2-complete.jar" org.antlr.v4.gui.TestRig

genpython: hive_visitor.py

hive_visitor.py: Hive.g4
	$(ANTLR) -visitor -Dlanguage=Python3 Hive.g4

HiveParser.java: Hive.g4
	$(ANTLR) -visitor Hive.g4


HiveParser.class: HiveParser.java
	javac *.java

gui: HiveParser.class
	$(GRUN) Hive query -tokens -gui -diagnostics  test.sql

clean:
	rm *.interp || true
	rm *.tokens || true
	rm *.class || true
	rm *.java || true