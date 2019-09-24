#!/usr/bin/python -tt
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

"""Wordcount exercise
Google's Python class

The main() below is already defined and complete. It calls print_words()
and print_top() functions which you write.

Workflow: don't build the whole program at once. Get it to an intermediate
milestone and print your data structure and sys.exit(0).
When that's working, try for the next milestone.

"""

import sys
import string
import collections

def file_to_dict(filename):
  dict_word= collections.Counter()
  with open(filename) as f:
    lines = f.readlines()
  for line in lines:
    line = remove_punctuation(line)
    words = line.split()
    dict_word.update(words)
  return dict_word


def remove_punctuation(string_input):
  for char in string.punctuation + string.digits:
    string_input = string_input.replace(char, "")
  return string_input


def file_to_sorted_dict_by_key(filename):
  dict_out = file_to_dict(filename)
  return collections.Counter(dict(sorted(dict_out.items(), key=lambda item: item[0])))

# Optional: define a helper function to avoid code duplication inside
# print_words() and print_top().
def print_output(input):
  for item in input:
    print(item[0] + ": " + str(item[1]))

# 1. For the --count flag, implement a print_words(filename) function that counts
# how often each word appears in the text and prints:
# word1 count1
# word2 count2
# ...
#
# Print the above list in order sorted by word (python will sort punctuation to
# come before letters -- that's fine). Store all the words as lowercase,
# so 'The' and 'the' count as the same word.
def print_words(filename):
  dict_sorted_by_key = file_to_sorted_dict_by_key(filename)
  print_output(dict_sorted_by_key.items())

# 2. For the --topcount flag, implement a print_top(filename) which is similar
# to print_words() but which prints just the top 20 most common words sorted
# so the most common word is first, then the next most common, and so on.
#
# Use str.split() (no arguments) to split on all whitespace.
def print_top(filename):
  dict_sorted_by_key = file_to_sorted_dict_by_key(filename)
  most_commun = dict_sorted_by_key.most_common(20)
  print_output(most_commun)
  return

# This basic command line argument parsing code is provided and
# calls the print_words() and print_top() functions which you must define.
def main():
  if len(sys.argv) != 3:
    print('usage: ./wordcount.py {--count | --topcount} file')
    sys.exit(1)

  option = sys.argv[1]
  filename = sys.argv[2]
  if option == '--count':
    print_words(filename)
  elif option == '--topcount':
    print_top(filename)
  else:
    print('unknown option: ' + option)
    sys.exit(1)

if __name__ == '__main__':
  main()
