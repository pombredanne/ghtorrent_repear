from comment_parser import comment_parser
import language_check 
import os
stream = []
for (root,dirs,files) in os.walk(os.getcwd(),topdown=True):
    for fi in files:
        if(fi.endswith('.py')):
            stream += comment_parser.extract_comments(os.path.join(root,fi),mime='text/x-python')
        elif(fi.endswith('.rb')):
            stream += comment_parser.extract_comments(os.path.join(root,fi),mime='text/x-ruby')
        elif(fi.endswith('.c')):
            stream += comment_parser.extract_comments(os.path.join(root,fi),mime='text/x-c')
        elif(fi.endswith('.cpp')):
            stream += comment_parser.extract_comments(os.path.join(root,fi),mime='text/x-c++')
        elif(fi.endswith('.go')):
            stream += comment_parser.extract_comments(os.path.join(root,fi),mime='text/x-go')
        elif(fi.endswith('.html')):
            stream += comment_parser.extract_comments(os.path.join(root,fi),mime='text/html')
        elif(fi.endswith('.java')):
            stream += comment_parser.extract_comments(os.path.join(root,fi),mime='text/x-java-source')
        elif(fi.endswith('.js')):
            stream += comment_parser.extract_comments(os.path.join(root,fi),mime='application/javascript')
        elif(fi.endswith('.sh')):
            stream += comment_parser.extract_comments(os.path.join(root,fi),mime='text/x-shellscript')
        elif(fi.endswith('.xml')):
            stream += comment_parser.extract_comments(os.path.join(root,fi),mime='text/xml')
tool = language_check.LanguageTool('en-US') 
i = 0
for line in stream: 
    matches = tool.check(line) 
    i = i + len(matches)      
    pass
print("No. of mistakes found in document is ", i) 
print() 
for mistake in matches: 
    print(mistake) 
    print() 