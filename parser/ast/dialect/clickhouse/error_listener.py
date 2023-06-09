# This file may have been modified by Beijing Volcano Engine Technology Ltd. (“ Volcano Engine's Modifications”).
# All Volcano Engine's Modifications are Copyright (2023) Beijing Volcano Engine Technology Ltd.

import logging


class SyntaxErrorListener():
    def syntaxError(self, recognizer, offendingToken, line, column, msg, e):
        if offendingToken is None:
            logging.error(
                "dpaccess-internal-Lexer error at line {0} column {1}.  Message: {2}".format(line, column, msg))
            raise ValueError("Lexer error at line")
        elif recognizer.symbolicNames[offendingToken.type] == "UNSUPPORTED":
            logging.error(
                "dpaccess-internal-Reserved SQL keyword is unsupported in this parser: {0} at line {1} column {2}.  Message: {3}".format(
                    offendingToken.text, line, column, msg))
            raise ValueError("Reserved SQL keyword is unsupported in this parser")
        elif msg.find("reportAttemptingFullContext") >= 0 or msg.find("reportContextSensitivity") >= 0 or msg.find(
                "reportAmbiguity") >= 0:
            # TODO: fix these problem and raise error here
            logging.warning(
                "dpaccess-internal-Bad token {0} at line {1} column {2}.  Message: {3}".format(offendingToken.text,
                                                                                               line, column, msg))
        else:
            logging.error(
                "dpaccess-internal-Bad token {0} at line {1} column {2}.  Message: {3}".format(offendingToken.text,
                                                                                               line, column, msg))
            raise ValueError("clickhouse small error listener Bad token")

    def reportAmbiguity(self, recognizer, dfa, startIndex, stopIndex, exact, ambigAlts, configs):
        # use DiagnosticErrorListener() to get full diagnostics
        # use this stub to raise ValueError if needed for unit tests to throw specific ambiguity errors
        pass

    def reportAttemptingFullContext(self, recognizer, dfa, startIndex, stopIndex, conflictingAlts, configs):
        # use DiagnosticErrorListener() to get full diagnostics
        # use this stub to raise ValueError if needed for unit tests to throw specific ambiguity errors
        # raise ValueError("Attempting Full Context")
        pass

    def reportContextSensitivity(self, recognizer, dfa, startIndex, stopIndex, prediction, configs):
        # use DiagnosticErrorListener() to get full diagnostics
        # use this stub to raise ValueError if needed for unit tests to throw specific ambiguity errors
        # raise ValueError("Found Exact")
        pass
