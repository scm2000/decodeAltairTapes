import os

def printKeywords(memory):
    curAddr = 0x88
    curIdx = 0
    while memory[curAddr] != 0:
        print(chr(memory[curAddr] & 0x7f), end = '')
        if memory[curAddr] & 0x80:
            print(f'   {curIdx}')
            curIdx += 1
        curAddr += 1
    #right after the keywords is a table of branch addresses
    print(hex(curAddr))
    curAddr =0x43
    for i in range(24):
        lo = memory[curAddr]
        curAddr += 1
        baddr = memory[curAddr] * 256 + lo
        curAddr += 1
        print(f'{i}: {hex(baddr)}')
    return

os.system("minimodem --rx -M 2400 -S 1850 -f cassette.wav 300 >basic.dat")

fp = open('basic.dat', 'rb')
print('skipping leader')
a = fp.read(1)[0]
a = fp.read(1)[0]
print(hex(a))
cnt = 1
while a == 0xae:
  a = fp.read(1)[0]
  cnt += 1
print(f'there were {cnt} leader bytes')
print('skipping checksum loader')
cl = fp.read(0xad)
print(hex(cl[-1]))

memory = bytearray(0x8000) #32k (bank switching is a problem)
hmem = 0
#loop for all packets
while True :
    #scan for a packet. either 0x3c or 0x78
    a = fp.read(1)[0]
    while a != 0x3c and a != 0x78:
        a = fp.read(1)[0]
    if a == 0x3c:
        #get len
        plen = fp.read(1)[0]
        #get addr
        checksum = lowaddr = fp.read(1)[0]
        hiaddr = fp.read(1)[0]
        checksum += hiaddr
        checksum = checksum % 256
        paddr = hiaddr*256+lowaddr
        #store bytes in memory and do the checksum
        maddr = paddr
        cnt = 0
        for i in range(plen):
            a = fp.read(1)[0]
            checksum += a
            checksum = checksum % 256
            memory[maddr] = a
            if maddr > hmem:
                hmem = maddr
            maddr += 1
            cnt += 1
        #read the packet checksum
        pcheck = fp.read(1)[0]
        print(f"read data packet: {plen}/{cnt} bytes at {hex(paddr)} hmem={hex(hmem)}, {'good' if checksum == pcheck else 'bad'} checksum {checksum}..{pcheck}")
    else:
        lowaddr = fp.read(1)[0]
        hiaddr = fp.read(1)[0]
        paddr = hiaddr*256+lowaddr
        print(f"read start packet, addr {hex(paddr)}")
        print('dumping memory')

        #before patching, print out keywords
        printKeywords(memory)

        ofp = open('basicLoad.bin', 'wb')
        #this is the runnable basic code
        ofp.write(memory[:hmem+1])

        #compute 16 bit checksum
        checksum = sum(memory[:hmem+1]) & 0xffff
        print(hex(checksum))
        exit()



