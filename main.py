import itertools
from operator import itemgetter, attrgetter, methodcaller

#MEMBUKA FILE EKSTERNAL
f = open('data.txt')
size = int(f.readline())

#MENYUSUN STRUKTUR DATA AWAL PADA MATRIKS
matrix = [['#' for x in range(size)] for y in range(size)]

for z in range(size):
	rowspace = f.readline()
	for y in range(size):
		matrix[z][y] = rowspace[y]

#MENDEKLARASIKAN KOTAK KOSONG MENDATAR DAN MENURUN
	#[row, start, finish]
horizontals = []
count = -999
start = -999
finish = -999

for z in range(size):
	row = z
	for y in range(size):
		if (matrix[z][y] == '-'):
			if (count == -999):
				start = y
				count = 1
			else:
				count += 1
				finish = y
		if (matrix[z][y] == '#') or (y == size-1):
			if (count > 1):
				horizontals.append(((row,start),(row,finish),count))
				count = -999
			elif (count == 1):
				count = -999
				start = -999
				finish = -999		

verticals = []

for y in range(size):
	col = y
	for z in range(size):
		if (matrix[z][y] == '-'):
			if (count == -999):
				start = z
				count = 1
			else:
				count += 1
				finish = z
		if (matrix[z][y] == '#') or (z == size-1):
			if (count > 1):
				verticals.append(((start,col),(finish,col),count))
				count = -999
			elif (count == 1):
				count = -999

blankspace = []
for z in range(len(horizontals)):
	blankspace.append(horizontals[z])
for z in range(len(verticals)):
	blankspace.append(verticals[z])
blankspace = sorted(blankspace, key=itemgetter(2))

blankspacelen = []
for z in range(len(blankspace)):
	blankspacelen.append(blankspace[z][2])

for z in range(len(blankspace)):
	blankspace[z] = list(blankspace[z])
	x_start = blankspace[z][0][0]
	x_finish = blankspace[z][1][0]
	y_start = blankspace[z][0][1]
	space_len = blankspace[z][2]
	if(x_start == x_finish):
		blankspace[z].append('H')
	else:
		blankspace[z].append('V')

#MENYUSUN STRUKTUR DATA SELURUH WORD DARI FILE EKSTERNAL
text = f.readline()
words = text.split(";")
wordsdata = []
for z in range(len(words)):
	wordsdata.append((words[z], len(words[z])))
wordsdata = sorted(wordsdata, key=itemgetter(1))
for z in range(len(wordsdata)):
	wordsdata[z] = list(wordsdata[z])
	wordsdata[z].append(-999)

#BRUTE FORCE MENGISIKAN KEMUNGKINAN JAWABAN
itr = 0
permutation = []
while (itr < len(blankspacelen)):
	intermed = []
	for z in range(itr, itr+blankspacelen.count(blankspacelen[itr])):
		intermed.append(z)
	permutation.append(intermed)
	itr += blankspacelen.count(blankspacelen[itr])

for z in range(len(permutation)):
	permutation[z] = list(itertools.permutations(permutation[z]))

cartesian_of_permutation = list(itertools.product(*permutation))

bruteforce = []
for z in range(len(cartesian_of_permutation)):
	flattened = []
	for sublist in cartesian_of_permutation[z]:
		for item in sublist:
			flattened.append(item)
	bruteforce.append(flattened)


#MELAKUKAN PENGECEKAN

def setpuzzle(matrix, wordsdata, blankspace, wordindex, spaceindex):
	x_start = blankspace[spaceindex][0][0]
	x_finish = blankspace[spaceindex][1][0]
	y_start = blankspace[spaceindex][0][1]
	space_len = blankspace[spaceindex][2]
	string_index = 0

	if (x_start == x_finish):						#horizontal space
		for z in range(y_start, y_start+space_len):
			matrix[x_start][z] = wordsdata[wordindex][0][string_index]
			string_index += 1
	else:											#vertical space
		for z in range(x_start, x_start+space_len):
			matrix[z][y_start] = wordsdata[wordindex][0][string_index]
			string_index += 1


def checkpuzzle(matrix, wordsdata, blankspace):
	isvalid = True

	for z in range(len(wordsdata)):
		spaceindex = wordsdata[z][2]
		x_start = blankspace[spaceindex][0][0]
		x_finish = blankspace[spaceindex][1][0]
		y_start = blankspace[spaceindex][0][1]
		space_len = blankspace[spaceindex][2]
		if (blankspace[wordsdata[z][2]][3] == 'H'):
			for string_index in range(len(wordsdata[z][0])):
				if (matrix[x_start][string_index] != wordsdata[z][0][string_index]):
					break
		else:
			for string_index in range(len(wordsdata[z][0])):
				if (matrix[string_index][y_start] != wordsdata[z][0][string_index]):
					break	

	return isvalid

for z in range(len(bruteforce)):
	for y in range(len(bruteforce[z])):
		setpuzzle(matrix, wordsdata, blankspace, y, bruteforce[z][y])
		wordsdata[y][2] = bruteforce[z][y]
	if (checkpuzzle(matrix, wordsdata, blankspace)):
		break

#MENCETAK
def printmatrix(matrix, size):
	for z in range(size):
		for y in range(size):
			print(matrix[z][y]),
		print

printmatrix(matrix, size)
for z in range(len(blankspace)):
	print blankspace[z]
for z in range(len(wordsdata)):
	print wordsdata[z]
for z in range(len(bruteforce)):
	print bruteforce[z]
printmatrix(matrix, size)

#MENUTUP FILE EKSTERNAL
f.close()

#https://stackoverflow.com/questions/952914/making-a-flat-list-out-of-list-of-lists-in-python