section OCSConnector_Sample;

// Tenant-Specific Values
tenant_id = Text.FromBinary(Extension.Contents("tenant_id"));

// Note: Client ID should be an Authorization Code Client with the below redirect_uri and logout_uri
client_id = Text.FromBinary(Extension.Contents("client_id"));

// OCS values
resource = Text.FromBinary(Extension.Contents("url"));
authorize_uri = Text.Combine({resource, "identity/connect/authorize"}); 
token_uri = Text.Combine({resource, "identity/connect/token"});
scope = "ocsapi";

// OAuth values for PowerBI
redirect_uri = "https://oauth.powerbi.com/views/oauthredirect.html";
logout_uri = "https://login.microsoftonline.com/logout.srf";

// Authorization Code + PKCE verifier/challenge
code_verifier = Base64Encode(GenerateRandomBytes(32));
// Note: Crypto and CryptoAlgorithm are not documented and can only be used inside Custom Data Connectors
code_challenge = Base64Encode(Crypto.CreateHash(CryptoAlgorithm.SHA256, Text.ToBinary(code_verifier, TextEncoding.Ascii)));

// Crypto functions for Authorization Code + PKCE
GenerateRandomBytes = (count as number) =>
    let
        RandomBit = () => Number.Round(Number.RandomBetween(0, 255)),
        list = List.Generate(()=> [ x = RandomBit(), y = {}] , each List.Count([y]) < count, each [x = RandomBit(), y = [y] & {x}] , each [x]),
        binary = Binary.FromList(list)
    in
        binary;

Base64Encode = (str as binary) =>
    let
        unescaped = Binary.ToText(str, BinaryEncoding.Base64),
        text = Text.Replace(Text.Replace(Text.Replace(unescaped, "+", "-"), "/", "_"), "=", "")
    in
        text;
        
// Login modal window dimensions
windowWidth = 720;
windowHeight = 1024;

[DataSource.Kind="OCSConnector_Sample", Publish="OCSConnector_Sample.Publish"]
shared OCSConnector_Sample.Contents = Value.ReplaceType(OCSConnectorImpl, OCSConnectorType);

OCSConnectorType = type function(
    url as (Uri.Type meta [
        Documentation.FieldCaption = "OSIsoft Cloud Services API Path",
        Documentation.FieldDescription = "OSIsoft Cloud Services API path and parameters",
        Documentation.SampleValues = {"https://dat-b.osisoft.com/api/v1/Tenants/{tenantId}/Namespaces"}
    ]),
    optional timeout as (type number meta [
        Documentation.FieldCaption = "Timeout",
        Documentation.FieldDescription = "Timeout in seconds for API request",
        Documentation.SampleValues = {100}
    ])) as binary meta [
        Documentation.LongDescription = "Raw data returned from API, usually JSON or CSV",
        Documentation.Name = "OSIsoft Cloud Services API Request"
    ];

OCSConnectorImpl = (url as text, optional timeout as number) =>
    let
        url = url,
        source = if timeout = null
        then Web.Contents(url)
        else Web.Contents(url, [ Headers = [#"Request-Timeout" = Number.ToText(timeout)], Timeout = #duration(0,0,0,timeout)])
    in
        source;

// Data Source Kind description
OCSConnector_Sample = [
    TestConnection = (dataSourcePath) => { "OCSConnector_Sample.Contents", dataSourcePath },
    Authentication = [
        OAuth = [
            StartLogin = StartLogin,
            FinishLogin = FinishLogin,
            Logout = Logout
        ]
    ],
    Label = Extension.LoadString("DataSourceLabel")
];

// Helper functions for OAuth2: StartLogin, FinishLogin, Refresh, Logout

// Authorization Request, see https://www.oauth.com/oauth2-servers/pkce/authorization-request/
StartLogin = (dataSourcePath, state, display) =>
    let
        authorizeUrl = authorize_uri & "?" & Uri.BuildQueryString([
            client_id = client_id, 
            redirect_uri = redirect_uri, 
            scope = scope,
            response_type = "code",
            code_challenge = code_challenge,
            code_challenge_method = "S256",
			acr_values = "tenant:" & tenant_id
        ])
    in
        [
            LoginUri = authorizeUrl,
            CallbackUri = redirect_uri,
            WindowHeight = windowWidth,
            WindowWidth = windowHeight,
            Context = null
        ];

// Extracts access_token from callbackUri
FinishLogin = (context, callbackUri, state) =>
    let
        // Parse the callbackUri and extract the Query string
        parts = Uri.Parts(callbackUri)[Query],
        // If the query string contains an "error" field, raise an error
        // Otherwise call TokenMethod to exchange our code for an access_token
        result = if Record.HasFields(parts, {"error", "error_description"}) then 
                    error Error.Record(parts[error], parts[error_description], parts)
                 else
                    TokenMethod("authorization_code", "code", parts[code])
    in
        result;

Logout = (accessToken) => logout_uri;

// Authorization Code Exchange, see https://www.oauth.com/oauth2-servers/pkce/authorization-code-exchange/
TokenMethod = (grantType, tokenField, code) =>
    let
        queryString = [
            grant_type = "authorization_code",
            redirect_uri = redirect_uri,
            client_id = client_id,
            code_verifier = code_verifier
        ],
        queryWithCode = Record.AddField(queryString, tokenField, code),

        tokenResponse = Web.Contents(token_uri, [
            Content = Text.ToBinary(Uri.BuildQueryString(queryWithCode)),
            Headers = [
                #"Content-type" = "application/x-www-form-urlencoded",
                #"Accept" = "application/json"
            ],
            ManualStatusHandling = {400} 
        ]),
        body = Json.Document(tokenResponse),
        result = if (Record.HasFields(body, {"error", "error_description"})) then 
                    error Error.Record(body[error], body[error_description], body)
                 else
                    body
    in
        result;

// Data Source UI publishing description
OCSConnector_Sample.Publish = [
    Beta = true,
    Category = "Online Services",
    ButtonText = { Extension.LoadString("ButtonTitle"), Extension.LoadString("ButtonHelp") },
    LearnMoreUrl = "https://powerbi.microsoft.com/",
    SourceImage = OCSConnector_Sample.Icons,
    SourceTypeImage = OCSConnector_Sample.Icons
];

OCSConnector_Sample.Icons = [
    Icon16 = { Extension.Contents("OCSConnector_Sample16.png"), Extension.Contents("OCSConnector_Sample20.png"), Extension.Contents("OCSConnector_Sample24.png"), Extension.Contents("OCSConnector_Sample32.png") },
    Icon32 = { Extension.Contents("OCSConnector_Sample32.png"), Extension.Contents("OCSConnector_Sample40.png"), Extension.Contents("OCSConnector_Sample48.png"), Extension.Contents("OCSConnector_Sample64.png") }
];
