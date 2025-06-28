with open('samplemess.txt', 'rb') as f:
    binaryread = f.read()

print("This is the binary object that was read")
print(binaryread, "\n")

binarylist = list(bytearray(binaryread))

print("this is the list of bytes in decimal form recieved")
print(binarylist, "\n")

decodedread = binaryread.decode('utf-8')

print("This is the decoded version of the binary read")
print(decodedread, "\n")

def replace_92_110_with_10(lst):
    i = 0
    while i < len(lst) - 1:
        if lst[i] == 92 and lst[i + 1] == 110:
            lst[i] = 10
            del lst[i + 1]
        else:
            i += 1
    return lst

replacedlist = replace_92_110_with_10(lst=binarylist)

print("This is the binary list but with the 92 - 110 replaced with 10.")
print(replacedlist, "\n")

binaryreplaced = bytes(replacedlist)

print("This is the binary object of the replaced version")
print(binaryreplaced, "\n")

decodedreplaced = binaryreplaced.decode('utf-8')

print("this is the decoded version of the replaced binary")
print(decodedreplaced, "\n")