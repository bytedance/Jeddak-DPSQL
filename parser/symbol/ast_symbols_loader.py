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

from exception.enum.meradata_errors_enum import MetaDataErrors
from parser.symbol.symbol_loading_visitor import SymbolLoadingVisitor, InitSymbolLoadingVisitor, \
    SQSymbolLoadingVisitor
from parser.ast.visitor.tree_visitor import VisitorOrder
from exception.errors import MetaDataError


def load_ast_symbols(ast=None, metamatcher=None):
    try:
        initVisitor = InitSymbolLoadingVisitor()
        ast.accept(initVisitor, VisitorOrder.SYMBOLLOADING)
    except Exception as err:
        raise MetaDataError(MetaDataErrors.INIT_SYMBOL_ERROR.value, str(err))

    try:
        visitor = SymbolLoadingVisitor(metamatcher)
        ast.accept(visitor, VisitorOrder.SYMBOLLOADING)
    except Exception as err:
        raise MetaDataError(MetaDataErrors.VISIT_SYMBOL_ERROR.value, str(err))


def load_sq_symbols(sq):
    visitor = SQSymbolLoadingVisitor(sq)
    sq.select_block.accept(visitor)

    source_block = sq.sq_ast.source_block
    if source_block is not None:
        source_block.accept(visitor)
