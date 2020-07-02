import sys
import os
from attributes.unit_test.discoverer import get_test_discoverer


def run(project_id, repo_path, cursor, **options):
    print("----- METRIC: UNIT TEST -----")
    query = 'SELECT language FROM projects WHERE id = %d' % project_id
    cursor.execute(query)
    # print('current_unit_test_directory: ',os.getcwd())
    repo_path_abs = str(os.getcwd()) + "\\" +repo_path
    #print('repo_path_unit_test: ',repo_path_abs)
    record = cursor.fetchone()
    # print('lan_unit_test: ',record[0])
    discoverer = get_test_discoverer(language=record[0])
    # print('discoverer_unit_test: ',discoverer)
    proportion = discoverer.discover(repo_path_abs)

    threshold = options['threshold']
    print('proportion: ',proportion)
    return (proportion >= threshold), proportion

if __name__ == '__main__':
    print('Attribute plugins are not meant to be executed directly.')
    sys.exit(1)
