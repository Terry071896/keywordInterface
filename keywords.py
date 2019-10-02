import requests
import datetime
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

    		#print(pname)
    		if pname[0:6] == 'uptime':
    			pname = pname[0:6]
    			if self._server_up(server, pname):
    				keywordDict.update({pname+server : '1'})
    			else:
    				keywordDict.update({pname+server : '0'})
    		elif pname == 'TESTINT':
    			if self._server_up(server, pname[:-1]):
    				keywordDict.update({pname : '1'})
    			else:
    				keywordDict.update({pname : '0'})
    		else:
    			keywordDict.update({pname : self._find_keyword(server, pname[:-1])})
    		counter += 1
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

    		result = response.json()
    	elif self._mode == 'simulate':
    		return 164
    	return result

    def _server_up(self, server, keyword):
    	try:
    		temp = self._find_keyword(server, keyword)
    		return True
    	except:
    		return False

    def get_keyword_history(self, server, keyword, time):
        data = {'x' : [], 'y' : []}
        if(self._server_up(server, keyword)):
            url = 'http://localhost:5002/showHistory?server=%s&keyword=%s&time=%s' % (server, keyword, time)
            try:
                response = requests.get(url)
            except requests.exceptions.RequestException as e:
                print("Error in getting data from the server")
                return data
            result = response.json()
            if(result[:6] == 'unable'):
                return data

            for row in result.split("\\n"):
                if row[0] == "#":
                    return data
                x, y = row.split(" ")
                x = datetime.datetime.strptime(x, '%Y-%m-%dT%H:%M:%S.%f')
                data["x"].append(x)
                data['y'].append(float(y))
        return data
