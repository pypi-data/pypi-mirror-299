# **pycolors-kit**
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)

## Description

Search for color names through HEX, or search for color information through names

## Installation

Install `pycolors-kit` into your python environment, using:

```shell
pip install pycolors-kit
```

After installing, you can use the project as follows:

## Example

```python
from pycolors_kit import ColorEx


def test():
    color = ColorEx()

    print(color.get_name_by_hex('#fe9956'))
    print(color.get_color_by_name('acapulco sun'))
    print(color.get_name_by_rgb([200,54,76]))

    print(color.rgb_to_hex([200, 54, 76]))
    print(color.hex_to_rgb('#C8364C'))


if __name__ == '__main__':
    test()
```

### Output
```text

Autumn Splendor
{'name': 'Acapulco Sun', 'hex': '#eb8a44', 'rgb': {'r': 235, 'g': 138, 'b': 68}, 'hsl': {'h': 25, 's': 80.67633, 'l': 59.41176}, 
                                           'lab': {'l': 67.31829, 'a': 33.92547, 'b': 52.72836}, 'luminance': 107.51389}
Cherry Lolly
#C8364C
(200, 54, 76)

```
***