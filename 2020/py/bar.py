r = '253149867'
input = [int(x) for x in r]

#Part 1
def rotate(input):
    return input[1:] + input[:1]

def round(input):
    store = input[1:4]
    remain = input[:1] + input[4:]
    current = input[0] - 1
    while current not in remain:
        if current > min(input):
            current = current - 1
        else:
            current = max(input)
    dest = remain.index(current)
    input = remain[:dest+1] + store + remain[dest+1:]
    return rotate(input)

for x in range(100):
    input = round(input)

while input[0] != 1:
    input = rotate(input)

output = ''
for x in input:
    output = output + str(x)

print(output[1:])

#Part 2
input = [int(x) for x in r]
for x in range(max(input),1000000):
    input.append(x+1)

current = input[0]
ring = {}
for i in range(len(input)):
    if i == len(input) - 1:
        ring[input[i]] = input[0]
    else:
        ring[input[i]] = input[i+1]

def round(ring,current):
    maximum = 1000000
    minimum = 1
    next = ring[current]
    outside = [None,None,None]
    for x in range(3):
        outside[x] = next
        next = ring[next]
    ring[current] = next
    dest = current - 1
    if dest == 0:
        dest = maximum
    while dest in outside:
        if dest > minimum:
            dest = dest - 1
        else:
            dest = maximum
    stitch = ring[dest]
    ring[dest] = outside[0]
    ring[outside[2]] = stitch
    return ring, next

for x in range(10000000):
    ring,current = round(ring,current)

print(ring[1]*ring[ring[1]])
