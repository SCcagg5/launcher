from Model.service import *

def setuproute(app, call):
    @app.route('/',                     ['OPTIONS', 'POST', 'GET'],   lambda x = None: call([])                                           )
    @app.route('/service/<>',    	    ['OPTIONS', 'GET'],           lambda x = None: call([service_exist, service_infos])               )
    @app.route('/service/<>',    	    ['OPTIONS', 'POST'],          lambda x = None: call([service_exist, service_new])               )
    @app.route('/setup/<>',    	        ['OPTIONS', 'GET'],           lambda x = None: call([service_setup_infos]) )
    def base():
        return
