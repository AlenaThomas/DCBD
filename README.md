# Assignment 1

Indian addresses show up on several web pages.  Note that there may be multiple addresses appearing in different parts of the same web page.

Our aim is to develop a tool that can extract addresses from such web pages, i.e. take each html file and reduce its contents. We must keep the address and try to remove as much other content form the input files as possible.

Indian addresses are written in multiple ways. So, you cannot make strong assumptions on the address format. For example, addresses may appear in a single line or across multiple lines. Addresses may not contain pincode. For evaluation, only websites containing at least one address in English may be chosen.

Write a process.py python file that takes html files from an input folder and writes the reduced files to an output folder such that you achieve maximum space gain.
