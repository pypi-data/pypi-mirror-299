# TerraHarmonize
This package was created for **SatSure SAGE**. It is designed for matching client data with internal data for proof-of-concept (POC) purposes. It is applicable to all states

### Installation
```sh
pip install TerraHarmonize
```
### Examples

For changing regional character to English.
```python
from TerraHarmonize import POC_matching

>>> string = '12/अ/1'
>>> print(POC_matching.char_assasin(string,'Hi'))
    '12/A/1'
```
For getting the index of the best match.

```python
from TerraHarmonize import POC_matching

>>> string = '13/A1'
>>> comparing_list = ['13/A1','14/A/1','12/A/1','13/అ','13-అ/1']
    #correct matching is [0,3,4] index i.e. '13/A1','13/అ','13-అ/1' 
>>> print(POC_matching(string,comparing_list).right_choice_AP(include='normal'))
    [0]
>>> print(POC_matching(string,comparing_list).right_choice_AP(include='both',state='AP'))
    [0, 3, 4]

```
Adding **/** inbetween a number and an alphabet.

```python
from TerraHarmonize import POC_matching

>>> data = '13/1AA/BB1/E'
>>> updated_data = POC_matching.string_updation(data,'En')
>>> print(updated_data)
    '13/1/AA/BB/1/E'

```