# decodeAltairTapes
a little bit of code that decodes an altair tape from a wav file into a .bin

I wrote this code to decode an original Altair 8K BASIC cassette tape to a .bin file

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
sample your cassette into a mono .wav file and call it "cassette.wav" in your current directory
then run: python3 altairScanToTape.py

It will print out succesful packets found (reporting checksum status etc)
Then it will print out the list of BASIC keywords found
Then it will print out a 16 bit simple checksum (useful if you are writing a loader to load the .bin somewhere)

It will deposit into the current directory:

basic.dat  -- the raw bytes that minimodem found

basicLoad.bin --   a memory dump containing the unpacked and loaded basic.
