import sys
import math
import cmath
import numpy as np
arg0 = sys.argv[0]
a = len(sys.argv)
if (a != 2) or (".netlist" not in sys.argv[1]):
   print(" PLEASE ENTER A VALID COMMAND WITH THE CORRECT FILE TYPE. ")
else:
    filename = sys.argv[1]
    f = open(filename)
    lines = f.readlines()
    f.close()
    num_lines = len(lines)
    for i in range(num_lines):
        lines[i] = lines[i].split("\n")[0]
    if (".circuit" not in lines) or (".end" not in lines) or ((lines.index(".circuit")) > (lines.index(".end"))):
            print("  CORRUPT DATA IN FILE.  ")
    else:
            i = lines.index(".circuit")
            j = lines.index(".end")
            c = j-i-1 ; words = []
            for b in range(i+1,len(lines)):
                 lines[b]=lines[b].split('#')[0]
                 words.append((lines[b].strip(" ")).split(" "))

            list_node = []; Ref = { "GND" : 0}; vs = []; j = 1; vs1 = []; r = 0; w = 1e-30; y = 0; q = 0; n = 0
            for k in range(0,len(words)):
                if ".ac" in words[k][0]:
                    w = complex(words[k][2]); n = 1
            for i in range(0,c):
                list_node = list_node + [words[i][1]] + [words[i][2]]
                if words[i][0].lower().startswith("v"):
                    vs = vs + [i]; vs1 = vs1 + [words[i][0]]
                if words[i][0].lower().startswith("c"):
                    words[i][3] = -1j/(w*complex(words[i][3]))
                if words[i][0].lower().startswith("l"):
                    words[i][3] = 1j*(w*complex(words[i][3]))
            if n == 1:
                for q in range(0,len(vs)):
                    m = math.radians(float(words[q][5]))
                    words[q][4] = complex(words[q][4])*(complex(math.cos(m)) + complex(math.sin(m))*1j)
            list_node = np.unique(list_node);
            for i in range(0,len(list_node)):
                Ref[list_node[i]] = i
            M = np.zeros((len(vs) + len(list_node),len(vs) + len(list_node)),dtype = np.complex)
            b = np.zeros((len(vs) + len(list_node),1),dtype = np.complex)
            M[0][0] = 1
            for i in vs:
                b[i+1] = complex(words[i][4])
                M[j][Ref[words[i][2]]] = 1
                M[j][Ref[words[i][1]]] = -1
                j += 1 ;
            for k in range(1,len(list_node)):
                for i in range(0,c):
                    if words[i][0] in vs1:
                        x = 1
                    if (list_node[k] in words[i][1] and x!=1) :
                        M[j][k] = M[j][k] - (1/complex(words[i][3]))
                        M[j][Ref[words[i][2]]] += (1/complex(words[i][3]))
                    if (list_node[k] in words[i][2] and x!=1):
                        M[j][k] = M[j][k] - (1/complex(words[i][3]))
                        M[j][Ref[words[i][1]]] += (1/complex(words[i][3]))
                    x = 0
                j += 1;
            for k in range(1,len(list_node)):
                for i in range(0,len(vs)):
                    if words[vs[i]][1] in list_node[0]:
                        y = 1
                    if words[vs[i]][2] in list_node[0]:
                        r = 2
                    if (list_node[k] in words[vs[i]][1] and y != 1):
                            M[len(vs) + Ref[words[i][1]]][len(list_node) + vs[i]] -= 1
                    if (list_node[k] in words[vs[i]][2] and r != 2):
                        M[len(vs) + Ref[words[i][2]]][len(list_node) + vs[i]] += 1
                    y = 0 ; r = 0
            M = np.array(M) ; b = np.array(b)
            x = np.linalg.solve(M,b)
            a = x.real
            b = x.imag
            for i in range(0,len(list_node)):
                print("\n","\t",list_node[i]," --- ",round(math.hypot(a[i],b[i]),4),end = '')
                if n == 1:
                    print(" --- ",round(math.degrees(cmath.phase(x[i])),6))
            for i in range(0,len(vs)):
                print("\n","\t","I%d" %(i+1)," --- ", round(math.hypot(a[i + len(list_node)],b[i + len(list_node)]),4), end = '')
                if n == 1:
                    print(" --- ",round(math.degrees(cmath.phase(x[i + len(list_node)])),6))
            print("\n")

            #END OF CODE
