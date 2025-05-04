import csv

data=[['email','password'],
      ['bhoomilandge@gmail.com','Byak@0503']
      ]

with open('credentials.csv','w',newline='') as file:
    write=csv.writer(file)
    write.writerows(data)