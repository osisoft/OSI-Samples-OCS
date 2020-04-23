using System;
using System.IO;
using Microsoft.Extensions.Configuration;

namespace ClientCredentialFlow
{
    public static class Program
    {
        private static IConfiguration _configuration;

        public static void Main()
        {
            InitConfig();

            ClientCredential.OcsUri = new Uri(GetConfigValue("Resource"));

            var tenantId = GetConfigValue("TenantId");
            var clientId = GetConfigValue("ClientId");
            var clientSecret = GetConfigValue("ClientKey");
            var version = GetConfigValue("ApiVersion");
            ClientCredential.CreateAuthenticatedHttpClient(clientId, clientSecret);

            // Make an HTTP request to OCS using the authenticated client - since this is the first request, the AuthenticationHandler will
            // authenticate and acquire an Access Token and cache it.
            try
            {
                var uri = new Uri($"api/{version}/Tenants/{tenantId}/Users", UriKind.Relative);
                var response = ClientCredential.AuthenticatedHttpClient.GetAsync(uri).Result;
                response.EnsureSuccessStatusCode();
                Console.WriteLine(response.Content.ReadAsStringAsync().Result);
                Console.WriteLine($"HTTP GET api/{version}/Tenants/{tenantId}/Users successful");
            }
            catch (AggregateException ex)
            {
                foreach (var inEx in ex.Flatten().InnerExceptions)
                {
                    Console.WriteLine($"Authentication failed with the following error: {inEx.Message}");
                }

                throw;
            }

            // Make another request to OCS - this call should use the cached Access Token.
            try
            {
                var uri = new Uri($"api/{version}/Tenants/{tenantId}/Users", UriKind.Relative);
                var response = ClientCredential.AuthenticatedHttpClient.GetAsync(uri).Result;
                response.EnsureSuccessStatusCode();
                Console.WriteLine($"HTTP GET api/{version}/Tenants/{tenantId}/Users successful");
            }
            catch (AggregateException ex)
            {
                foreach (var inEx in ex.Flatten().InnerExceptions)
                {
                    Console.WriteLine($"Authentication failed with the following error: {inEx.Message}");
                }

                throw;
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
                Console.WriteLine("Error while initiating configuration: " + ex);
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

                var value = _configuration[key];

                if (value == null)
                {
                    Console.WriteLine($"Missing the value for \"{key}\" in config file");
                    Environment.Exit(1);
                }

                return value;
            }
            catch (Exception)
            {
                Console.WriteLine($"Configuration issue");
                throw;
            }
        }
    }
}
