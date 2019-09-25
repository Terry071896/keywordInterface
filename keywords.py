import requests
class Keywords(object):

    def __init__(self, servers=None, keywords=None, mode='web'):

        if keywords is None:
            keywords = []
        if servers is None:
        	servers = []
        
        self._servers = servers
        self._keywords = keywords
        self._mode = mode

    def get_keyword(self):
    	counter = 0
    	keywordDict = dict()
    	for pname in self._keywords:
    		server = self._servers[counter]
    		keywordDict.update({pname : (self._find_keyword(server, pname))})
    		
    	return keywordDict

    def _find_keyword(self, server, keyword):
    	if self._mode == 'local':
    		proc = subprocess.Popen("show -terse -s %s %s " % (server, keyword), stdout=subprocess.PIPE, shell=True)
    		result = proc.communicate()
    	elif self._mode == 'ktlpython':
    		proc = ktl.cache(server, keyword)
    		result = proc.read()
    	elif self._mode == 'web':
    		url = 'http://localhost:5002/show?server=%s&keyword=%s' % (server, keyword)
    		try:
    			response = requests.get(url)
    		except requests.exceptions.RequestException as e:
    			print("Error in getting data from the server")
    			return
    		result = response.json()
    	elif self._mode == 'simulate':
    		return 164
    	return result
