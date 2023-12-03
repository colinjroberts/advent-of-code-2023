# Advent of Code 2023

An ambitiously structured repo for AoC with directories for each language I might try them in. Python reuses template code from past years for easy boilerplate generation and running one or more days.

## Starting a new day - Python
To generate templates for a new day, edit the `build_day(n)` in the entry point at the end of `tools.py` such n is the current, then run `python tools.py`. This will update `main.py` and generate txt files for the test and actual inputs. 

## Running one or more days - Python
Run the code for one or more days by updating `start, end = n, m` line in `main.py` then run that file to run all of the code for days `n` to `m`, inclusive. 