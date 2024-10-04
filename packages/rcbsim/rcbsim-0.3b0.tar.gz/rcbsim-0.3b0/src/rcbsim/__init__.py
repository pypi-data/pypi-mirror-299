""" RC building simulator """
__version__ = '0.3b0'

__copyright__ = """This software was forked from the original RC_BuildingSimulator

which gives permission to anyone to use the software per the MIT ammended license below

All credit for the original software belongs to "Architecture and Buildings Systems ETH Zürich"
------------------


The MIT License (MIT) ammended

Copyright (c) 2016 Architecture and Building Systems

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Any use of this software in research requires a reference back to the department
of Architecture and Building Systems of the ETH Zürich"""

from . import building_physics
from . import emission_system
from . import supply_system
from . import radiation
from . import auxiliary
