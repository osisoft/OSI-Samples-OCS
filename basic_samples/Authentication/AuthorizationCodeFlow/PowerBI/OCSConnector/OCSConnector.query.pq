// Use this file to write queries to test your data connector
let
    result = OCSConnector_Sample.Contents("https://dat-b.osisoft.com/api/v1/Tenants/{REPLACE_WITH_TENANT_ID}/Namespaces")
in
    result