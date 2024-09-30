/****************************************************************************
 * IConstraintStmtForeach.h
 *
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 *
 ****************************************************************************/
#pragma once
#include <stdint.h>
#include <unordered_map>
#include <memory>
#include <set>
#include <string>
#include <vector>
#include "zsp/ast/impl/UP.h"
#include "zsp/ast/IVisitor.h"
#include "zsp/ast/IConstraintScope.h"

namespace zsp {
namespace ast {

class IConstraintScope;
using IConstraintScopeUP=UP<IConstraintScope>;
typedef std::shared_ptr<IConstraintScope> IConstraintScopeSP;
class IConstraintStmtField;
using IConstraintStmtFieldUP=UP<IConstraintStmtField>;
typedef std::shared_ptr<IConstraintStmtField> IConstraintStmtFieldSP;
class IExpr;
using IExprUP=UP<IExpr>;
typedef std::shared_ptr<IExpr> IExprSP;
class IConstraintSymbolScope;
using IConstraintSymbolScopeUP=UP<IConstraintSymbolScope>;
typedef std::shared_ptr<IConstraintSymbolScope> IConstraintSymbolScopeSP;
class IConstraintStmtForeach;
using IConstraintStmtForeachUP=UP<IConstraintStmtForeach>;
class IConstraintStmtForeach : public virtual IConstraintScope {
public:
    
    virtual ~IConstraintStmtForeach() { }
    
    
    virtual IConstraintStmtField *getIt() = 0;
    
    virtual void setIt(IConstraintStmtField *v) = 0;
    
    virtual IConstraintStmtField *getIdx() = 0;
    
    virtual void setIdx(IConstraintStmtField *v) = 0;
    
    virtual IExpr *getExpr() const = 0;
    
    virtual void setExpr(IExpr *v, bool own=true) = 0;
    
    virtual IConstraintSymbolScope *getSymtab() const = 0;
    
    virtual void setSymtab(IConstraintSymbolScope *v, bool own=true) = 0;
};
    
    } // namespace zsp
    } // namespace ast
    
