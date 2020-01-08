using System;
using Microsoft.AspNetCore;
using Microsoft.AspNetCore.Hosting;

namespace AuthorizationCodeFlow
{
    public static class Program
    {
        public static void Main(string[] args)
        {
            Console.WriteLine("WARNING: The web server used in this sample is intended for use in testing or debugging sample applications locally. It has not been reviewed for security issues.");
            CreateWebHostBuilder(args).Build().Run();
        }

        public static IWebHostBuilder CreateWebHostBuilder(string[] args) =>
            WebHost.CreateDefaultBuilder(args)
                .UseStartup<Startup>();
    }
}
