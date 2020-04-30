// Use this file to write queries to test your data connector
let
    result = OCSConnector_Sample.Contents("https://dat-b.osisoft.com", "/api/v1/Tenants/d7847614-2e4a-4c1e-812b-e8de5fd06a0f/Namespaces", 100)
in
    result