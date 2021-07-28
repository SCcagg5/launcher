
routes:
 
```pyhton
    @app.route('/',                     ['OPTIONS', 'POST', 'GET'])
    @app.route('/service/<service>',           ['OPTIONS', 'GET']        )
    @app.route('/service/<service>',           ['OPTIONS', 'POST']       )
    @app.route('/setup/<setup_id>',             ['OPTIONS', 'GET']        )
```

service list:

```json
["wordpress"]
```

examples:

```
curl --location --request POST 'localhost:8081/service/wordpress' \
--header 'Content-Type: application/json' \
--data-raw '{
    "variables": { "domain_name": "test"},
    "options": {}
}'
```
