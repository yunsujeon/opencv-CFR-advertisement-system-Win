import os
import sys
import requests

import json

##### Using Open API(Clova Face Recognition)
client_id = "pg4aIiYkw9LxJOpcOTzT"
client_secret = "HhKvPRFr8P"
url = "https://openapi.naver.com/v1/vision/face" # face recognition

files = {'image': open('1.jpeg', 'rb')}
headers = {'X-Naver-Client-Id': client_id, 'X-Naver-Client-Secret': client_secret }
response = requests.post(url,  files=files, headers=headers)
rescode = response.status_code

### get information part
facegender = []
faceage = []

if(rescode==200):
    #print (response.text)		# get ALL information
    data = json.loads(response.text)		#get some information
    
    faceCount = data['info']['faceCount']		#get number of people

    for i in data['faces']:	# get people's gender and age
    	facegender.append(i['gender']['value'])
    	faceage.append(i['age']['value'])
    
else:
    print("Error Code:" + str(rescode))

# check information
print faceCount
for i in range(faceCount):
	print facegender[i], faceage[i]

# get average age of each person
average_age = []
for i in range(faceCount):
	average_age.append(int(faceage[i][0] + faceage[i][1]) + 2) 
	print average_age[i]

male = [0,0,0,0,0,0,0,0,0]
female = [0,0,0,0,0,0,0,0,0]

# classify
for i in range(faceCount):
	if facegender[i] == "male":
		if 0 < average_age[i] < 10:
			male[0] += 1
		elif 10 <= average_age[i] < 20:
			male[1] += 1
		elif 20 <= average_age[i] < 30:
			male[2] += 1
		elif 30 <= average_age[i] < 40:
			male[3] += 1			
		elif 40 <= average_age[i] < 50:
			male[4] += 1
		elif 50 <= average_age[i] < 60:
			male[5] += 1
		elif 60 <= average_age[i] < 70:
			male[6] += 1
		elif 70 <= average_age[i] < 80:
			male[7] += 1			
	else:
		if 1 <= average_age[i] < 10:
			female[0] += 1
		elif 10 <= average_age[i] < 20:
			female[1] += 1
		elif 20 <= average_age[i] < 30:
			female[2] += 1
		elif 30 <= average_age[i] < 40:
			female[3] += 1			
		elif 40 <= average_age[i] < 50:
			female[4] += 1
		elif 50 <= average_age[i] < 60:
			female[5] += 1
		elif 60 <= average_age[i] < 70:
			female[6] += 1
		elif 70 <= average_age[i] < 80:
			female[7] += 1

print male
print female

max_male = 0
max_female = 0

for i in range(8):
	if max(male) != 0:
		if male[i] == max(male):
			max_male = i
	else:
		max_male = -1

	if max(female) != 0:
		if female[i] == max(female):
			max_female = i
	else:
		max_female = -1

print sum(male), sum(female)
print max_male, max_female