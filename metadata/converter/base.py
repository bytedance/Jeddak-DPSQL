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

class BaseTypeConverter():
    ENGINE = "BaseTypeConverter"

    def dbtype_to_type(self, dbtype):
        raise NotImplementedError("%s dbtype_to_type not implemented" % (self.ENGINE))

    def function_dbtype(self, funcname):
        raise NotImplementedError("%s function_dbtype not implemented" % (self.ENGINE))

    def function_type(self, funcname):
        raise NotImplementedError("%s function_type not implemented" % (self.ENGINE))

    def litral_dbtype(self, tp, value):
        raise NotImplementedError("%s litral_dbtype not implemented" % (self.ENGINE))

    def op_dbtype(self, op, ltn, rtn):
        raise NotImplementedError("%s op_dbtype not implemented" % (self.ENGINE))
