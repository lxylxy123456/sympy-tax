#	sympy-tax - Using sympy to compute tax as an equation
#	Copyright (C) 2024  lxylxy123456
#
#	This program is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.
#
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with this program.  If not, see <https://www.gnu.org/licenses/>.

from sympy import Max, Min, Piecewise

from c_f1040sb import compute_f1040sb
from c_f1040sd import compute_f1040sd

def tax_computation_worksheet(g, ti):
	v = Piecewise(
		(ti * g('c_f1040_16_ws_b1') - g('c_f1040_16_ws_d1'),
		 (ti >= g('c_f1040_16_ws_t1')) & (ti < g('c_f1040_16_ws_t2'))),
		(ti * g('c_f1040_16_ws_b2') - g('c_f1040_16_ws_d2'),
		 (ti >= g('c_f1040_16_ws_t2')) & (ti < g('c_f1040_16_ws_t3'))),
		(ti * g('c_f1040_16_ws_b3') - g('c_f1040_16_ws_d3'),
		 (ti >= g('c_f1040_16_ws_t3')) & (ti < g('c_f1040_16_ws_t4'))),
		(ti * g('c_f1040_16_ws_b4') - g('c_f1040_16_ws_d4'),
		 (ti >= g('c_f1040_16_ws_t4')) & (ti < g('c_f1040_16_ws_t5'))),
		(ti * g('c_f1040_16_ws_b5') - g('c_f1040_16_ws_d5'),
		 (ti >= g('c_f1040_16_ws_t5'))),
		(0, True))
	c = ti >= g('c_f1040_16_ws_t1')
	return v, c

def compute_f1040_qdcgtw(e):
	# Qualified Dividends and Capital Gain Tax Worksheet - Line 16
	@e.ded
	def v_f1040_16_qdcgtw_1(g):
		return g('v_f1040_15'), True
	@e.ded
	def v_f1040_16_qdcgtw_2(g):
		return g('v_f1040_3a'), True
	# Are you filing Schedule D?
	e.di('v_f1040_16_qdcgtw_3_file_d')
	@e.ded2
	def v_f1040_16_qdcgtw_3(ge):
		_d15v, _d15c = ge('v_f1040sd_15')
		_d16v, _d16c = ge('v_f1040sd_16')
		_7v, _7c = ge('v_f1040_7')
		_qv, _qc= ge('v_f1040_16_qdcgtw_3_file_d')
		_v = Piecewise(
			(Min(_d15v, _d16v), _qv >= 1),
			(_7v, _qv <= 0),
			(0, True))
		_c = _qc & (((_qv >= 1) & _d15c & _d16c) | ((_qv <= 0) & _7c))
		return _v, _c
	@e.ded
	def v_f1040_16_qdcgtw_4(g):
		return g('v_f1040_16_qdcgtw_2') + g('v_f1040_16_qdcgtw_3'), True
	@e.ded
	def v_f1040_16_qdcgtw_5(g):
		return Max(g('v_f1040_16_qdcgtw_1') - g('v_f1040_16_qdcgtw_4'), 0), True
	@e.ded
	def v_f1040_16_qdcgtw_6(g):
		return g('c_f1040_16_qdcgtw_6'), True
	@e.ded
	def v_f1040_16_qdcgtw_7(g):
		return Min(g('v_f1040_16_qdcgtw_1'), g('v_f1040_16_qdcgtw_6')), True
	@e.ded
	def v_f1040_16_qdcgtw_8(g):
		return Min(g('v_f1040_16_qdcgtw_5'), g('v_f1040_16_qdcgtw_7')), True
	@e.ded
	def v_f1040_16_qdcgtw_9(g):
		return g('v_f1040_16_qdcgtw_7') - g('v_f1040_16_qdcgtw_8'), True
	@e.ded
	def v_f1040_16_qdcgtw_10(g):
		return Min(g('v_f1040_16_qdcgtw_1'), g('v_f1040_16_qdcgtw_4')), True
	@e.ded
	def v_f1040_16_qdcgtw_11(g):
		return g('v_f1040_16_qdcgtw_9'), True
	@e.ded
	def v_f1040_16_qdcgtw_12(g):
		return g('v_f1040_16_qdcgtw_10') - g('v_f1040_16_qdcgtw_11'), True
	@e.ded
	def v_f1040_16_qdcgtw_13(g):
		return g('c_f1040_16_qdcgtw_13'), True
	@e.ded
	def v_f1040_16_qdcgtw_14(g):
		return Min(g('v_f1040_16_qdcgtw_1'), g('v_f1040_16_qdcgtw_13')), True
	@e.ded
	def v_f1040_16_qdcgtw_15(g):
		return g('v_f1040_16_qdcgtw_5') + g('v_f1040_16_qdcgtw_9'), True
	@e.ded
	def v_f1040_16_qdcgtw_16(g):
		return g('v_f1040_16_qdcgtw_14') - g('v_f1040_16_qdcgtw_15'), True
	@e.ded
	def v_f1040_16_qdcgtw_17(g):
		return Min(g('v_f1040_16_qdcgtw_12'), g('v_f1040_16_qdcgtw_16')), True
	@e.ded
	def v_f1040_16_qdcgtw_18(g):
		return g('v_f1040_16_qdcgtw_17') * g('c_f1040_16_qdcgtw_18_perc'), True
	@e.ded
	def v_f1040_16_qdcgtw_19(g):
		return g('v_f1040_16_qdcgtw_9') + g('v_f1040_16_qdcgtw_17'), True
	@e.ded
	def v_f1040_16_qdcgtw_20(g):
		return g('v_f1040_16_qdcgtw_10') - g('v_f1040_16_qdcgtw_19'), True
	@e.ded
	def v_f1040_16_qdcgtw_21(g):
		return g('v_f1040_16_qdcgtw_20') * g('c_f1040_16_qdcgtw_21_perc'), True
	@e.ded
	def v_f1040_16_qdcgtw_22(g):
		return tax_computation_worksheet(g, g('v_f1040_16_qdcgtw_5'))
	@e.ded
	def v_f1040_16_qdcgtw_23(g):
		return (g('v_f1040_16_qdcgtw_18') + g('v_f1040_16_qdcgtw_21') +
				g('v_f1040_16_qdcgtw_22')), True
	@e.ded
	def v_f1040_16_qdcgtw_24(g):
		return tax_computation_worksheet(g, g('v_f1040_16_qdcgtw_1'))
	@e.ded
	def v_f1040_16_qdcgtw_25(g):
		return Min(g('v_f1040_16_qdcgtw_23'), g('v_f1040_16_qdcgtw_24')), True

def compute_f1040(e):
	# 1040 - Income
	e.di('v_f1040_1a')
	e.di('v_f1040_1b')
	e.di('v_f1040_1c')
	e.di('v_f1040_1d')
	e.di('v_f1040_1e')
	e.di('v_f1040_1f')
	e.di('v_f1040_1g')
	e.di('v_f1040_1h')
	e.di('v_f1040_1i')
	@e.ded
	def v_f1040_1z(g):
		return sum([
			g('v_f1040_1a'),
			g('v_f1040_1b'),
			g('v_f1040_1c'),
			g('v_f1040_1d'),
			g('v_f1040_1e'),
			g('v_f1040_1f'),
			g('v_f1040_1g'),
			g('v_f1040_1h'),
			g('v_f1040_1i'),
		]), True
	compute_f1040sb(e)
	e.di('v_f1040_2a')
	@e.ded
	def v_f1040_2b(g):
		return g('v_f1040sb_4'), True
	e.di('v_f1040_3a')
	@e.ded
	def v_f1040_3b(g):
		return g('v_f1040sb_6'), True
	e.di('v_f1040_4a')
	e.di('v_f1040_4b')
	e.di('v_f1040_5a')
	e.di('v_f1040_5b')
	e.di('v_f1040_6a')
	e.di('v_f1040_6b')
	compute_f1040sd(e)
	@e.ded2
	def v_f1040_7(gc):
		_16v, _16c = gc('v_f1040sd_16')
		_21v, _21c = gc('v_f1040sd_21')
		v = Piecewise(
			(_16v, _16c & (_16v >= 0)),
			(_21v, _21c),
			(0, True))
		c = (_16c & (_16v >= 0)) | _21c
		return v, c
	e.di('v_f1040_8')
	@e.ded
	def v_f1040_9(g):
		return sum([
			g('v_f1040_1z'),
			g('v_f1040_2b'),
			g('v_f1040_3b'),
			g('v_f1040_4b'),
			g('v_f1040_5b'),
			g('v_f1040_6b'),
			g('v_f1040_7'),
			g('v_f1040_8'),
		]), True
	e.di('v_f1040_10')
	@e.ded
	def v_f1040_11(g):
		return g('v_f1040_9') - g('v_f1040_10'), True
	@e.ded
	def v_f1040_12(g):
		return g('c_f1040_12_sd'), True
	e.di('v_f1040_13')
	@e.ded
	def v_f1040_14(g):
		return g('v_f1040_12') - g('v_f1040_13'), True
	@e.ded
	def v_f1040_15(g):
		return Max(g('v_f1040_11') - g('v_f1040_14'), 0), True

	# 1040 - Tax and Credits
	compute_f1040_qdcgtw(e)
	@e.ded
	def v_f1040_16(g):
		# Using Qualified Dividends and Capital Gain Tax Worksheet.
		# To not use this, uncomment the following line.
		#return tax_computation_worksheet(g, g('v_f1040_15'))
		return g('v_f1040_16_qdcgtw_25'), True
	e.di('v_f1040_17')
	@e.ded
	def v_f1040_18(g):
		return g('v_f1040_16') + g('v_f1040_17'), True
	e.di('v_f1040_19')
	e.di('v_f1040_20')
	@e.ded
	def v_f1040_21(g):
		return g('v_f1040_19') + g('v_f1040_20'), True
	@e.ded
	def v_f1040_24(g):
		return Max(g('v_f1040_18') - g('v_f1040_21'), 0), True

	# 1040 - Payments
	e.di('v_f1040_25a')
	e.di('v_f1040_25b')
	e.di('v_f1040_25c')
	@e.ded
	def v_f1040_25d(g):
		return g('v_f1040_25a') + g('v_f1040_25b') + g('v_f1040_25c'), True
	e.di('v_f1040_26')
	e.di('v_f1040_27')
	e.di('v_f1040_28')
	e.di('v_f1040_29')
	e.di('v_f1040_31')
	@e.ded
	def v_f1040_32(g):
		return sum([
			g('v_f1040_27'),
			g('v_f1040_28'),
			g('v_f1040_29'),
			g('v_f1040_31'),
		]), True
	@e.ded
	def v_f1040_33(g):
		return g('v_f1040_25d') + g('v_f1040_26') + g('v_f1040_32'), True

	# 1040 - Refund
	@e.ded
	def v_f1040_34(g):
		_24 = g('v_f1040_24')
		_33 = g('v_f1040_33')
		return _33 - _24, _33 > _24

	# 1040 - Amount You Owe
	@e.ded
	def v_f1040_37(g):
		_24 = g('v_f1040_24')
		_33 = g('v_f1040_33')
		return _24 - _33, _33 < _24

