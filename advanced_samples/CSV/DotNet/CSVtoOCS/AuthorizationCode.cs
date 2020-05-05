using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Net;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Net.Sockets;
using System.Runtime.InteropServices;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using IdentityModel.Client;
using IdentityModel.OidcClient;
using IdentityModel.OidcClient.Browser;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Http;

namespace CSVtoOCS
{
    //
    // Summary:
    //     DelegatingHandler to assist with authenticating with Identity Server.
    public class AuthenticationHandler_PKCE : DelegatingHandler
    {
        private string accessToken = null;
        private DateTime expiration = DateTime.MinValue;

        private string _clientId = null;

        private string _scope = null;

        private string _tenantId = null;

        public AuthenticationHandler_PKCE(string tenantId, string clientId, string resource = "https://dat-b.osisoft.com", string scope = "openid ocsapi")
        {
            _tenantId = tenantId;
            _clientId = clientId;
            _scope = scope
                ;
            AuthorizationCode.OcsAddress = resource;
            AuthorizationCode.RedirectHost = "https://127.0.0.1";
            AuthorizationCode.RedirectPort = 54567;
            AuthorizationCode.RedirectPath = "signin-oidc";

            if(SystemBrowser.OpenBrowser == null)
                SystemBrowser.OpenBrowser = new OpenSystemBrowser();
            // Get access token.

        }
    

        protected override Task<HttpResponseMessage> SendAsync(HttpRequestMessage request, CancellationToken cancellationToken)
        { 
            if (accessToken == null || expiration.AddSeconds(5) < DateTime.Now)
            {
                (accessToken, expiration) =
                    AuthorizationCode.GetAuthorizationCodeFlowAccessToken(_clientId, _scope, _tenantId);
            }

            request.Headers.Authorization = new AuthenticationHeaderValue("Bearer" , accessToken);


            return base.SendAsync(request, cancellationToken);
        }
    }

    public static class AuthorizationCode
    {
        private static OidcClient _oidcClient;
        private static string _ocsIdentityUrl;
        private static string _redirectHost;
        private static int _redirectPort;
        private static string _redirectPath;

        public static string OcsAddress
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

        public static (string, DateTime) GetAuthorizationCodeFlowAccessToken(string clientId, string scope, string tenantId)
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
                var dict = new Dictionary<string, string>();
                dict.Add("acr_values", $"tenant:{tenantId}");
                var loginRequest = new LoginRequest
                {
                    FrontChannelExtraParameters = dict
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

    public interface IOpenBrowser
    {
        void OpenBrowser(string url, string userName, string password);
    }

    public class OpenSystemBrowser : IOpenBrowser
    {
        public void OpenBrowser(string address, string userName, string password)
        {
            if (string.IsNullOrEmpty(address))
            {
                throw new ArgumentException("Address cannot be null or empty", nameof(address));
            }

            try
            {
                Process.Start(address);
            }
            catch
            {
                // hack because of this: https://github.com/dotnet/corefx/issues/10361
                if (RuntimeInformation.IsOSPlatform(OSPlatform.Windows))
                {
                    address = address.Replace("&", "^&", StringComparison.OrdinalIgnoreCase);
                    Process.Start(new ProcessStartInfo("cmd", $"/c start {address}") { CreateNoWindow = true });
                }
                else if (RuntimeInformation.IsOSPlatform(OSPlatform.Linux))
                {
                    Process.Start("xdg-open", address);
                }
                else if (RuntimeInformation.IsOSPlatform(OSPlatform.OSX))
                {
                    Process.Start("open", address);
                }
                else
                {
                    throw;
                }
            }
        }
    }

    public class SystemBrowser : IBrowser
    {
        private readonly string _path;

        public SystemBrowser(int? port = null, string path = null)
        {
            _path = path;

            if (!port.HasValue)
            {
                Port = GetRandomUnusedPort();
            }
            else
            {
                Port = port.Value;
            }
        }

        public static string UserName { get; set; }
        public static string Password { get; set; }
        public static IOpenBrowser OpenBrowser { get; set; }

        public int Port { get; }

        public async Task<BrowserResult> InvokeAsync(BrowserOptions options, CancellationToken cancellationToken = new CancellationToken())
        {
            if (options == null)
            {
                throw new ArgumentException("Options cannot be null.", nameof(options));
            }

            using var listener = new LoopbackHttpListener(Port, _path);
            OpenBrowser.OpenBrowser(options.StartUrl, UserName, Password);

            try
            {
                var result = await listener.WaitForCallbackAsync().ConfigureAwait(false);
                if (string.IsNullOrWhiteSpace(result))
                {
                    return new BrowserResult { ResultType = BrowserResultType.UnknownError, Error = "Empty response." };
                }

                return new BrowserResult { Response = result, ResultType = BrowserResultType.Success };
            }
            catch (TaskCanceledException ex)
            {
                return new BrowserResult { ResultType = BrowserResultType.Timeout, Error = ex.Message };
            }
        }

        private int GetRandomUnusedPort()
        {
            var listener = new TcpListener(IPAddress.Loopback, 0);
            listener.Start();
            var port = ((IPEndPoint)listener.LocalEndpoint).Port;
            listener.Stop();
            return port;
        }
    }

    public class LoopbackHttpListener : IDisposable
    {
        private const int DefaultTimeout = 60 * 5; // 5 mins (in seconds)
        private readonly IWebHost _host;
        private readonly TaskCompletionSource<string> _source = new TaskCompletionSource<string>();

        public LoopbackHttpListener(int port, string path = null)
        {
            path ??= string.Empty;
            if (path.StartsWith("/", StringComparison.OrdinalIgnoreCase)) path = path.Substring(1);

            Address = $"https://127.0.0.1:{port}/{path}";

            _host = new WebHostBuilder()
                .UseKestrel()
                .UseUrls(Address)
                .Configure(Configure)
                .Build();
            _host.Start();
        }

        public string Address { get; }

        public void Dispose()
        {
            Dispose(true);
            GC.SuppressFinalize(this);
        }

        public Task<string> WaitForCallbackAsync(int timeoutInSeconds = DefaultTimeout)
        {
            Task.Run(async () =>
            {
                await Task.Delay(timeoutInSeconds * 1000).ConfigureAwait(false);
                _source.TrySetCanceled();
            });

            return _source.Task;
        }

        protected virtual void Dispose(bool includeManaged)
        {
            if (includeManaged)
            {
                if (_host != null)
                {
                    _host.Dispose();
                }
            }
        }

        private void Configure(IApplicationBuilder app)
        {
            app.Run(async ctx =>
            {
                if (ctx.Request.Method == "GET")
                {
                    SetResult(ctx.Request.QueryString.Value, ctx);
                }
                else if (ctx.Request.Method == "POST")
                {
                    if (!ctx.Request.ContentType.Equals("application/x-www-form-urlencoded",
                        StringComparison.OrdinalIgnoreCase))
                    {
                        ctx.Response.StatusCode = 415;
                    }
                    else
                    {
                        using var sr = new StreamReader(ctx.Request.Body, Encoding.UTF8);
                        var body = await sr.ReadToEndAsync().ConfigureAwait(false);
                        SetResult(body, ctx);
                    }
                }
                else
                {
                    ctx.Response.StatusCode = 405;
                }
            });
        }

        private void SetResult(string value, HttpContext ctx)
        {
            try
            {
                ctx.Response.StatusCode = 200;
                ctx.Response.ContentType = "text/html";
                ctx.Response.WriteAsync("<h1>You can now return to the application.</h1>");
                ctx.Response.Body.FlushAsync();

                _source.TrySetResult(value);
            }
            catch
            {
                ctx.Response.StatusCode = 400;
                ctx.Response.ContentType = "text/html";
                ctx.Response.WriteAsync("<h1>Invalid request.</h1>");
                ctx.Response.Body.FlushAsync();
                throw;
            }
        }
    }

}
