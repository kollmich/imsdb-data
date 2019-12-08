import json

# read file
with open('data.txt', 'r') as myfile:
    data = json.load(myfile)

# import json
# with open('resultJSON.txt') as f:
#     json_data = json.load(f)

print(data[3]["subtitles"])#["title"])
