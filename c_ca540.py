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

from sympy import Max, Piecewise, Xor

from c_ca540ca import compute_ca540ca

def compute_ca540(e):
	# CA 540 - Exemptions
	e.di('v_ca540_6')
	@e.ded
	def v_ca540_7_n(g):
		v = Piecewise(
			(1, (g('c_ca540_1') >= 1) | (g('c_ca540_3') >= 1) |
				(g('c_ca540_4') >= 1)),
			(2, (g('c_ca540_2') >= 1) | (g('c_ca540_5') >= 1)))
		return v, g('v_ca540_6') <= 0
	@e.ded
	def v_ca540_7(g):
		return g('v_ca540_7_n') * g('c_ca540_7_mul'), True
	e.di('v_ca540_8_n')
	@e.ded
	def v_ca540_8(g):
		return g('v_ca540_8_n') * g('c_ca540_8_mul'), True
	e.di('v_ca540_9_n')
	@e.ded
	def v_ca540_9(g):
		return g('v_ca540_9_n') * g('c_ca540_9_mul'), True
	e.di('v_ca540_10_n')
	@e.ded
	def v_ca540_10(g):
		return g('v_ca540_10_n') * g('c_ca540_10_mul'), True
	@e.ded
	def v_ca540_11(g):
		return sum([
			g('v_ca540_7'),
			g('v_ca540_8'),
			g('v_ca540_9'),
			g('v_ca540_10'),
		]), True

	# CA 540 - Taxable Income
	e.di('v_ca540_12')
	@e.ded
	def v_ca540_13(g):
		return g('v_f1040_11'), True
	compute_ca540ca(e)
	@e.ded
	def v_ca540_14(g):
		return g('v_ca540ca_I_C_27_B'), True
	@e.ded
	def v_ca540_15(g):
		return g('v_ca540_13') - g('v_ca540_14'), True
	@e.ded
	def v_ca540_16(g):
		return g('v_ca540ca_I_C_27_C'), True
	@e.ded
	def v_ca540_17(g):
		return g('v_ca540_15') + g('v_ca540_16'), True
	@e.ded
	def v_ca540_18(g):
		return Max(g('v_ca540ca_II_30'), g('c_ca540_18_sd')), True
	@e.ded
	def v_ca540_19(g):
		return Max(g('v_ca540_17') - g('v_ca540_18'), 0), True

	# CA 540 - Tax
	@e.ded
	def v_ca540_31(g):
		_ti = g('v_ca540_19')
		# Note: this is only implementing the Tax Rate Schedule.
		args = []
		for i in range(1, 10):
			_t = g('c_ca540_31_trs_t%d' % i)
			_a = g('c_ca540_31_trs_a%d' % i)
			_b = g('c_ca540_31_trs_b%d' % i)
			_v = (_ti - _t) * _a + _b
			_c = _ti >= _t
			if i != 9:
				_c &= _ti < g('c_ca540_31_trs_t%d' % (i + 1))
			args.append((_v, _c))
		v = Piecewise(*args, (0, True))
		c = _ti >= g('c_ca540_31_trs_t1')
		return v, c
	@e.ded
	def v_ca540_32(g):
		# AGI Limitation Worksheet not implemented.
		return g('v_ca540_11'), g('v_ca540_13') <= g('c_ca540_32_fed_agi')
	@e.ded
	def v_ca540_33(g):
		return Max(g('v_ca540_31') - g('v_ca540_32'), 0), True
	e.di('v_ca540_34')
	@e.ded
	def v_ca540_35(g):
		return g('v_ca540_33') - g('v_ca540_34'), True

	# CA 540 - Special Credits
	e.di('v_ca540_40')
	e.di('v_ca540_43')
	e.di('v_ca540_44')
	e.di('v_ca540_45')
	e.di('v_ca540_46')
	@e.ded
	def v_ca540_47(g):
		return sum([
			g('v_ca540_40'),
			g('v_ca540_43'),
			g('v_ca540_44'),
			g('v_ca540_45'),
			g('v_ca540_46'),
		]), True
	@e.ded
	def v_ca540_48(g):
		return Max(g('v_ca540_35') - g('v_ca540_47'), 0), True

	# CA 540 - Other Taxes
	e.di('v_ca540_61')
	e.di('v_ca540_62')
	e.di('v_ca540_63')
	@e.ded
	def v_ca540_64(g):
		return sum([
			g('v_ca540_48'),
			g('v_ca540_61'),
			g('v_ca540_62'),
			g('v_ca540_63'),
		]), True
	# CA 540 - Payments
	e.di('v_ca540_71')
	e.di('v_ca540_72')
	e.di('v_ca540_73')
	e.di('v_ca540_75')
	e.di('v_ca540_76')
	e.di('v_ca540_77')
	@e.ded
	def v_ca540_78(g):
		return sum([
			g('v_ca540_71'),
			g('v_ca540_72'),
			g('v_ca540_73'),
			g('v_ca540_75'),
			g('v_ca540_76'),
			g('v_ca540_77'),
		]), True

	# CA 540 - Use Tax
	e.di('v_ca540_91')

	# CA 540 - ISR Penalty
	e.di('v_ca540_92')

	# CA 540 - Overpaid Tax/Tax Due
	@e.ded
	def v_ca540_93(g):
		_78 = g('v_ca540_78')
		_91 = g('v_ca540_91')
		return _78 - _91, _78 > _91
	@e.ded
	def v_ca540_94(g):
		_78 = g('v_ca540_78')
		_91 = g('v_ca540_91')
		return _91 - _78, _91 > _78
	@e.ded
	def v_ca540_95(g):
		_92 = g('v_ca540_92')
		_93 = g('v_ca540_93')
		return _93 - _92, _93 > _92
	@e.ded
	def v_ca540_96(g):
		_92 = g('v_ca540_92')
		_93 = g('v_ca540_93')
		return _92 - _93, _92 > _93
	@e.ded
	def v_ca540_97(g):
		_95 = g('v_ca540_95')
		_64 = g('v_ca540_64')
		return _95 - _64, _95 > _64
	e.di('v_ca540_98')
	@e.ded
	def v_ca540_99(g):
		return g('v_ca540_97') - g('v_ca540_98'), True
	@e.ded
	def v_ca540_100(g):
		_95 = g('v_ca540_95')
		_64 = g('v_ca540_64')
		return _64 - _95, _95 < _64

	# CA 540 - Contributions
	e.di('v_ca540_110')

	# CA 540 - Amount You Owe
	@e.ded2
	def v_ca540_111(gc):
		_94v, _94c = gc('v_ca540_94')
		_96v, _96c = gc('v_ca540_96')
		_99v, _99c = gc('v_ca540_99')
		_100v, _100c = gc('v_ca540_100')
		_110v, _110c = gc('v_ca540_110')
		_v = _94v + _96v + _100v + _110v
		_c = _99c & (_99v <= 0) & _94c & _96c & _100c & _110c
		return _v, _c

	# CA 540 - Interest and Penalties
	e.di('v_ca540_112')
	e.di('v_ca540_113')
	@e.ded2
	def v_ca540_114(gc):
		_99v, _99c = gc('v_ca540_99')
		_110v, _110c = gc('v_ca540_110')
		_111v, _111c = gc('v_ca540_111')
		_112v, _112c = gc('v_ca540_112')
		_113v, _113c = gc('v_ca540_113')
		# a: Is there an amount on line 111? -> Yes
		_av = _111v + _112v + _113v
		_ac = _111c & (_111v > 0) & _112c & _113c
		# b: Is there an amount on line 111? -> No; Line 15 -> Yes, More than 99
		_1v = _110v + _112v + _113v
		_1c = _110c & _112c & _113c
		_bv = _1v - _99v
		_bc = (_1v > _99v) & _99c & _1c
		# Combine case a and b above (Note: this Piecewise seems to be slow).
		_v = Piecewise((_av, _ac), (_bv, _bc), (0, True))
		_c = Xor(_ac, _bc)
		return _v, _c

	# CA 540 - Refund and Direct Deposit
	@e.ded
	def v_ca540_115(g):
		_9 = g('v_ca540_99')
		_1 = g('v_ca540_110') + g('v_ca540_112') + g('v_ca540_113')
		return _9 - _1, _9 > _1

