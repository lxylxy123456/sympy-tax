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

import argparse, functools

import yaml, sympy
from sympy import symbols
from sympy.logic.boolalg import BooleanTrue, BooleanFalse

from c_f1040 import compute_f1040
from c_ca540 import compute_ca540

def get_consts(file_name, f_filing_status, c_filing_status):
	fs_translate = lambda x: {
		's': 's', 'single': 's',
		'j': 'j', 'mfj': 'j', 'married filing jointly': 'j',
		'h': 'h', 'hoh': 'h', 'head of household': 'h',
		'p': 'p', 'mfs': 'p', 'married filing separately': 'p',
		'q': 'q', 'qss': 'q', 'qualifying surviving spouse': 'q',
	}[x.lower().replace('_', ' ').replace('-', ' ')]
	f_fs = fs_translate(f_filing_status)
	c_fs = fs_translate(c_filing_status)
	assert f_fs in ['s', 'j', 'h', 'p', 'q']
	data = yaml.load(open(file_name), yaml.Loader)
	for k, v in data['global'].items():
		yield k, v
	for k, v in data['f_filing_status'].items():
		vv = list(filter(lambda x: f_fs in x[0], v.items()))
		assert len(vv) == 1
		yield k, next(iter(vv))[1]
	for k, v in data['c_filing_status'].items():
		vv = list(filter(lambda x: c_fs in x[0], v.items()))
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
		# Dict as {symbol: default}.
		self.inputs = {}
		# Set as {'name'}, for inputs that need to be kept as variable.
		self.variable_inputs = set()
		# Dict as {'name': value}, for inputs that do not have default values.
		self.fixed_inputs = {}

	def set_variable_fixed_inputs(self, variable_inputs, fixed_inputs):
		self.variable_inputs = variable_inputs
		self.fixed_inputs = fixed_inputs

	def _set_symbol(self, name, value, condition):
		assert isinstance(value, sympy.core.basic.Basic)
		assert isinstance(condition, sympy.core.basic.Basic)
		assert name not in self.symbols
		self.symbols[name] = (value, condition)

	def define_input(self, name, default=0, condition=BooleanTrue()):
		assert name not in self.inputs
		assert name not in self.symbols
		if name not in self.variable_inputs:
			sn = sympy.core.numbers.Number(self.fixed_inputs.get(name, default))
		else:
			sn = symbols(name)
		self.inputs[sn] = default
		self._set_symbol(name, sn, condition)
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

	def define_equation_decorator2(self, func):
		name = func.__code__.co_name
		def _get_symbol_condition(name):
			nonlocal condition
			v, c = self.get_symbol(name)
			return v, c
		value, condition = func(_get_symbol_condition)
		self.define_equation(name, value, condition)
	def ded2(self, *args, **kwargs):
		return self.define_equation_decorator2(*args, **kwargs)

	def get_symbol(self, name):
		return self.symbols[name]
	def g(self, *args, **kwargs):
		return self.get_symbol(*args, **kwargs)

def compute_consts(e, file_name, f_filing_status, c_filing_status):
	for k, v in get_consts(file_name, f_filing_status, c_filing_status):
		e.dc(k, v)

@functools.cache
def get_inputs(input_file):
	inputs = {}
	for k, v in yaml.load(open(input_file), yaml.Loader).items():
		if type(v) == list:
			value = sum(v, start=sympy.core.numbers.Number(0))
		else:
			value = sympy.core.numbers.Number(v)
		inputs[k] = value
	return inputs

def format_exp(e):
	s = repr(e)
	if len(s) > 60:
		s = s[:60] + '...' + ' (%d)' % len(s)
	return s

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-f', '--filing-status', default='single')
	parser.add_argument('-c', '--consts-file', default='consts/2024.yml')
	parser.add_argument('-i', '--input-file', default='input.yml')
	parser.add_argument('-v', '--verbose', action='store_true')
	parser.add_argument('--plot', action='store_true')
	args = parser.parse_args()

	e = Equation()
	if 'fixed inputs':
		# e.g. {'v_f1040_1a'}
		e.set_variable_fixed_inputs(set(), get_inputs(args.input_file))
	compute_consts(e, args.consts_file, args.filing_status, args.filing_status)
	compute_f1040(e)
	compute_ca540(e)
	inputs = e.inputs.copy()
	for k, v in get_inputs(args.input_file).items():
		inputs[e.g(k)[0]] = v
	for i in e.equations:
		v, c = e.g(i)
		print(i, '=', end=' ')
		if args.verbose:
			print(format_exp(v))
			if c != True:
				print(' ' * len(i), '  if', format_exp(c))
			print(' ' * len(i), '=', end=' ')
		# Using xreplace because subs is slow.
		# https://github.com/sympy/sympy/issues/22240
		cs = c.xreplace(inputs)
		if cs == True:
			print(v.xreplace(inputs))
		elif cs == False:
			print('undefined')
		else:
			raise RuntimeError('Cannot evaluate condition')
		if args.verbose:
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

