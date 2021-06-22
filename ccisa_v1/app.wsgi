#!/usr/bin/ccisa
import sys 

#!/usr/bin/python
#activate_this = '/var/www/ccisa/activate_this.py'
#with open(activate_this) as file_:
  #  exec(file_.read(), dict(__file__=activate_this))

sys.path.insert(0, '/var/www/ccisa')   
           
from ccisa import app as application
