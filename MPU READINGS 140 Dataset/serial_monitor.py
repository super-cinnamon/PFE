import serial
from time import sleep
from time import time
import sys
from scipy.stats import skew
import pandas as p
import random
import math
import operator
from pycm import *

#classify training data through knn
#################################################### KNN CLASS ################################################################
class KNN:
			# Dans la class chaque fonction doit contenir "self" correpons a l'objet (passe en parametre)
			#Quant on applle une fonction a l'interieur d'une fonction on mis NOMCLASS.NOMMETHOD(self)

			def ReadDataSet(self , filename):
						d= p.read_csv(filename, sep=',',header=0, encoding='ascii', engine='python')
						return d

			##########################################################################################
			def DataInfo(self , d):
						print("")

						print("******************** Informations sur les attributs du dataset *******************")
						print(" longueur du dataset = ",len(d.index))
						print("")
						print("")

						info=d.info()
						print("**********************************************************")
						print("")
						print("")
						print("")

				#############################################
			 #la soustraction d'un attribut par attribut se fait d'une maniere automatique entre les deux ligne , ici line veut dire element
			def distanceEcludienne(self,line1 , line2 , length):
				 distance=0         
				 for x in range(length):
							 if ((type(line1[x]) == str) | (type(line2[x]) == str)):
										 if (line1[x]==line2[x]):
													 distance=0
										 else:
													 distance=1
							 else:
											distance += pow((line1[x]-line2[x]),2)
											
				 return math.sqrt(distance)
				 
			#############################################
			
			def VoisinKNN(self,instanceTest , trainingSet , k):
						distance = []
		
						# dans le length de test on met -1 psk le test ne contient pas de classe(label)
						length = len(instanceTest) -1

						#calculer la distance entre chaque nouvelle instance et les element de train dataset
						#puis ajouter le resultat dans une liste contenant "l'instance, la distance et l'indice de l'instance"
						for x in range(len(trainingSet)):
								dist = KNN.distanceEcludienne(self,instanceTest,trainingSet[x],length)
								distance.append((trainingSet[x],dist,x))

						#faire le tri selon la distance du plus petite au plus grande distance    
						distance.sort(key=operator.itemgetter(1))
						
						voisins=[]
						IndiceDist=[]
						#Garder que les K premières instances dans la liste "voisins" et la distance avec l'indice dans la liste "IndiceDist"
						for x in range (k+1):
								voisins.append(distance[x][0])
								#IndiceDist contient la distance , et l'indice de l'element
								IndiceDist.append((distance[x][2],distance[x][1]))
								
						print("voisins = ")
						
						print(voisins)

						print("Indice,Distance = ")
						print(IndiceDist)

						#voisinKNN retourn un enregistrement de deux listes voisins et IndiceDist
						return voisins,IndiceDist

			##Divide dataset into trainingSet and testSet

			def DivideDataset(self ,d , split , trainingDataset=[] , testSet=[]):
						count=0
						voisins=[]
						# X dans les ligne et Y dans les colonne
						lignes=d.values
						dataset = lignes.tolist()
						#choisir un nombre aléatoirement pour diviser le dataset en train et test
						for x in range (1,len(dataset)):
										a = random.random()
										if a < split:
												trainingDataset.append(dataset[x])
										else:
												testSet.append(dataset[x])
						 #le résultat c'est un enregistrement de deux liste.                    
						return trainingDataset,testSet


			###### ici voisins c'est une liste qui contient toute les voisins (comme des elements)######################################
			def ClassifyF (self,K,trainingDataset , testSet):
						
						#pour chaque instance faire
						for x in range (len(testSet)):
												#former l'ensemble des K voisins
												v=KNN.VoisinKNN(self,testSet[x] , trainingDataset , K)
												voisins=v[0]
												#declarer un dictionnaire (enregistrement cle:valeur)**VoisinOccurance={'normal':3}
												VoisinOccurance = {}
												#pour chaque voisin determiner le nombre d'occurrence de chaque classe
												for y  in range (len(voisins)):
														#voisins[x][-1] le x correspond a la ligne et le -1 (modulo) c la classe
														ClasseChoisie = voisins[y][-1]
														if ClasseChoisie in VoisinOccurance:
																VoisinOccurance[ClasseChoisie]+=1
														else:
																VoisinOccurance[ClasseChoisie]=1
																
												#key=operator.itemgetter(1) veut dire faire le tri selon le 2eme element(le premier elem c'est zero)
												#generer une liste de paire cle,val ex: list = [('a',2), ('b',1),('c',0)]
												#trier une list contenant les elements triées de plus grand au plus petit (reverse)        
												VoisinOccSorted = sorted(VoisinOccurance.items(),key=operator.itemgetter(1),reverse=True)
												print('la classe est:')
												print(VoisinOccSorted[0][0])

												testSet[x][-1]=VoisinOccSorted[0][0]
												
						return testSet
			 ###############################################################
			def ClassifyI (self,trainingDataset , instance,K):
						#former l'ensemble des K voisins
						v=KNN.VoisinKNN(self,instance , trainingDataset , K)
						voisins=v[0]
						VoisinOccurance = {}
						#pour chaque voisin determiner le nombre d'occurrence de chaque classe
						for y  in range (len(voisins)):
									#voisins[x][-1] le x correspond a la ligne et le -1 on travaille par modulo il correspond a la derniere case(c'est la classe)
									#VoisinOccurance contient le nombre d'occurrence de chaque classe dans l'ensemble "voisin"
									ClasseChoisie = voisins[y][-1]
									if ClasseChoisie in VoisinOccurance:
												VoisinOccurance[ClasseChoisie]+=1
									else:
												VoisinOccurance[ClasseChoisie]=1

						#key=operator.itemgetter(1) veut dire faire le trie selon le 2eme element(le premier elem c'est zero)
						#generer une liste de paire cle,val ex: list = [('a',2), ('b',1),('c',0)]
						#trier une list contenant les elements triées de plus grand au plus petit (reverse)      
						VoisinOccSorted = sorted(VoisinOccurance.items(),key=operator.itemgetter(1),reverse=True)
						print('la classe est:')
						print(VoisinOccSorted[0][0])
						for x in range(len(instance)):
									if(x == (len(instance)-1)):
												
												instance[x]=VoisinOccSorted[0][0]
												print("instance: " ,instance[x])
												
						return VoisinOccSorted[0][0],v[1]
		###########################################################################
			def ADDInstnace( self, train, instance):
						train.append(instance)
						return train
			###################################################################
			def WriteFile( self, filename, instance):
						with open(filename,'a') as f:
									for i in range(0,len(instance)-1):
												f.write(str(instance[i])+",")
									f.write(str(instance[len(instance)-1]))    
									f.write("\n")
									f.close()

####################################################### MAIN ##################################################################
Obj1=   KNN()

#Appelle d'une method de la classe
d = KNN.ReadDataSet(Obj1,r'moves for weka.csv')
KNN.DataInfo(Obj1, d)
dataset = KNN.DivideDataset(Obj1,d , 1 , [] , [])
#connecting to the arduino

COM = 'COM3'
first = 1
BAUD = 19200
ser = serial.Serial(COM, BAUD)
start_time = time()
seconds = 4
print('waiting for device')
print(ser.name)
theArray = []
roll = []
pitch = []
yaw = []

while(1):
	if(first == 1):
		start = time()
		first = 2
		while (1):
			current = time()
			elap = current - start
			line = ser.readline()
			if(elap > 2.2):
				break
	current_time = time()
	elapsed_time = current_time - start_time
	line = ser.readline()
	lineStr = line.decode()
	lineStr = lineStr.strip()
	theArray.append(lineStr)	
	if elapsed_time > seconds:
		for x in theArray:
			line = x.split("/")
			roll.append(float(line.pop(0)))
			temp = line.pop(0)
			temp.replace("\n", "")
			pitch.append(float(temp))
			temp = line.pop(0)
			temp.replace("\n", "")
			yaw.append(float(temp))
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
		# put the class to nothing
		move.append('')
		# classify here with knn
		testdataset = KNN.ClassifyI(Obj1, dataset[0], move, 3)
		# print the result
		print(testdataset)
		del testdataset

		tempostr = ""
		for element in move:
			tempostr = tempostr + str(element) + ","
		tempostr = tempostr[:-1]
		print(tempostr)

		theArray = []
		roll = []
		pitch = []
		yaw = []
		start_time = time()
