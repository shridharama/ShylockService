# ShylockService
Backend service and analytics engine for the Shylock Clover app


cf push ShylockService

hosted at http://shylockservice.cfapps.io/api/v1.0

ex:
curl -i -H "Content-Type: application/json" -X POST -d '{"uuid":"100", "timestamp":"1477207066", "distance":"near","beacon_id":103}' http://shylockservice.cfapps.io/api/v1.0/pushBeaconEvent


