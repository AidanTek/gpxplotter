import csv

with open('/Users/sm21988/Documents/Python/pythoncsvreader/It_might_not_be_there_an_exhibition_tour/track_points.csv', newline='') as csvfile:
	xcoor = csv.reader(csvfile, delimiter=',', quotechar='|')
	for row in xcoor:
		print(', '.join(row)) # This specifically prints column 0 from the .csv file
