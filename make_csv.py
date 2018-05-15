import csv

headers = ['酒店名', '地址', '星际', '电话']
with open('hotel.csv', 'w') as f:
    csv_write = csv.writer(f, dialect='excel')
    csv_write.writerow(headers)
