import random


class FakeKeywordValues(object):

    def __init__(self, process_names=None):

        if process_names is None:
            process_names = []

        self._process_names = process_names

    def get_data(self):
        return {
            pname: self._sample_data(pname) for pname in self._process_names
        }

    def _sample_data(self, process_name):
    	if process_name[1:6] == 'RANGE':
    		return random.randint(0,2)	
    	else:
    		return random.randint(0,1)
