import re

list = "1 hour 45 minutes"
result = int(re.findall('(\d+) minutes',list)[0])
print(type(result))
print(result)