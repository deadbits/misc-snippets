#!/usr/bin/env python
# script to demonstrate computation of Hamming distance
# between two strings
# this example was taken from the Wikipedia page.
# it is included in this repo as a reference of my own
# and the calculation function is not my own creation.


def calculate_distance(str1, str2):
		assert len(str1) == len(str2)
		dist = sum(ch1 != ch2 for ch1, ch2 in zip(str1, str2))
		print("Result: ")
		print(dist)

def main():
		string_one = raw_input("string one: ")
		string_two = raw_input("string two: ")
		if len(string_one) != len(string_two):
				print("string lengths are not identical!")
				sys.exit(1)
		calculate_distance(string_one, string_two)

main()
