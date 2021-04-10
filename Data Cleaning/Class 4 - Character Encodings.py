# Character Encodings
import pandas as pd
import numpy as np
import chardet

### start with a string
before = "This is the euro symbol: €"

### check to see what datatype it is
type(before)

### encode it to a different encoding, replacing characters that raise errors
after = before.encode("utf-8", errors="replace")

### check the type
type(after)

### start with a string
before = "This is the euro symbol: €"

### encode it to a different encoding, replacing characters that raise errors
after = before.encode("ascii", errors = "replace")

### convert it back to utf-8
print(after.decode("ascii"))

### try to read in a file not in UTF-8
kickstarter_2016 = pd.read_csv("../Data/ks-projects-201612.csv")

### look at the first ten thousand bytes to guess the character encoding
with open("../input/kickstarter-projects/ks-projects-201801.csv", 'rb') as rawdata:
    result = chardet.detect(rawdata.read(10000))

### check what the character encoding might be
print(result)

### read in the file with the encoding detected by chardet
kickstarter_2016 = pd.read_csv("../input/kickstarter-projects/ks-projects-201612.csv", encoding='Windows-1252')

### save our file (will be saved as UTF-8 by default!)
kickstarter_2016.to_csv("ks-projects-201801-utf8.csv")
