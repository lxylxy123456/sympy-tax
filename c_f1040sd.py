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

from sympy import Max, Piecewise

def compute_f1040sd(e):
	# 1040 Schedule D - Part I Short-Term
	e.di('v_f1040sd_1a_d')
	e.di('v_f1040sd_1a_e')
	@e.ded
	def v_f1040sd_1a_h(g):
		v = g('v_f1040sd_1a_d') - g('v_f1040sd_1a_e')
		return v, True
	e.di('v_f1040sd_1b_d')
	e.di('v_f1040sd_1b_e')
	e.di('v_f1040sd_1b_g')
	@e.ded
	def v_f1040sd_1b_h(g):
		v = g('v_f1040sd_1b_d') - g('v_f1040sd_1b_e') + g('v_f1040sd_1b_g')
		return v, True
	e.di('v_f1040sd_2_d')
	e.di('v_f1040sd_2_e')
	e.di('v_f1040sd_2_g')
	@e.ded
	def v_f1040sd_2_h(g):
		v = g('v_f1040sd_2_d') - g('v_f1040sd_2_e') + g('v_f1040sd_2_g')
		return v, True
	e.di('v_f1040sd_3_d')
	e.di('v_f1040sd_3_e')
	e.di('v_f1040sd_3_g')
	@e.ded
	def v_f1040sd_3_h(g):
		v = g('v_f1040sd_3_d') - g('v_f1040sd_3_e') + g('v_f1040sd_3_g')
		return v, True
	e.di('v_f1040sd_4')
	e.di('v_f1040sd_5')
	e.di('v_f1040sd_6')
	@e.ded
	def v_f1040sd_7(g):
		return sum([
			g('v_f1040sd_1a_h'),
			g('v_f1040sd_1b_h'),
			g('v_f1040sd_2_h'),
			g('v_f1040sd_3_h'),
			g('v_f1040sd_4'),
			g('v_f1040sd_5'),
			-g('v_f1040sd_6'),
		]), True

	# 1040 Schedule D - Part II Long-Term
	e.di('v_f1040sd_8a_d')
	e.di('v_f1040sd_8a_e')
	@e.ded
	def v_f1040sd_8a_h(g):
		v = g('v_f1040sd_8a_d') - g('v_f1040sd_8a_e')
		return v, True
	e.di('v_f1040sd_8b_d')
	e.di('v_f1040sd_8b_e')
	e.di('v_f1040sd_8b_g')
	@e.ded
	def v_f1040sd_8b_h(g):
		v = g('v_f1040sd_8b_d') - g('v_f1040sd_8b_e') + g('v_f1040sd_8b_g')
		return v, True
	e.di('v_f1040sd_9_d')
	e.di('v_f1040sd_9_e')
	e.di('v_f1040sd_9_g')
	@e.ded
	def v_f1040sd_9_h(g):
		v = g('v_f1040sd_9_d') - g('v_f1040sd_9_e') + g('v_f1040sd_9_g')
		return v, True
	e.di('v_f1040sd_10_d')
	e.di('v_f1040sd_10_e')
	e.di('v_f1040sd_10_g')
	@e.ded
	def v_f1040sd_10_h(g):
		v = g('v_f1040sd_10_d') - g('v_f1040sd_10_e') + g('v_f1040sd_10_g')
		return v, True
	e.di('v_f1040sd_11')
	e.di('v_f1040sd_12')
	e.di('v_f1040sd_13')
	e.di('v_f1040sd_14')
	@e.ded
	def v_f1040sd_15(g):
		return sum([
			g('v_f1040sd_8a_h'),
			g('v_f1040sd_8b_h'),
			g('v_f1040sd_9_h'),
			g('v_f1040sd_10_h'),
			g('v_f1040sd_11'),
			g('v_f1040sd_12'),
			g('v_f1040sd_13'),
			-g('v_f1040sd_14'),
		]), True

	# 1040 Schedule D - Part III Summary
	@e.ded
	def v_f1040sd_16(g):
		return g('v_f1040sd_7') + g('v_f1040sd_15'), True
	@e.ded
	def v_f1040sd_17(g):
		v = Piecewise(
			(1, (g('v_f1040sd_15') > 0) & (g('v_f1040sd_16') > 0)),
			(0, True))
		c = g('v_f1040sd_16') > 0
		return v, c
	# TODO: Not implemented
	e.di('v_f1040sd_18')
	# TODO: Not implemented
	e.di('v_f1040sd_19')
	# Whether filing Form 4952.
	e.di('v_f1040sd_20_file_4952')
	@e.ded
	def v_f1040sd_20(g):
		_18 = g('v_f1040sd_18')
		_19 = g('v_f1040sd_19')
		_4952 = g('v_f1040sd_20_file_4952')
		v = Piecewise(
			(1,
			 (_18 <= 0) & (_18 >= 0) & (_19 <= 0) & (_19 >= 0) & (_4952 <= 0)),
			(0, True))
		c = g('v_f1040sd_17') >= 1
		return v, c
	@e.ded
	def v_f1040sd_21(g):
		_16 = g('v_f1040sd_16')
		return Max(g('c_f1040sd_21_lmt'), _16), _16 < 0
	@e.ded2
	def v_f1040sd_22(gc):
		_3v, _3c = gc('v_f1040_3a')
		_16v, _16c = gc('v_f1040sd_16')
		_17v, _17c = gc('v_f1040sd_17')
		v = Piecewise((1, _3v > 0), (0, True))
		c = _3c & _16c & ((_16v <= 0) | (_17c & (_17v <= 0)))
		return v, c

