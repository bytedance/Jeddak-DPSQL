# Copyright (2023) Beijing Volcano Engine Technology Ltd.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Exception usage example：
QueryInterfaceError("5002", "Current version can not process add noise")
the first parameter is code(error code number)，the second parameter is the specific exception message
The code range of each module is specified as follows:
-----------------------------------------------------
Parser
- Number：0001-1000
-----------------------------------------------------
MetaData
- Number：1001-2000
-----------------------------------------------------
Rewriter
- Number：2001-3000
-----------------------------------------------------
Dbaccess
- Number：3001-4000
-----------------------------------------------------
PrivacyAccountant
- Number：4001-5000
-----------------------------------------------------
QueryInterface
- Number：5001-6000
-----------------------------------------------------
JwtVerify
- Number：6001-7000
-----------------------------------------------------
AnalysisError
- Number：8001-9000
-----------------------------------------------------
HttpServiceError
- Number：9001-10000
-----------------------------------------------------
UtilsError
- Number：10001-11000
"""


class Error(Exception):
    def __init__(self, status, message):
        super().__init__(message, status)
        self.message = message
        self.status = status


class ParserError(Error):
    def __init__(self, status, message):
        Error.__init__(self, 'P' + str(status), message)


class MetaDataError(Error):
    def __init__(self, status, message):
        Error.__init__(self, 'M' + str(status), message)


class RewriterError(Error):
    def __init__(self, status, message):
        Error.__init__(self, 'R' + str(status), message)


class DbaccessError(Error):
    def __init__(self, status, message):
        Error.__init__(self, 'D' + str(status), message)


class PrivacyAccountantError(Error):
    def __init__(self, status, message):
        Error.__init__(self, 'B' + str(status), message)


class QueryInterfaceError(Error):
    def __init__(self, status, message):
        Error.__init__(self, 'Q' + str(status), message)


class AnalysisError(Error):
    def __init__(self, status, message):
        Error.__init__(self, 'A' + str(status), message)


class JwtVerify(Error):
    def __init__(self, status, message):
        Error.__init__(self, 'J' + str(status), message)


class HttpServiceError(Error):
    def __init__(self, status, message):
        Error.__init__(self, 'H' + str(status), message)


class UtilsError(Error):
    def __init__(self, status, message):
        Error.__init__(self, 'U' + str(status), message)
