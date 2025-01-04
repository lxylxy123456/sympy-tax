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

import argparse

import yaml, sympy
from sympy import Eq, Max, Piecewise, nan, symbols
from sympy.logic.boolalg import BooleanTrue, BooleanFalse

def get_consts(file_name, f_filing_status):
	f_fs = {
		's': 's', 'single': 's',
		'j': 'j', 'mfj': 'j', 'married filing jointly': 'j',
		'h': 'h', 'hoh': 'h', 'head of household': 'h',
		'p': 'p', 'mfs': 'p', 'married filing separately': 'p',
		'q': 'q', 'qss': 'q', 'qualifying surviving spouse': 'q',
	}[f_filing_status.lower().replace('_', ' ').replace('-', ' ')]
	assert f_fs in ['s', 'j', 'h', 'p', 'q']
	data = yaml.load(open(file_name), yaml.Loader)
	for k, v in data['global'].items():
		yield k, v
	for k, v in data['f_filing_status'].items():
		vv = list(filter(lambda x: f_fs in x[0], v.items()))
		assert len(vv) == 1
		yield k, next(iter(vv))[1]

# Naming convention:
#	c_*: constant
#	v_*: symbols (equations, inputs)
class Equation:
	def __init__(self):
		# Dict as {'name': (value, condition)}.
		self.symbols = {}
		# List of constant names.
		self.consts = []
		# List of equation names.
		self.equations = []
		# Dict as {'name': default}.
		self.inputs = {}

	def _set_symbol(self, name, value, condition):
		assert isinstance(value, sympy.core.basic.Basic)
		assert isinstance(condition, sympy.core.basic.Basic)
		self.symbols[name] = (value, condition)

	def define_input(self, name, default=0, condition=BooleanTrue()):
		assert name not in self.inputs
		self.inputs[name] = default
		self._set_symbol(name, symbols(name), condition)
	def di(self, *args, **kwargs):
		return self.define_input(*args, **kwargs)

	def define_const(self, name, value):
		assert name not in self.symbols
		self._set_symbol(name, sympy.core.numbers.Number(value), BooleanTrue())
		self.consts.append(name)
	def dc(self, *args, **kwargs):
		return self.define_const(*args, **kwargs)

	def define_equation(self, name, value, condition):
		assert name not in self.symbols
		if not isinstance(value, sympy.core.basic.Basic):
			print('Warning: %s is const but is defined as equation' % name)
			value = sympy.core.numbers.Number(value)
		if not isinstance(condition, sympy.core.basic.Basic):
			condition = {True: BooleanTrue, False: BooleanFalse}[condition]()
		self._set_symbol(name, value, condition)
		self.equations.append(name)
	def de(self, *args, **kwargs):
		return self.define_equation(*args, **kwargs)

	def define_equation_decorator(self, func):
		name = func.__code__.co_name
		condition = True
		def _get_symbol(name):
			nonlocal condition
			v, c = self.get_symbol(name)
			condition &= c
			return v
		value, c = func(_get_symbol)
		condition &= c
		self.define_equation(name, value, condition)
	def ded(self, *args, **kwargs):
		return self.define_equation_decorator(*args, **kwargs)

	def get_symbol(self, name):
		return self.symbols[name]
	def g(self, *args, **kwargs):
		return self.get_symbol(*args, **kwargs)

def compute_consts(e, file_name, f_filing_status):
	for k, v in get_consts(file_name, f_filing_status):
		e.dc(k, v)

def compute_1040(e):
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
	e.di('v_f1040_2a')
	e.di('v_f1040_2b')
	e.di('v_f1040_3a')
	e.di('v_f1040_3b')
	e.di('v_f1040_4a')
	e.di('v_f1040_4b')
	e.di('v_f1040_5a')
	e.di('v_f1040_5b')
	e.di('v_f1040_6a')
	e.di('v_f1040_6b')
	e.di('v_f1040_7')
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
	@e.ded
	def v_f1040_16(g):
		_ti = g('v_f1040_15')
		# Note: this is only implementing the 2024 Tax Computation Worksheet.
		v = Piecewise(
			(_ti * g('c_f1040_16_ws_b1') - g('c_f1040_16_ws_d1'),
			 (_ti >= g('c_f1040_16_ws_t1')) & (_ti < g('c_f1040_16_ws_t2'))),
			(_ti * g('c_f1040_16_ws_b2') - g('c_f1040_16_ws_d2'),
			 (_ti >= g('c_f1040_16_ws_t2')) & (_ti < g('c_f1040_16_ws_t3'))),
			(_ti * g('c_f1040_16_ws_b3') - g('c_f1040_16_ws_d3'),
			 (_ti >= g('c_f1040_16_ws_t3')) & (_ti < g('c_f1040_16_ws_t4'))),
			(_ti * g('c_f1040_16_ws_b4') - g('c_f1040_16_ws_d4'),
			 (_ti >= g('c_f1040_16_ws_t4')) & (_ti < g('c_f1040_16_ws_t5'))),
			(_ti * g('c_f1040_16_ws_b5') - g('c_f1040_16_ws_d5'),
			 (_ti >= g('c_f1040_16_ws_t5'))))
		c = _ti >= g('c_f1040_16_ws_t1')
		return v, c
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

def format_exp(e):
	s = repr(e)
	if len(s) > 60:
		s = s[:60] + '...'
	return s

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-f', '--filing-status', default='single')
	parser.add_argument('-c', '--consts-file', default='consts/2024.yml')
	parser.add_argument('-i', '--input-file', default='input.yml')
	parser.add_argument('--plot', action='store_true')
	args = parser.parse_args()

	args.consts_file
	e = Equation()
	compute_consts(e, args.consts_file, args.filing_status)
	compute_1040(e)
	inputs = e.inputs.copy()
	inputs.update(yaml.load(open(args.input_file), yaml.Loader))
	for i in e.equations:
		v, c = e.g(i)
		print(i, '=', format_exp(v))
		if c != True:
			print(' ' * len(i), '  if', format_exp(c))
		cs = c.subs(inputs.items())
		if cs == True:
			print(' ' * len(i), '=', v.subs(inputs.items()))
		elif cs == False:
			print(' ' * len(i), '=', 'undefined')
		else:
			raise RuntimeError('Cannot evaluate condition')
		print()

	if args.plot:
		# TODO: plotting does not implement condition check yet.
		from sympy import plot
		x = e.g('v_f1040_1a')[0]
		del inputs['v_f1040_1a']
		y = (e.g('v_f1040_16')[0] / e.g('v_f1040_15')[0]).subs(inputs.items())
		print(repr(y).replace('v_f1040_1a', 'x'))
		plot(y, (x, 0, 1000000))

if __name__ == '__main__':
	main()

