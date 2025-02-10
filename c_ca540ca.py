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

from sympy import Max

def define_sum(e, name, fmt, vs):
	v = 0
	c = True
	for i in vs:
		_v, _c = e.g(fmt % i)
		v += _v
		c &= _c
	e.define_equation(name, v, c)

def compute_ca540ca(e):
	# CA 540CA - Part I - Section A - Line 1a-7 - Column A-C
	for i in ['1a', '1b', '1c', '1d', '1e', '1f', '1g', '1h', '1i', '1z', '2a',
			  '2b', '3a', '3b', '4a', '4b', '5a', '5b', '6a', '6b', '7']:
		# Column A
		if i not in ['1i']:
			e.define_equation('v_ca540ca_I_A_%s_A' % i, *e.g('v_f1040_%s' % i))
		# Column B
		if i not in ['1i']:
			if i == '1z':
				define_sum(e, 'v_ca540ca_I_A_%s_B' % i, 'v_ca540ca_I_A_%s_B',
						   ['1a', '1b', '1c', '1d', '1e', '1f', '1g', '1h'])
			else:
				e.di('v_ca540ca_I_A_%s_B' % i)
		# Column C
		if i not in ['6b']:
			if i == '1z':
				define_sum(e, 'v_ca540ca_I_A_%s_C' % i, 'v_ca540ca_I_A_%s_C',
						   ['1a', '1b', '1c', '1d', '1e', '1f', '1g', '1h',
							'1i'])
			else:
				e.di('v_ca540ca_I_A_%s_C' % i)

	# CA 540CA - Part I - Section B - Line 1-10 - Column A-C
	for i in ['1', '2a', '3', '4', '5', '6', '7', '9a', '9b1', '9b2', '9b3',
			  '10']:
		# Column A
		if i not in ['9b1', '9b2', '9b3']:
			if i == '10':
				define_sum(e, 'v_ca540ca_I_B_%s_A' % i, 'v_ca540ca_I_%s_A',
						   ['A_1z', 'A_2b', 'A_3b', 'A_4b', 'A_5b', 'A_6b',
							'A_7', 'B_1', 'B_2a', 'B_3', 'B_4', 'B_5', 'B_6',
							'B_7', 'B_9a'])
			else:
				# Schedule 1 not implemented yet, so define as input.
				e.di('v_ca540ca_I_B_%s_A' % i)
		# Column B
		if i not in ['2a']:
			if i == '10':
				define_sum(e, 'v_ca540ca_I_B_%s_B' % i, 'v_ca540ca_I_%s_B',
						   ['A_1z', 'A_2b', 'A_3b', 'A_4b', 'A_5b', 'A_6b',
							'A_7', 'B_1', 'B_3', 'B_4', 'B_5', 'B_6',
							'B_7', 'B_9a', 'B_9b1', 'B_9b2', 'B_9b3'])
			else:
				e.di('v_ca540ca_I_B_%s_B' % i)
		# Column C
		if i not in ['1', '7', '9b1', '9b2', '9b3']:
			if i == '10':
				define_sum(e, 'v_ca540ca_I_B_%s_C' % i, 'v_ca540ca_I_%s_C',
						   ['A_1z', 'A_2b', 'A_3b', 'A_4b', 'A_5b', 'A_7',
							'B_2a', 'B_3', 'B_4', 'B_5', 'B_6', 'B_9a'])
			else:
				e.di('v_ca540ca_I_B_%s_C' % i)

	# CA 540CA - Part I - Section C - Line 11-26 - Column A-C
	for i in ['11', '12', '13', '14', '15', '16', '17', '18', '19a', '20', '21',
			  '23', '25', '26']:
		# Column A
		if i not in []:
			if i == '26':
				define_sum(e, 'v_ca540ca_I_C_%s_A' % i, 'v_ca540ca_I_C_%s_A',
						   ['11', '12', '13', '14', '15', '16', '17', '18',
							'19a', '20', '21', '23', '25'])
			else:
				# Schedule 1 not implemented yet, so define as input.
				e.di('v_ca540ca_I_C_%s_A' % i)
		# Column B
		if i not in ['14', '16', '18', '19a', '21', '23']:
			if i == '26':
				define_sum(e, 'v_ca540ca_I_C_%s_B' % i, 'v_ca540ca_I_C_%s_B',
						   ['11', '12', '13', '15', '17', '20', '25'])
			else:
				# Schedule 1 not implemented yet, so define as input.
				e.di('v_ca540ca_I_C_%s_B' % i)
		# Column C
		if i not in ['11', '13', '15', '16', '17', '18', '23']:
			if i == '26':
				define_sum(e, 'v_ca540ca_I_C_%s_C' % i, 'v_ca540ca_I_C_%s_C',
						   ['12', '14', '19a', '20', '21', '25'])
			else:
				# Schedule 1 not implemented yet, so define as input.
				e.di('v_ca540ca_I_C_%s_C' % i)

	# CA 540CA - Part I - Section C - Line 27 - Column A-C
	@e.ded
	def v_ca540ca_I_C_27_A(g):
		return g('v_ca540ca_I_B_10_A') - g('v_ca540ca_I_C_26_A'), True
	@e.ded
	def v_ca540ca_I_C_27_B(g):
		return g('v_ca540ca_I_B_10_B') - g('v_ca540ca_I_C_26_B'), True
	@e.ded
	def v_ca540ca_I_C_27_C(g):
		return g('v_ca540ca_I_B_10_C') - g('v_ca540ca_I_C_26_C'), True

	# CA 540CA - Part II - Line 1-17 - Column A-C
	# Not implemented.

	# CA 540CA - Part II - Line 18
	e.di('v_ca540ca_II_18')

	# CA 540CA - Part II - Line 19-30
	e.di('v_ca540ca_II_19')
	e.di('v_ca540ca_II_20')
	e.di('v_ca540ca_II_21')
	@e.ded
	def v_ca540ca_II_22(g):
		return sum([
			g('v_ca540ca_II_19'),
			g('v_ca540ca_II_20'),
			g('v_ca540ca_II_21'),
		]), True
	@e.ded
	def v_ca540ca_II_23(g):
		return g('v_f1040_11'), True
	@e.ded
	def v_ca540ca_II_24(g):
		return Max(g('v_ca540ca_II_23') * 0.02, 0), True
	@e.ded
	def v_ca540ca_II_25(g):
		return Max(g('v_ca540ca_II_22') - g('v_ca540ca_II_24'), 0), True
	@e.ded
	def v_ca540ca_II_26(g):
		return g('v_ca540ca_II_18') + g('v_ca540ca_II_25'), True
	e.di('v_ca540ca_II_27')
	@e.ded
	def v_ca540ca_II_28(g):
		return g('v_ca540ca_II_26') + g('v_ca540ca_II_27'), True
	@e.ded
	def v_ca540ca_II_29(g):
		# Itemized Deductions Worksheet not implemented.
		return g('v_ca540ca_II_28'), g('v_ca540_13') <= g('c_ca540_32_fed_agi')
	@e.ded
	def v_ca540ca_II_30(g):
		return Max(g('v_ca540ca_II_29'), g('c_ca540_18_sd')), True

