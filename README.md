# decodeAltairTapes
a little bit of code that decodes an altair tape from a wav file into a .bin

I wrote this code to decode an original Altair 8K BASIC cassette tape I own to a .bin file.

A note about versions of basic..   The 8k v3.2 version of basic tape starts with a leader byte of 0xae..  that also happens to be the length of the second stage bootstrap code found at the beginning of the tape.  so my code skips all the 0xae bytes, plus a count of 0xad bytes which comprise the bootstrap loader.  following that is the packets that make up the actual BASIC load..  If you have a cassette for
a different version of BASIC you can do some checking on your own.. such as let minimodem decode to basic.dat -- the rest of the program will fail,but take a look at the value of the leader bytes found at the beginning of basic.dat.  Next use the -L option on the command line to rerun with that byte value in decimal.

This project does not distribute Microsoft’s Altair BASIC binaries. You must supply your own copy from legally obtained sources (e.g., original cassette, licensed distribution).”

What it does is use "minimodem" to convert a mono .wav file in a file name cassette.wav into
a basic.dat file of raw demodulated bytes.
Then it interprets the bytes accoridng to the packet types found on Altair tapes.

Since it's geared for Altair BASIC, it knows to ignore the second level boot loader found on the tape
and after loading the packets into scratch memory, it dumps the table of BASIC keywords as
a sanity check.  Then it dumps the scratch memory out to a file basicLoad.bin.

However, it should be usable (with some minor modifications) to decode any original Altair tape
The current code assumes Mark:2400hz and Space:1850hz and 300 baud.

## Prerequsites
You will need to install minimodem and have it on your path.
You will need a version of Python 3 to run this code

## Running
NOTE!: The code now takes command line arguments so the following is based on the defaults.  Type
"python3 altairScanToTape.py -h"  for options.

sample your cassette into a mono .wav file and call it "cassette.wav" in your current directory
then run: python3 altairScanToTape.py

It will print out succesful packets found (reporting checksum status etc)
Then it will print out the list of BASIC keywords found
Then it will print out a 16 bit simple checksum (useful if you are writing a loader to load the .bin somewhere)

It will deposit into the current directory:

basic.dat  -- the raw bytes that minimodem found

basicLoad.bin --   a memory dump containing the unpacked and loaded basic.
