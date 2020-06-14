# Ant algorithm
This is the implementation of ant colony optimization to the Flow Shop Problem based on Thomas Stutzle article that you can 
download for free [here](https://pdfs.semanticscholar.org/dec2/f4177b3beaf9d5400d5886c25fe1a98bbbc5.pdf "Here").

This repository contains code and some files that I performed tests on. These files have different number of jobs and machines.

Algorithm gives better solution than e.g. Neh but only when you improve solution by using local search. In my implementation I used SA.

Below you can see my comparision of calculating best Cmax for attached files.

File    | Neh        | SA         | ACO        | ACO + SA  
------  | ---------- | ---------- | ---------- | ----------
ta002   | 1365       | 1365       | 1415       | 1359
ta012   | 1786       | 1725       | 2027       | 1659
ta022   | 2150       | 2150       | 2513       | 2126
ta032   | 2882       | 2882       | 3118       | 2828
ta042   | 3023       | 3023       | 3468       | 3023
ta052   | 3921       | 3959       | 4439       | 3908
ta062   | 5284       | 5284       | 5632       | 5289
ta072   | 5491       | 5491       | 6157       | 5349
Average | 3237       | 3234       | 3596       | 3222

