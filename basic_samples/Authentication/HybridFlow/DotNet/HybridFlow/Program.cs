using System;
using System.Globalization;
using System.IO;
using System.Net.Http;
using System.Threading.Tasks;
using Microsoft.Extensions.Configuration;

namespace HybridFlow
{
    public static class Program
    {
        private static IConfiguration _configuration;

        public static void Main()
        {
            bool test = false;
            try
            {
                InitConfig();

                if (SystemBrowser.OpenBrowser == null)
                {
                    SystemBrowser.OpenBrowser = new OpenSystemBrowser();
                }
                else
                {
                    test = true;
                    SystemBrowser.Password = GetConfigValue("Password");
                    SystemBrowser.UserName = GetConfigValue("UserName");
                }

                Hybrid.OcsAddress = GetConfigValue("Resource");
                Hybrid.RedirectHost = GetConfigValue("RedirectHost");
                Hybrid.RedirectPort = int.Parse(GetConfigValue("RedirectPort"), CultureInfo.InvariantCulture);
                Hybrid.RedirectPath = GetConfigValue("RedirectPath");

                var tenantId = GetConfigValue("TenantId");
                var clientId = GetConfigValue("ClientId");
                var clientSecret = GetConfigValue("ClientKey");
                var ocsUrl = GetConfigValue("Resource");
                var apiVersion = GetConfigValue("ApiVersion");

                // Get access token and refresh token.
                var (accessToken, refreshToken, expiration) =
                    Hybrid.GetHybridFlowAccessToken(clientId, clientSecret, tenantId);
                Console.WriteLine("Access Token: " + accessToken);
                Console.WriteLine("Refresh Token: " + refreshToken);
                Console.WriteLine("Expires: " + expiration);

                // Make a request to Get Users endpoint
                var result1 = GetRequest($"{ocsUrl}/api/{apiVersion}/Tenants/{tenantId}/Users", accessToken).Result;
                Console.WriteLine(result1
                    ? "Request succeeded"
                    : "request failed");
                if (!result1)
                    throw new Exception("Request failed");

                // Get a new access token from a refresh token. If the previous access token has not expired it can still be used.
                // This will also reissue a new refresh token. Old refresh token will no longer be valid after use.
                (accessToken, refreshToken, expiration) =
                    Hybrid.GetAccessTokenFromRefreshToken(refreshToken, clientId, clientSecret);
                Console.WriteLine("Access Token: " + accessToken);
                Console.WriteLine("Refresh Token: " + refreshToken);
                Console.WriteLine("Expires: " + expiration);

                // Make a request to Get Users endpoint
                var result2 = GetRequest($"{ocsUrl}/api/{apiVersion}/Tenants/{tenantId}/Users", accessToken).Result;
                Console.WriteLine(result2
                    ? "Request succeeded"
                    : "request failed");
                if (!result2)
                    throw new Exception("Request failed");
            }
            catch (Exception e)
            {
                Console.WriteLine(e.ToString());
                if (test)
                    throw;
            }

            if (!test)
                Console.ReadLine();
        }

        private static async Task<bool> GetRequest(string endpoint, string accessToken)
        {
            Console.WriteLine("Make request:");
            using var request = new HttpRequestMessage()
            {
                Method = HttpMethod.Get,
                RequestUri = new Uri(endpoint),
            };

            // Attach  the access token to the Authorization header in the HTTP request.
            request.Headers.Authorization =
                new System.Net.Http.Headers.AuthenticationHeaderValue("Bearer", accessToken);

            try
            {
                using var client = new HttpClient();
                var response = await client.SendAsync(request).ConfigureAwait(false);
                response.EnsureSuccessStatusCode();

                // Uncomment this line to get the results of the calls
                // var responseBodyJson = JsonConvert.SerializeObject(response.Content.ReadAsStringAsync().Result, Formatting.Indented);
                // Console.WriteLine(responseBodyJson);
                return true;
            }
            catch (HttpRequestException)
            {
                return false;
            }
        }

        private static void InitConfig()
        {
            try
            {
                _configuration = new ConfigurationBuilder()
                    .AddJsonFile("appsettings.json", optional: false, reloadOnChange: false)
                    .Build();
            }
            catch (FileNotFoundException ex)
            {
                Console.WriteLine("Config file missing: " + ex);
                throw;
            }
            catch (Exception ex)
            {
                Console.WriteLine("Error while initiating configuration: " + ex.ToString());
                throw;
            }
        }

        private static string GetConfigValue(string key)
        {
            try
            {
                if (_configuration == null)
                {
                    Console.WriteLine("Config Null");
                    InitConfig();
                }

                var value = _configuration.GetValue<string>(key);

                if (value == null)
                {
                    Console.WriteLine($"Missing the value for \"{key}\" in config file");
                    throw new Exception($"Missing the value for \"{key}\" in config file");
                }

                return value;
            }
            catch
            {
                Console.WriteLine($"Configuration issue");
                throw;
            }
        }
    }
}
