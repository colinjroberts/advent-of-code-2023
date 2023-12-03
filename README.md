# Advent of Code 2023

An ambitiously structured repo for AoC with directories for each language I might try them in. Python reuses template code from past years for easy boilerplate generation and running one or more days.

## Python

### Structure
- `inputs`: a directory with the txt files for each day's problems.
- `main.py`: the driver for running one or more days of code.
- `tools.py`: input processing tools and the template generator
- `p__.py`: files for each day. They each have a method of the same name called by `main.py` and `part1` and `part2` methods as entry points for each half of the problem. 

### Starting a new day
To generate templates for a new day, edit the `build_day(n)` in the entry point at the end of `tools.py` such n is the current, then run `python tools.py`. This will update `main.py` and generate txt files for the test and actual inputs. 

### Running one or more days
Run the code for one or more days by updating `start, end = n, m` line in `main.py` then run that file to run all of the code for days `n` to `m`, inclusive. 