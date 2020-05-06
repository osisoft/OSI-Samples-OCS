using System;
using System.IO;
using System.Text;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Http;

namespace HybridFlow
{
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
