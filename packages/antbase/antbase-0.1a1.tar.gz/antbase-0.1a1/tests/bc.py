import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from antbase.base.bc import Bc

def test_bc():
    Bc.print_project_list()
    print('Test Bc has been stopped.')

