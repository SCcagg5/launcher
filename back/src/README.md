    
```pyhton
    @app.route('/',                     ['OPTIONS', 'POST', 'GET'])
    @app.route('/service/<>',           ['OPTIONS', 'GET']        )
    @app.route('/service/<>',           ['OPTIONS', 'POST']       )
    @app.route('/setup/<>',             ['OPTIONS', 'GET']        )
```
