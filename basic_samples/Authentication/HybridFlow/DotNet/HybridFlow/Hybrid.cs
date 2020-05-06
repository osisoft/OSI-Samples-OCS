using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Threading.Tasks;
using IdentityModel.Client;
using IdentityModel.OidcClient;

namespace HybridFlow
{
    public static class Hybrid
    {
        /// <summary>
        /// Identity resource suffix.
        /// </summary>
        private const string IdentityResourceSuffix = "/identity";
        private static OidcClient _oidcClient;
        public static string OcsAddress { get; set; }

        public static string RedirectHost { get; set; }

        public static int RedirectPort { get; set; }

        public static string RedirectPath { get; set; }

        private static string OcsIdentityUrl
        {
            get { return OcsAddress + IdentityResourceSuffix; }
        }

        public static (string, string, DateTime) GetHybridFlowAccessToken(string clientId, string clientSecret,
            string tenantId)
        {
            Console.WriteLine("+-----------------------+");
            Console.WriteLine("|  Sign in with OIDC    |");
            Console.WriteLine("+-----------------------+");
            Console.WriteLine();

            LoginResult loginResult = null;
            do
            {
                if (loginResult != null)
                {
                    Console.WriteLine(loginResult.Error);
                    return (string.Empty, string.Empty, DateTime.Now);
                }

                Console.WriteLine("Prompting for login via a browser...");
                var scope = "openid ocsapi offline_access";
                loginResult = SignIn(clientId, clientSecret, scope, tenantId).Result;
            }
            while (loginResult.IsError);

            return (loginResult.AccessToken, loginResult.RefreshToken, loginResult.AccessTokenExpiration.ToLocalTime());
        }

        public static async void Logout()
        {
            await _oidcClient.LogoutAsync().ConfigureAwait(false);
        }

        public static (string, string, DateTime) GetAccessTokenFromRefreshToken(string refreshToken, string clientId,
            string clientSecret)
        {
            Console.WriteLine();
            Console.WriteLine("+-----------------------+");
            Console.WriteLine("|  Getting Access token from Refresh token    |");
            Console.WriteLine("+-----------------------+");
            Console.WriteLine();

            return RefreshTokenAsync(refreshToken, clientId, clientSecret).Result;
        }

        private static async Task<ProviderInformation> GetProviderInformation()
        {
            // Discover endpoints from metadata.
            using HttpClient client = new HttpClient();

            // Create a discovery request
            var discoveryDocumentRequest = new DiscoveryDocumentRequest
            {
                Address = OcsIdentityUrl,
                Policy = new DiscoveryPolicy
                {
                    ValidateIssuerName = false,
                },
            };

            var discoveryResponse =
                await client.GetDiscoveryDocumentAsync(discoveryDocumentRequest).ConfigureAwait(false);

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
                        discoveryResponse.TokenEndpointAuthenticationMethodsSupported,
                };
        }

        private static async Task<LoginResult> SignIn(string clientId, string clientSecret, string scope,
            string tenantId)
        {
            // create a redirect URI using an available port on the loopback address.
            // requires the OP to allow random ports on 127.0.0.1 - otherwise set a static port
            var browser = new SystemBrowser(RedirectPort);
            var redirectUri = $"{RedirectHost}:{browser.Port}/{RedirectPath}";
            try
            {
                // Create the OICD client Options
                var options = new OidcClientOptions
                {
                    Authority = OcsIdentityUrl,
                    ClientId = clientId,
                    ClientSecret = clientSecret,
                    RedirectUri = redirectUri,
                    Scope = scope,
                    FilterClaims = false,
                    Flow = OidcClientOptions.AuthenticationFlow.Hybrid,
                    Browser = browser,
                    Policy = new Policy
                    {
                        Discovery = new DiscoveryPolicy
                        {
                            ValidateIssuerName = false,
                        },
                    },
                };

                _oidcClient = new OidcClient(options);
                var loginRequest = new LoginRequest
                {
                    FrontChannelExtraParameters = new Dictionary<string, string> { { "acr_values", $"tenant:{tenantId}" } },
                };

                // Login with the client. This call will open a new tab in your default browser
                return await _oidcClient.LoginAsync(loginRequest).ConfigureAwait(false);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error while logging in: {ex}");
                throw;
            }
        }

        private static async Task<(string, string, DateTime)> RefreshTokenAsync(string refreshToken, string clientId,
            string clientSecret)
        {
            if (string.IsNullOrEmpty(refreshToken))
            {
                Console.WriteLine("No refresh token provided");
            }

            Console.WriteLine($"Using refresh token: {refreshToken}");

            // Get provider information manually
            var provider = await GetProviderInformation().ConfigureAwait(false);

            // Make a refresh token request. This will issue new access and refresh tokens.
            using var tokenClient = new HttpClient();
            var refreshRequest = new RefreshTokenRequest
            {
                Address = provider.TokenEndpoint,
                ClientId = clientId,
                ClientSecret = clientSecret,
                RefreshToken = refreshToken,
            };
            var response = await tokenClient.RequestRefreshTokenAsync(refreshRequest).ConfigureAwait(false);

            if (response.IsError)
            {
                Console.WriteLine("Error while getting the refresh token: " + response.Error);
                return (string.Empty, string.Empty, DateTime.Now);
            }

            return (response.AccessToken, response.RefreshToken,
                DateTime.Now.AddSeconds(response.ExpiresIn).ToLocalTime());
        }
    }
}
