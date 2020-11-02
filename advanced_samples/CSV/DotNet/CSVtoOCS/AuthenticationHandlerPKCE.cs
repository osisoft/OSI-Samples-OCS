using System;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Threading;
using System.Threading.Tasks;

namespace CSVtoOCS
{
    /// <summary>
    /// DelegatingHandler to assist with authenticating with Identity Server.
    /// </summary>
    public class AuthenticationHandlerPKCE : DelegatingHandler
    {
        private string _accessToken;
        private DateTime _expiration = DateTime.MinValue;

        public AuthenticationHandlerPKCE(string tenantId, string clientId, string resource = "https://dat-b.osisoft.com")
        {
            TenantId = tenantId;
            ClientId = clientId;
            AuthorizationCode.OcsAddress = resource;
            AuthorizationCode.RedirectHost = "https://127.0.0.1";
            AuthorizationCode.RedirectPort = 54567;
            AuthorizationCode.RedirectPath = "signin-oidc";

            if (SystemBrowser.OpenBrowser == null)
                SystemBrowser.OpenBrowser = new OpenSystemBrowser();
        }

        private string ClientId { get; set; }
        private string TenantId { get; set; }

        protected override Task<HttpResponseMessage> SendAsync(HttpRequestMessage request, CancellationToken cancellationToken)
        {
            if (request == null)
            {
                throw new ArgumentNullException(nameof(request));
            }

            if (_accessToken == null || _expiration.AddSeconds(5) < DateTime.Now)
            {
                (_accessToken, _expiration) =
                    AuthorizationCode.GetAuthorizationCodeFlowAccessToken(ClientId, TenantId);
            }

            request.Headers.Authorization = new AuthenticationHeaderValue("Bearer", _accessToken);

            return base.SendAsync(request, cancellationToken);
        }
    }
}
