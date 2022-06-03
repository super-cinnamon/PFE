import glob
from scipy.stats import skew
import xlsxwriter

workbook = xlsxwriter.Workbook('ALLinstancesTable.xlsx')
worksheet = workbook.add_worksheet()
titles = ["maxroll","maxpitch","maxyaw","minroll","minpitch","minyaw","avgroll","avgpitch","avgyaw","ranroll","ranpitch","ranyaw","asyroll","asypitch","asyyaw","class"]
row = 0
i=0
for i in range(0,15):
	worksheet.write(row,i, titles[i])

row += 1

file_name = "MPUREAD 1 move right*.txt" 
for file_name_wild in glob.glob(file_name):
	with open(file_name_wild, "r") as file:
		pitch = []
		roll = []
		yaw = []
	
		for x in file:
			line = x.split("/")
			roll.append(float(line.pop(0)))
			temp = line.pop(0)
			temp.replace("\n", "")
			pitch.append(float(temp))
			temp = line.pop(0)
			temp.replace("\n", "")
			yaw.append(float(temp))
		file.close()

		move = []
	# max
		move.append(max(roll))
		move.append(max(pitch))
		move.append(max(yaw))
	# min
		move.append(min(roll))
		move.append(min(pitch))
		move.append(min(yaw))
	# mean
		move.append(sum(roll) / len(roll))
		move.append(sum(pitch) / len(pitch))
		move.append(sum(yaw) / len(yaw))
	# range
		move.append(max(roll) - min(roll))
		move.append(max(pitch) - min(pitch))
		move.append(max(yaw) - min(yaw))
	# asymmetry
		move.append(skew(roll))
		move.append(skew(pitch))
		move.append(skew(yaw))

		move.append("on")

		i = 0
		for i in range(0,15):
			worksheet.write(row,i,move[i])
		row += 1
		

file_name = "MPUREAD 1 move wrong*.txt"
for file_name_wild in glob.glob(file_name):
	with open(file_name_wild, "r") as f:
		pitch = []
		roll = []
		yaw = []

		for x in f:
			line = x.split("/")
			roll.append(float(line.pop(0)))
			temp = line.pop(0)
			temp.replace("\n", "")
			pitch.append(float(temp))
			temp = line.pop(0)
			temp.replace("\n", "")
			yaw.append(float(temp))
		f.close()
		move = []
		# max
		move.append(max(roll))
		move.append(max(pitch))
		move.append(max(yaw))
		# min
		move.append(min(roll))
		move.append(min(pitch))
		move.append(min(yaw))
		# mean
		move.append(sum(roll) / len(roll))
		move.append(sum(pitch) / len(pitch))
		move.append(sum(yaw) / len(yaw))
		# range
		move.append(max(roll) - min(roll))
		move.append(max(pitch) - min(pitch))
		move.append(max(yaw) - min(yaw))
		# asymmetry
		move.append(skew(roll))
		move.append(skew(pitch))
		move.append(skew(yaw))
		
		move.append("off")

		i = 0
		for i in range(0,15):
			worksheet.write(row,i,move[i])
		row += 1	

workbook.close()
