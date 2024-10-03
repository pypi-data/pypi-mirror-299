# SimpleCalculator

`SimpleCalculator` is a basic Python class for performing arithmetic operations. It supports addition, subtraction, multiplication, division, modulus, and floor division. You can also check equality between two numbers.

## Features

- Add two numbers
- Subtract two numbers
- Multiply two numbers
- Divide two numbers
- Modulus of two numbers
- Floor division of two numbers
- Check if two numbers are equal
- Retrieve the last calculated result

## Installation

You can install this package from PyPI (once uploaded) using pip:

```bash

pip install simplecalculatoruniue

```

## Usage

from simplecalculator import SimpleCalculator

# Create an instance of the calculator

calc = SimpleCalculator()

# Perform operations
add_result = calc.add(5, 3)        # 8
sub_result = calc.sub(10, 4)       # 6
mul_result = calc.mul(7, 2)        # 14
div_result = calc.div(15, 3)       # 5.0
mod_result = calc.mod(10, 3)       # 1
floor_result = calc.floor(10, 3)   # 3
equal_result = calc.equal(5, 5)    # True

# Get the last result
last_result = calc.get_result()    # Returns the result of the last operation

# License

# This project is licensed under the MIT License.

