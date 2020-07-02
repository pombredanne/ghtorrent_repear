import collections
from lib import utilities
import sys
import os
import os as inner_os
from lib.core import Tokenizer
from lib.utilities import url_to_json
from spellchecker import SpellChecker
import re
from comment_parser import comment_parser
QUERY = '''
SELECT name FROM projects WHERE id={0}
'''
def run(project_id, repo_path, cursor, **options):
    num_core_doc_words = 0
    totalNumberOfdocWords = 0
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
                totalNumberOfdocWords += len(trim_doc.split())
                spell = SpellChecker()
                trim_doc = re.sub(r"\b[a-zA-Z]\b", "", trim_doc)
                trim_doc = re.sub(r"\b[a-zA-Z][a-zA-Z]\b", "", trim_doc)
                trim_doc = trim_doc.split()
                spelled = spell.known(trim_doc)
                num_core_doc_words += len(spelled)
            docs_ratio = 0
            if(totalNumberOfdocWords > 0):
                docs_ratio = float(num_core_doc_words)/float(totalNumberOfdocWords*1.0)
                #print('documentation ratio: ',docs_ratio)
            break
    ratio = 0

    # Dictionary of language => metrics dictionary
    util = utilities.get_loc(stri)

    sloc = 0
    cloc = 0
    for lang, metrics in util.items():
        sloc += metrics['sloc']
        cloc += metrics['cloc']

    if sloc == 0:   # No source code
        return False, ratio

    t_loc = sloc + cloc
    ratio = (cloc / t_loc) if t_loc > 0 else 0
    ratio = ratio*docs_ratio
    attr_threshold = options['threshold']
    print("----- METRIC: DOCUMENTATION -----")
    print('ratio: ',ratio)
    threshold = options['threshold']
    return (ratio >= threshold, ratio)
if __name__ == '__main__':
    print('Attribute plugins are not meant to be executed directly.')
    sys.exit(1)
