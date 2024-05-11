#Spazer tool for processing web pages

from bs4 import BeautifulSoup
import os, csv, re, pathlib

from thefuzz import fuzz, process

#Variables to track the input, output and gained space
space_gained = 0
space_input = 0
space_output = 0

print("Welcome to Spazer\n")

city_distr_list = []
file_path = os.path.dirname(__file__)

file1 = open(file_path+"\\india_cities.csv")
csv_reader = csv.reader(file1)
for row in csv_reader:
    for v in row:
        city_distr_list.append(v)
file1.close()

file1 = open(file_path+"\\india_districts.csv")
csv_reader = csv.reader(file1)
for row in csv_reader:
    for v in row:
        city_distr_list.append(v)
file1.close()

PINCODE = r'(\b\d{3}\s?\d{3}\b)|(\b\d{2}\b)'

ADDRESS_KEYWORDS = ['floor', 'building', 'block', 'no.', 'avenue', 'annexe', 'road', 'tower', 'sector', 'plot', 'phase', 'gate', 'junction',
                    'street', 'lane', 'flat', 'complex', 'colony']


for x in range(5):
    filename = str(x) + ".html"
    file = pathlib.Path('input/' + filename)
    if (file.exists()):

        #Read each file
        print("Reading " + filename)
        f = open('input/' + filename, 'r', errors="ignore")
        contents = f.read()   
        
        #Remove html tags
        soup = BeautifulSoup(contents, 'lxml')        
        output = soup.get_text() 
       
        #Your code begins  ###############################

        output_words = []
        output_lines = output.splitlines()
        for line in output_lines:
            for word in line.split(' '):
                for w in word.split('-'):
                    if w != "":
                        output_words.append(w)

        addresses = []


        for i in range(len(output_words)):
            for w1 in output_words[i].split('.'):
                for w2 in w1.split(','):
                    if w2 != '' and w2 in city_distr_list:
                        extracted_text = " ".join(output_words[i-12 : i+5])
                        if extracted_text != "":
                            c = extracted_text.index(output_words[i])
                            matches = re.findall(PINCODE, extracted_text[c:])
                            if matches:
                                addresses.append(extracted_text)
    
                            else:
                                s = extracted_text[:c].lower()
                                result = any(k in s for k in ADDRESS_KEYWORDS)
                                if result:
                                    addresses.append(extracted_text)
                            
                    else:
                        flag = False
                        for place in city_distr_list:
                            if place in w2:
                                extracted_text = " ".join(output_words[i-15 : i+5])
                                if extracted_text != "":
                                    c = extracted_text.index(output_words[i])
                                    matches = re.findall(PINCODE, extracted_text[c:])
                                    if matches:
                                        addresses.append(extracted_text)
                                        flag = True
                                    
                            if flag:
                                break

        
        final_addresses = []
        for i in range(len(addresses)-1):
            if fuzz.ratio(addresses[i], addresses[i+1]) < 90:
                final_addresses.append(addresses[i])
        final_addresses.append(addresses[-1])

        output = "\n\n".join(final_addresses)
        print(output)


        #Your code ends  #################################              
        
        #Write the output variable contents to output/ folder.
        print ("Writing reduced " + filename)
        fw = open('output/' + filename, "w")
        fw.write(output)
        fw.close()
        f.close()
        
        #Calculate space savings
        space_input = space_input + len(contents)
        space_output = space_output + len(output)
        
space_gained = round((space_input - space_output) * 100 / space_input, 2)

print("\nTotal Space used by input files = " + str(space_input) + " characters.") 
print("Total Space used by output files = " + str(space_output) + " characters.")
print("Total Space Gained = " + str(space_gained) + "%") 
       
    




