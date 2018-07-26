# sequence-analyzer
Analyze a datafile line-by-line to find (lack of) randomness.
Reads a data file and looks for repetitions and patterns at each index.
Great for cryptanalysis.

Dependencies:

  numpy

  matplotlib

  urllib


Usage: <code>python3 main.py -i \<input-file\> -d [decoder]</code>

Example: <code>python3 main.py -i samples/sample_hex.txt</code>

Output:
![sample_image.png](https://raw.githubusercontent.com/christianwang0x/sequence-analyzer/master/sample_image.png)
