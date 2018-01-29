# Import any necessary modules or packages 
import csv
import re
import os
import itertools

# Allows for manual input of filename
filename = raw_input("What is the filename: ")
# Comparative file. Needs to be updated every week. 
unreachables = 'clean_unreachables.csv'

# Main function. Use '#' to negate any unnecessary scripts 
def main():
	email_trimmer(filename)
	email_checker(filename)
	email_unreachable(filename, unreachables)
	email_send(filename, unreachables)

# Pre-processes the data to remove any empty spaces that may trigger  
# the email checker below 
def email_trimmer(filename):
	with open(filename, 'rU') as csvfile, open(('trim_%s' % filename), 'wb') as output:
		writer = csv.writer(output, delimiter=',')
		readCSV = csv.reader(csvfile, delimiter = ',')
		
		writer.writerow(["email"])
		next(readCSV)
		
		for row in readCSV:
			address = row

			if address == []:
				next(readCSV)			
			
			else:
				address = row[0]
				address.strip()
				address = re.sub(' ', '',address)
				writer.writerow([address])
	print "Trimmer - Successfully completed!"	

# Scans each email to ensure that it has an arabesque(@), a period(.)
# and text before and after the arabesque and before and the after 
# the period. It corrects some pre-determined errors and automatically adds
# two necessary emails  
def email_checker(filename):
	results = []

	with open(('trim_%s' % filename), 'rU') as csvfile, open(('customer_zaius_%s' % filename), 'wb') as output:
		readCSV = csv.reader(csvfile, delimiter = ',')
		writer = csv.writer(output, delimiter=',')
		writer.writerow(["email"])
		next(readCSV)

		for row in readCSV:
			address = row

			if address == []:
				next(readCSV)

			else:
				match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z0-9-]+)*(\.[a-z0-9-]+)*(\.[a-z0-9-]+)$', address[0].lower())
				if match != None:
					writer.writerow(address)

				else:
					sub = re.sub('[\xc2\xc3\xa3\xbe\x8e\xae\x83\xa8\xe6\xc4\xca\n]','', address[0].lower())
					match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z0-9-]+)*(\.[a-z0-9-]+)$', sub)

					if match != None:
						writer.writerow([sub])
					else:
						results.append(address)

		for test in results:
			match = re.search(r"'", test[0].lower())
			if match != None:
				writer.writerow(test)
			else:
				writer.writerow(["FIX THIS EMAIL: %r " % test])

		writer.writerow(["sean.mbogo@####.com"])
		writer.writerow(["c####.p####@####.com"])
		os.remove('trim_%s' % filename)

		print "Checker - Successfully completed!"

# This script simply checks whether the emails in the first file are present 
# in the Unreachables section 
def email_unreachable(filename, unreachables):
	with open(filename, 'rU') as email_list, open(unreachables, 'rU') as unreachables_list, \
	open(('UNREACHABLES_%s') % filename, 'w+') as output: 
		writer = csv.writer(output, delimiter=',')
		readCSV1 = email_list.readlines()
		readCSV2 = unreachables_list.readlines()

		for line in readCSV1:
			if line in readCSV2:
				writer.writerow([line])
	print "Unreachables - Successfully completed!"

# This script simply checks whether the emails in the first file are NOT present 
# in the Unreachables section 
def email_send(filename, unreachables):
	with open("customer_zaius_%s" % filename, 'rU') as email_list, open(unreachables, 'rU') as unreachables_list, \
	open(('SENT_EMAILS_%s') % filename, 'w+') as output: 
		writer = csv.writer(output, delimiter=',')
		readCSV1 = email_list.readlines()
		readCSV2 = unreachables_list.readlines()

		for line in readCSV1:
			if line not in readCSV2:
				writer.writerow([line])
	print "Sent - Successfully completed!"
main()



	
