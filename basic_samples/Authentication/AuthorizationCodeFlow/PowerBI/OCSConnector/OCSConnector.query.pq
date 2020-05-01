// Use this file to write queries to test your data connector
let
    result = OCSConnector_Sample.Contents("https://dat-b.osisoft.com", "/api/v1/Tenants/{tenantId}/Namespaces", 100)
in
    result