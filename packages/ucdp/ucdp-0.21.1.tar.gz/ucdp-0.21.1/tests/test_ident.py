#
# MIT License
#
# Copyright (c) 2024 nbiotcloud
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
"""Identifier."""

import ucdp as u


def test_expridents():
    """Expression Identifier Resolve."""
    ident0 = u.Ident(u.UintType(8), "ident0")
    ident1 = u.Ident(u.UintType(8), "ident1")
    ident2 = u.Ident(u.UintType(8), "ident2")

    assert u.get_expridents(ident0 + -ident1) == (ident0, ident1)
    assert u.get_expridents(ident0 + 5) == (ident0,)
    assert u.get_expridents(ident0 + 5) == (ident0,)
    assert u.get_expridents(u.ConcatExpr((ident0, ident1))) == (ident0, ident1)
    assert u.get_expridents(u.Log2Expr(ident0)) == (ident0,)

    assert u.get_expridents(u.TernaryExpr(ident2 == 5, ident1, ident0)) == (ident2, ident1, ident0)


def test_idents():
    """Idents."""
    port = u.Port(u.ClkRstAnType(), "main_i")
    idents = u.Idents([port])
    assert idents["main_i"] is port
    assert idents["main_i"] == port
    assert "main_clk_i" in idents
    assert idents["main_clk_i"] == u.Port(u.ClkType(), "main_clk_i", direction=u.IN, doc=u.Doc(title="Clock"))
