__author__ = 'root'
#! /usr/bin/env python
import subprocess
import main
#returncode=subprocess.call("ls -l",shell=True)
a=subprocess.call(["/root/shell/test.sh","sh test.sh"],stdout=None,shell=True)
result=subprocess.Popen(["/root/shell/test.sh","sh test.sh"],stdout=subprocess.PIPE)
code=result.communicate()
#print code

conf=main.read_no_conf("/usr/local/nginx/conf/nginx.conf")
main.nginx_update(conf,"MainArgs|||worker_processes|||3")
main.dumpf(conf,"/usr/local/nginx/conf/nginx.conf")