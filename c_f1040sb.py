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

def compute_f1040sb(e):
	# 1040 Schedule B - Part I Interest
	e.di('v_f1040sb_2')
	e.di('v_f1040sb_3')
	@e.ded
	def v_f1040sb_4(g):
		return g('v_f1040sb_2') - g('v_f1040sb_3'), True

	# 1040 Schedule B - Part II Ordinary Dividends
	e.di('v_f1040sb_6')

