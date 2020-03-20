using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Threading.Tasks;
using IdentityModel.Client;
using IdentityModel.OidcClient;

namespace AuthorizationCodeFlow
{
    public static class AuthorizationCodeFlow
    {
        private static OidcClient _oidcClient;
        private static string _ocsIdentityUrl;
        private static string _redirectHost;
        private static int _redirectPort;
        private static string _redirectPath;

        public static string OcsUrl
        {
            set => _ocsIdentityUrl = value + IdentityResourceSuffix;
        }

        public static string RedirectHost
        {
            set => _redirectHost = value;
        }

        public static int RedirectPort
        {
            set => _redirectPort = value;
        }

        public static string RedirectPath
        {
            set => _redirectPath = value;
        }

        /// <summary>
        /// Identity resource suffix.
        /// </summary>
        private const string IdentityResourceSuffix = "/identity";

        public static (string, DateTime) GetAuthorizationCodeFlowAccessToken(string clientId, string tenantId)
        {
            Console.WriteLine("+-----------------------+");
            Console.WriteLine("|  Sign in with OIDC    |");
            Console.WriteLine("+-----------------------+");
            Console.WriteLine("");

            LoginResult loginResult = null;
            do
            {
                if (loginResult != null)
                {
                    Console.WriteLine(loginResult.Error);
                    return (string.Empty, DateTime.Now);
                }

                Console.WriteLine("Prompting for login via a browser...");
                var scope = "openid ocsapi";
                loginResult = SignIn(clientId, scope, tenantId).Result;
            } while (loginResult.IsError);


            return (loginResult.AccessToken, loginResult.AccessTokenExpiration.ToLocalTime());
        }

        private static async Task<ProviderInformation> GetProviderInformation()
        {
            // Discover endpoints from metadata.
            using (HttpClient client = new HttpClient())
            {
                // Create a discovery request
                var discoveryDocumentRequest = new DiscoveryDocumentRequest
                {
                    Address = _ocsIdentityUrl,
                    Policy = new DiscoveryPolicy
                    {
                        ValidateIssuerName = false
                    }
                };

                var discoveryResponse =
                    await client.GetDiscoveryDocumentAsync(discoveryDocumentRequest);

                return discoveryResponse.IsError
                    ? throw new Exception($"Error while getting the discovery document: {discoveryResponse.Error}")
                    : new ProviderInformation()
                    {
                        IssuerName = discoveryResponse.Issuer,
                        KeySet = discoveryResponse.KeySet,
                        AuthorizeEndpoint = discoveryResponse.AuthorizeEndpoint,
                        TokenEndpoint = discoveryResponse.TokenEndpoint,
                        EndSessionEndpoint = discoveryResponse.EndSessionEndpoint,
                        UserInfoEndpoint = discoveryResponse.UserInfoEndpoint,
                        TokenEndPointAuthenticationMethods =
                            discoveryResponse.TokenEndpointAuthenticationMethodsSupported
                    };
            }
        }

        private static async Task<LoginResult> SignIn(string clientId, string scope, string tenantId)
        {
            // create a redirect URI using an available port on the loopback address.
            // requires the OP to allow random ports on 127.0.0.1 - otherwise set a static port
            var browser = new SystemBrowser(_redirectPort);
            var redirectUri = string.Format($"{_redirectHost}:{browser.Port}/{_redirectPath}");
            try
            {
                // Create the OICD client Options
                var options = new OidcClientOptions
                {
                    Authority = _ocsIdentityUrl,
                    ClientId = clientId,
                    RedirectUri = redirectUri,
                    Scope = scope,
                    FilterClaims = false,
                    Flow = OidcClientOptions.AuthenticationFlow.AuthorizationCode,
                    Browser = browser,
                    Policy = new Policy
                    {
                        Discovery = new DiscoveryPolicy
                        {
                            ValidateIssuerName = false
                        }
                    },
                };

                _oidcClient = new OidcClient(options);
                var loginRequest = new LoginRequest
                {
                    FrontChannelExtraParameters = new Dictionary<string, string>{{"acr_values", $"tenant:{tenantId}"}}
                };

                // Login with the client. This call will open a new tab in your default browser
                return await _oidcClient.LoginAsync(loginRequest);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error while logging in: {ex}");
                throw ex;
            }
        }

        public static async void Logout()
        {
            await _oidcClient.LogoutAsync();
        }
    }
}
