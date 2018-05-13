import csv

with open('VQHA69.csv') as csvfile: #, newline=''
     weather = csv.reader(csvfile, delimiter='|')
     for row in weather:
         print(', '.join(row)) 
