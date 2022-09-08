import requests
import json
import io
import time

#config section
token =  "" #ApiToken xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
console_url = "" #https://usea1-xxxxxxx.sentinelone.net
output_path = "c:\\S1_export" #folder to write the file to
output_file_name = "blacklist_%DATE%" #Output file name - token %DATE% will be replaced by today's date
output_extension = ".csv" #Output file extension
#end config section

strApiURL = console_url + "/web/api/v2.1/restrictions?limit=100&includeChildren=True&includeParents=True"

now = datetime.now() # current date and time
date_string = now.strftime("%Y-%m-%d") #today's date
output_file_name = output_file_name.replace("%DATE%", date_string) #replace token
output_path = output_path + "\\" + output_file_name + output_extension #build output path

def logToFile(strfilePathOut, strDataToLog, boolDeleteFile, strWriteMode):
    with open(strfilePathOut, strWriteMode, encoding="utf-8") as target:
      if boolDeleteFile == True:
        target.truncate()
      target.write(strDataToLog + "\n")

def append_csv(strAggregate, strAdd):
    if strAggregate == "":
        strAggregate = strAdd
    elif strAdd is None:
        strAggregate = strAggregate + ","
    else:
        strAggregate = strAggregate + "," + strAdd.replace("\"","\"\"\"")
    return strAggregate

def process_restrictions(restriction_list):

  for restriction in restriction_list:
    csv_row = restriction['createdAt']
    csv_row = append_csv(csv_row, restriction['description'])
    csv_row = append_csv(csv_row, restriction['osType'])
    csv_row = append_csv(csv_row, restriction['scopeName'])
    csv_row = append_csv(csv_row, restriction['scopePath'])
    csv_row = append_csv(csv_row, restriction['source'])
    csv_row = append_csv(csv_row, restriction['updatedAt'])
    csv_row = append_csv(csv_row, restriction['value'])
    logToFile(output_path,csv_row,False,'a')


response = requests.get(strApiURL, headers={'Authorization':token}, verify=False)
blacklist = json.loads(response.content.decode('utf8'))

header = 'createdAt'
header = append_csv(header,'description')
header = append_csv(header,'osType')
header = append_csv(header,'scopeName')
header = append_csv(header,'scopePath')
header = append_csv(header,'source')
header = append_csv(header,'updatedAt')
header = append_csv(header,'value')
logToFile(output_path,header,True,'w')

process_restrictions(blacklist["data"])
while 'nextCursor' in blacklist['pagination']:
  next_cursor = blacklist['pagination']['nextCursor']
  time.sleep(1.0)
  if next_cursor == None:
    print("done")
    break
  response = requests.get(strApiURL + "&cursor=" + next_cursor, headers={'Authorization':token}, verify=False)
  blacklist = json.loads(response.content.decode('utf8'))
  process_restrictions(blacklist["data"])
