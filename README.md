# name_check
Python script to aid in coming up with Chinese kids names

This script helps with coming up with 3-character Chinese kid names. In the 3-character name format, names will start with the single-character family name, followed by 2 character given name. e.g. 金城武 - family-name 金, given-name 城武. Furthermore, the 1st character of the given name may or may not be fixed by the family. Often, families will have a poem that is used to determine the 1st character in the given name. With the 1st generation in the family using the 1st character in the poem, the 2nd generation using the 2nd character, and so on.

This script allows to come up with Chinese names given these constraints and sample texts used to choose the last character. Characters from the sample texts are used as the last character in names. Then, the name is sent off to http://www.123cha.com/ to calculate a naming score. Names with higher scores are considered to be more lucky. The scores and candidate names will be printed to stdout and output to an output file (sorted).

Usage:
```
$ ./name_check.py --help
usage: name_check.py [-h] [--family-name FAMILY_NAME]
                     [--middle-character MIDDLE_CHARACTER] --text TEXT
                     [--output OUTPUT]

Generate some name candidates.

optional arguments:
  -h, --help            show this help message and exit
  --family-name FAMILY_NAME
                        Family name to use in generation
  --middle-character MIDDLE_CHARACTER
                        Optional fixed middle character
  --text TEXT           Path to text file used for name generation. Must be
                        utf-8 encoded
  --output OUTPUT       Path to text file used as output
```

Example usage:
```
# generate names starting with 梁興 and ending with characters from 大學
./name_check.py --text=input_大學.txt --family-name=梁 --middle-character=興

# generate names starting with 黃 and ending with 2 characters from 論語
./name_check.py --text=input_論語.txt --family-name=黃
```
