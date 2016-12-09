# encoding: utf-8
import re

def main():
	r = open('./true.txt','r')  
	line = r.readline()
	
	i = 0;
	while line:  
		if len(line) > 5:
			# print len(line)
			i = i + 1
			stri = str(i);
			w = file('./true/'+stri+'.txt','w')  
			w.write(line)  
			w.close  
		line = r.readline() 
	r.close

	r = open('./false.txt','r')  
	line = r.readline()
	
	i = 0;
	while line:  
		if len(line) > 5:
			# print len(line)
			i = i + 1
			stri = str(i);
			w = file('./false/'+stri+'.txt','w')  
			w.write(line)  
			w.close  
		line = r.readline() 
	r.close

if __name__ == '__main__':
	main()