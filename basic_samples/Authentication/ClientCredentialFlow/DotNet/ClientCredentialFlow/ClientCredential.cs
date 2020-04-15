using System;
using System.Net.Http;
using OSIsoft.Identity;

namespace ClientCredentialFlow
{
    public static class ClientCredential
    {
        public static Uri OcsUri { get; set; }

        public static HttpClient AuthenticatedHttpClient { get; set; }

        private static AuthenticationHandler AuthenticationHandler { get; set; }

        public static void CreateAuthenticatedHttpClient(string clientId, string clientSecret)
        {
            Console.WriteLine(Resources.SignInWithClientCredentials);
            Console.WriteLine();

            AuthenticationHandler = InitiateAuthenticationHandler(clientId, clientSecret);
            AuthenticatedHttpClient = new HttpClient(AuthenticationHandler)
            {
                BaseAddress = OcsUri,
            };
        }

        private static AuthenticationHandler InitiateAuthenticationHandler(string clientId, string clientSecret)
        {
            // Create an instance of the AuthenticationHandler.
            return new AuthenticationHandler(OcsUri, clientId, clientSecret)
            {
                InnerHandler = new HttpClientHandler()
                {
                    AllowAutoRedirect = false,
                },
            };
        }
    }
}
