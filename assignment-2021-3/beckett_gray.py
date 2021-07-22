import itertools ,time ,sys

def CreateStrings(n,Nodes):
    if len(Nodes[0]) == n:
        return Nodes
    else:
        NewNodes=[]
        for String in Nodes:
            String1="0" + String
            String2="1" + String[::-1]
            NewNodes.append(String1)
            NewNodes.append(String2)
    return CreateStrings(n,NewNodes)

def DecimalToBinary (Dec , n):
    Binary = ""
    for i in range (2,len(bin(Dec))):
        Binary += bin(Dec)[i]

    Binary = Binary.zfill( n)
    return Binary

def BinaryToDecimal (Bin):
    Decimal = 0
    power = len(Bin)-1
    for number in Bin:
        if number == "1":
            Decimal += 2 **power
        power -=1
    return Decimal

def AlterBinary (Binary , i):
    AlteredBinary = ""
    i = len(Binary) -1 -i
    for j in range (0 , len(Binary)):
        if j == i :
            if Binary [i] =="0":
                AlteredBinary += "1"
            else:
                AlteredBinary += "0"
        else :
            AlteredBinary += Binary[j]
    return AlteredBinary

def Flip(x,i):
    BinaryString = DecimalToBinary(x , n)
    ChangedBinary = AlterBinary(BinaryString , i)
    return BinaryToDecimal(ChangedBinary)

def SequenceToDelta(code):
    delta=""
    for i in range(0,len(code)-1):
        element1 = code[i][::-1]
        element2 = code[i+1][::-1]
        for j in range(0,len(element1)):
            if element1[j] != element2[j]:
                delta += str(j)
                continue
    return delta

def GC_DFS(d, x, max_coord, n, gc):
    if d == 2**(n-1):
        all_codes.append(gc.copy())
        return
    for i in range(0,min(n-1,max_coord+1)):
        x = Flip(x,i)
        if not visited[x]:
            visited[x] = True
            gc.append(x)
            GC_DFS(d+1,x,max(i+1,max_coord),n,gc)
            visited[x] = False
            gc.pop()
        x = Flip(x,i)

def GC_DFS_Beckett(d, x, max_coord, n, gc,tail):
    if d == 2 ** (n - 1):
        all_codes.append(gc.copy())
        return
    for i in range(0, min(n - 1, max_coord + 1)):
        BinVersion = DecimalToBinary(x, n)
        if BinVersion[::-1][i] == "1":
            if tail[0] != i:
                continue
        x = Flip(x, i)

        if not visited[x]:
            keeptail = tail.copy()
            if BinVersion[::-1][i] == "1":
                if tail[0] == i:
                    tail.pop(0)
            else:
                tail.append(i)

            visited[x] = True
            gc.append(x)
            GC_DFS_Beckett(d + 1, x, max(i + 1, max_coord), n, gc,tail)
            visited[x] = False
            tail = keeptail.copy()
            gc.pop()
        x = Flip(x, i)

def CheckIfCircle(Code):
    # We will check here if the last element has only one 1 between zeros meaning its circle
    if Code[-1].count("1") == 1:
        for i in range(0,len(Code)):
            if Code[-1][::-1][i] == "1":
                return i
    else:
        return False


if sys.argv[-1] =="-r":
   n = int(sys.argv[2])
else:
   n= int(sys.argv[-1])
n = n +1
all_codes=[]
Strings=CreateStrings(n,[""])
visited = [False]*len(Strings)
visited[0] = True
stack =[0]
tail=[]




if len(sys.argv) == 2 or (len(sys.argv) == 3 and sys.argv[1] =="-a"):
    GC_DFS(1, 0, 0, n, stack )
    for i in range(0, len(all_codes)):
        for j in range(0, len(all_codes[i])):
            all_codes[i][j] = DecimalToBinary(all_codes[i][j], n - 1)
    Deltas = []
    for solution in all_codes:
        Deltas.append(SequenceToDelta(solution))
        if CheckIfCircle(solution):
            Deltas[-1] += str(CheckIfCircle(solution))
            print("C",Deltas[-1])
        else:
            print("P",Deltas[-1])
elif  len(sys.argv) == 3:
    if sys.argv[1] == "-b" :
        GC_DFS_Beckett(1, 0, 0, n, stack,tail)
        for i in range(0, len(all_codes)):
            for j in range(0, len(all_codes[i])):
                all_codes[i][j] = DecimalToBinary(all_codes[i][j], n - 1)
        Deltas = []
        for solution in all_codes:
            if CheckIfCircle(solution):
                Deltas.append(SequenceToDelta(solution))
                Deltas[-1] += str(CheckIfCircle(solution))
                print("B" ,Deltas[-1])
    if sys.argv[1] == "-c" :
        GC_DFS(1, 0, 0, n, stack)
        for i in range(0, len(all_codes)):
            for j in range(0, len(all_codes[i])):
                all_codes[i][j] = DecimalToBinary(all_codes[i][j], n - 1)
        Deltas = []
        for solution in all_codes:
            if CheckIfCircle(solution):
                Deltas.append(SequenceToDelta(solution))
                Deltas[-1] += str(CheckIfCircle(solution))
                print("C", Deltas[-1])
    if sys.argv[1] == "-u" :
        GC_DFS_Beckett(1, 0, 0, n, stack, tail)
        for i in range(0, len(all_codes)):
            for j in range(0, len(all_codes[i])):
                all_codes[i][j] = DecimalToBinary(all_codes[i][j], n - 1)
        Deltas = []
        for solution in all_codes:
            if not CheckIfCircle(solution):
                Deltas.append(SequenceToDelta(solution))
                print("U", Deltas[-1])
elif len(sys.argv) == 4:
    if sys.argv[-1] == "-r" :

        GC_DFS_Beckett(1, 0, 0, n, stack,tail)
        for i in range(0, len(all_codes)):
            for j in range(0, len(all_codes[i])):
                all_codes[i][j] = DecimalToBinary(all_codes[i][j], n - 1)
        Deltas = []
        for solution in all_codes:
            if CheckIfCircle(solution):
                Deltas.append(SequenceToDelta(solution))
                Deltas[-1] += str(CheckIfCircle(solution))
                print("B" ,Deltas[-1])
        PermutationsString = ""
        for k in range(0, n - 1):
            PermutationsString += str(k)
        permutations = list(itertools.permutations(PermutationsString))
        for delta in range(0, len(Deltas)):
            Versions = []
            for permutation in permutations:
                version = ""
                for number in Deltas[delta]:
                    version += permutation[int(number)]
                Versions.append(version)
            for j in range(delta, len(Deltas)):
                if Deltas[j][::-1] in Versions:
                    print(Deltas[delta], "<=>", Deltas[j])
    if sys.argv[2] == "-f" :
        GC_DFS_Beckett(1, 0, 0, n, stack,tail)
        for i in range(0, len(all_codes)):
            for j in range(0, len(all_codes[i])):
                all_codes[i][j] = DecimalToBinary(all_codes[i][j],n - 1)
        Deltas = []
        for solution in all_codes:
            if CheckIfCircle(solution):
                Deltas.append(SequenceToDelta(solution))
                Deltas[-1] += str(CheckIfCircle(solution))
                print("B" ,Deltas[-1])
                print("B" ,*solution)
    if sys.argv[1] == "-u" :
        GC_DFS_Beckett(1, 0, 0, n, stack, tail)
        for i in range(0, len(all_codes)):
            for j in range(0, len(all_codes[i])):
                all_codes[i][j] = DecimalToBinary(all_codes[i][j], n - 1)
        Deltas = []
        for solution in all_codes:
            if not CheckIfCircle(solution):
                Deltas.append(SequenceToDelta(solution))
                print("U", Deltas[-1])
            for i in range(len(solution[0])-1,-1,-1):
                string =""
                for item in solution:
                    print(item[i],"",end="")
                print("")

