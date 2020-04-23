using System;
using System.IO;
using System.Threading.Tasks;
using Microsoft.Extensions.Configuration;

namespace OmfIngressClientLibraries
{
    public static class Program
    {
        private static OmfIngressClient _omfIngressClient;
        private static Device _omfDevice;
        private static IConfiguration _config;

        public static string Address { get; set; }
        public static string TenantId { get; set; }
        public static string NamespaceId { get; set; }
        public static string ClientId { get; set; }
        public static string ClientSecret { get; set; }
        public static string ConnectionName { get; set; }
        public static string StreamId { get; set; }
        public static string DeviceClientId { get; set; }
        public static string DeviceClientSecret { get; set; }

        [System.Diagnostics.CodeAnalysis.SuppressMessage("Design", "CA1031:Do not catch general exception types", Justification = "Sample needs to ensure cleanup, and will throw last error encountered.")]
        public static void Main()
        {
            Setup();
            Exception toThrow = null;
            OmfConnection omfConnection = null;
            try
            {
                // Create the Connection, send OMF
                omfConnection = CreateOmfConnectionAsync().GetAwaiter().GetResult();
                SendTypeContainerAndDataAsync().GetAwaiter().GetResult();
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);
                toThrow = ex;
            }
            finally
            {
                // Delete the Type and Stream
                try
                {
                    DeleteTypeAndContainerAsync().GetAwaiter().GetResult();
                }
                catch (Exception ex)
                {
                    Console.WriteLine(ex.Message);
                    toThrow = ex;
                }

                if (omfConnection != null)
                {
                    // Delete the Connection
                    try
                    {
                        DeleteOmfConnectionAsync(omfConnection).GetAwaiter().GetResult();
                    }
                    catch (Exception ex)
                    {
                        Console.WriteLine(ex.Message);
                        toThrow = ex;
                    }
                }

                Console.WriteLine("Complete!");
                Console.ReadKey();
            }

            if (toThrow != null)
            {
                throw toThrow;
            }
        }

        public static void Setup()
        {
            IConfigurationBuilder builder = new ConfigurationBuilder()
                .SetBasePath(Directory.GetCurrentDirectory())
                .AddJsonFile("appsettings.json");
            _config = builder.Build();

            // ==== Client constants ====
            TenantId = _config["TenantId"];
            NamespaceId = _config["NamespaceId"];
            Address = _config["Address"];
            ClientId = _config["ClientId"];
            ClientSecret = _config["ClientSecret"];
            ConnectionName = _config["ConnectionName"];
            StreamId = _config["StreamId"];
            DeviceClientId = _config["DeviceClientId"];
            DeviceClientSecret = _config["DeviceClientSecret"];

            _omfDevice = new Device(Address, TenantId, NamespaceId, DeviceClientId, DeviceClientSecret);

            // Get Ingress Services to communicate with server and handle ingress management
            _omfIngressClient = new OmfIngressClient(Address, TenantId, NamespaceId, ClientId, ClientSecret);

            Console.WriteLine($"OCS endpoint at {Address}");
            Console.WriteLine();            
        }

        public static async Task<OmfConnection> CreateOmfConnectionAsync()
        {
            // Create the Connection
            OmfConnection omfConnection = await _omfIngressClient.CreateOmfConnectionAsync(DeviceClientId, ConnectionName, NamespaceId).ConfigureAwait(false);
            return omfConnection;
        }

        public static async Task SendTypeContainerAndDataAsync()
        {
            // Create the Type and Stream
            await _omfDevice.CreateDataPointTypeAsync().ConfigureAwait(false);
            await _omfDevice.CreateStreamAsync(StreamId).ConfigureAwait(false);

            // Send random data points
            Random rand = new Random();
            Console.WriteLine("Sending 5 OMF Data Messages.");
            for (int i = 0; i < 5; i++)
            {
                DataPointType dataPoint = new DataPointType() { Timestamp = DateTime.UtcNow, Value = rand.NextDouble() };
                await _omfDevice.SendValueAsync(StreamId, dataPoint).ConfigureAwait(false);
                await Task.Delay(1000).ConfigureAwait(false);
            }
        }

        public static async Task DeleteTypeAndContainerAsync()
        {
            // Delete the Type and Stream
            await _omfDevice.DeleteStreamAsync(StreamId).ConfigureAwait(false);
            await _omfDevice.DeleteDataPointTypeAsync().ConfigureAwait(false);
        }

        public static async Task DeleteOmfConnectionAsync(OmfConnection omfConnection)
        {
            // Delete the Connection           
            await _omfIngressClient.DeleteOmfConnectionAsync(omfConnection).ConfigureAwait(false);
        }
    }
}
