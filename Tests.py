import numpy as np

reflector = [25, 23, 21, 19, 17, 15, 13, 11, 9, 7, 5, 3, 1, -1, -3, -5, -7, -9, -11, -13, -15, -17, -19, -21, -23, -25]

rotor3 = [[12, -1, 23, 10, 2, 14, 5, -5, 9, -2, -13, 10, -2, -8, 10, -6, 6, -16, 2, -1, -17, -5, -14, -9, -20, -10],
		 [1, 16, 5, 17, 20, 8, -2, 2, 14, 6, 2, -5, -12, -10, 9, 10, 5, -9, 1, -14, -2, -10, -6, 13, -10, -23]]	 
rotor2 = [[25, 7, 17, -3, 13, 19, 12, 3, -1, 11, 5, -5, -7, 10, -2, 1, -2, 4, -17, -8, -16, -18, -9, -1, -22, -16], [3, 17, 22, 18, 16, 7, 5, 1, -7, 16, -3, 8, 2, 9, 2, -5, -1, -13, -12, -17, -11, -4, 1, -10, -19, -25]]
		 
rotor1 = [[17, 4, 19, 21, 7, 11, 3, -5, 7, 9, -10, 9, 17, 6, -6, -2, -4, -7, -12, -5, 3, 4, -21, -16, -2, -21 ], [10, 21, 5, -17, 21, -4, 12, 16, 6, -3, 7, -7, 4, 2, 5, -7, -11, -17, -9, -6, -9, -19, 2, -3, -21, -4]]
		 
alphabet_codes = np.arange(26)

Output = ""

#textInput  = input("here:")
#listInput = list(textInput)

Input1 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
#Result Output1 : TXHSKJICGFEOQWLZMUDARYNBVP & Expected:
Input2 = "abcdefghijklmnopqrstuvwxyz"
#Result Output2 : ICGFEOQWLZMUDARYNBVPTXHSKJ & Expected:
Input3 = "AbCdEfGhLmNoPqRStUvWxYz"
#Result Output3 : TCHFKOIWODWRZNUDPRXNSVJ & Expected:
Input4 = "Lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod tempor incididunt ut labore et dolore magna aliqua Ut enim ad minim veniam quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur Excepteur sint occaecat cupidatat non proident sunt in culpa qui officia deserunt mollit anim id est laborum"
#Result Output4 :  TCHFKOIWODWRZNUDPRXNSVJ & Expected:
for letter in Input4:
	code = ord(letter) - 65
	##ALLER
	p = code % 26
	positionR1 = rotor1[1][p]
	p += positionR1
	positionR2 = rotor2[1][p % 26]
	p += positionR2
	positionR3 = rotor3[1][p % 26]
	p += positionR3
	positionR = reflector[p % 26]
	p += positionR
	
	
	#print(positionR1)
	#print(positionR2)
	#print(positionR3)
	#print(positionR)

	##RETOUR
	positionR3 = rotor3[0][p % 26]
	p += positionR3
	positionR2 = rotor2[0][p % 26]
	p += positionR2
	positionR1 = rotor1[0][p % 26]
	p += positionR1
	
	
	#print(positionR)
	#print(positionR3)
	#print(positionR2)
	#print(positionR1)
	#print("lettre encryptée:", chr((p %26)+ 65))
	Output += chr((p %26)+ 65)
	
	#print("p is",p)
	
print(Output)
#print(alphabet_codes)
#print(listInput)
