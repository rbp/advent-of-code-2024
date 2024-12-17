stones in a line, numbered
sometimes the number on a stone change. 
Sometimes, the stone splits in 2 (the others must shift)

Rules (appy first applicable), applied to each stone. All stones change simultaneously!
1. if n == 0, n == 1
2. if n has *even* number of digits, replace with *2* stones.
    left half of digits on new left stone, right half on new right stone.
    *no leading zeroes*
3. If nothing else appplies, n = n * 2024

Order is always preserved

