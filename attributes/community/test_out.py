# def isEnglish(s):
#     try:
#         s.encode(encoding='utf-8').decode('ascii')
#         print(s)
#     except UnicodeDecodeError:
#         return False
#     else:
#        
#  return True
def removeNonAscii(s): return "".join(i for i in s if ord(i)<128)
# import re
# w = "1 静かな美男"
# english_check = re.compile(r'[a-z]')

# if english_check.match(w):
#     print("english",w)
# else:
#     w = w.split(" ")[0]
#     print("other:",w)
w = "1 静かな美男"
print(removeNonAscii(w))