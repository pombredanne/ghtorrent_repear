import collections
import sys
import os
import os as inner_os
from lib.core import Tokenizer
from lib.utilities import url_to_json
from gingerit.gingerit import GingerIt
from spellchecker import SpellChecker
import re
from comment_parser import comment_parser
QUERY = '''
SELECT name FROM projects WHERE id={0}
'''
def run(project_id, repo_path, cursor, **options):
    num_core_doc_msgs = 0
    totalNumberOfdocmsgs = 0
    cursor.execute(QUERY.format(project_id))
    repoName = cursor.fetchone()[0]
    os.chdir("path/"+str(project_id)+"/")
    stri = os.getcwd() 
    for repos in os.listdir():
        if(repos == repoName):
            os.chdir(repos)
            stream = []
            print("----- METRIC: DOCUMENTATION QUALITY -----")
            print('os path: ',os.getcwd())
            for (root,dirs,files) in inner_os.walk(os.getcwd(),topdown=True):
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
            for docs in stream:
                docs = str(docs).lower()
                trim_doc = re.sub("[^a-zA-Z ]+", "", docs)
                trim_doc = ' '.join(trim_doc.split())
                if(len(trim_doc) > 0):
                    totalNumberOfdocmsgs += 1
                # totalNumberOfdocmsgs += len(trim_doc.split())
                # spell = SpellChecker()
                # trim_doc = re.sub(r"\b[a-zA-Z]\b", "", trim_doc)
                # trim_doc = re.sub(r"\b[a-zA-Z][a-zA-Z]\b", "", trim_doc)
                ginger_parser = GingerIt()
                ginger_grammar_results = ginger_parser.parse(trim_doc)
                ginger_corrections = ginger_grammar_results['corrections']
                if(len(ginger_corrections) == 0):
                    num_core_doc_msgs += 1 
                # trim_doc = trim_doc.split()
                # spelled = spell.known(trim_doc)
                #num_core_doc_msgs += len(spelled)
            docs_ratio = 0
            if(totalNumberOfdocmsgs > 0):
                docs_ratio = float(num_core_doc_msgs)/float(totalNumberOfdocmsgs*1.0)
                print('documentation ratio: ',docs_ratio)
            break
    threshold = options['threshold']
    return (docs_ratio >= threshold, docs_ratio)
if __name__ == '__main__':
    print('Attribute plugins are not meant to be executed directly.')
    sys.exit(1)
