using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text.RegularExpressions;
using System.Threading.Tasks;
using Microsoft.Extensions.Configuration;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using OSIsoft.Data;
using OSIsoft.DataViews;
using OSIsoft.DataViews.Contracts;
using OSIsoft.Identity;

namespace BulkUploader
{
    public static class Program
    {
        public static string DataviewPath { get; set; }
        public static string SdsTypePath { get; set; }
        public static string SdsStreamPath { get; set; }
        public static string SdsStreamMetaPath { get; set; }
        public static string SdsStreamTagPath { get; set; }
        public static string SdsStreamDataPath { get; set; }
        public static string SdsDataOnlyPath { get; set; }

        public static Exception ToThrow { get; set; }
        public static ISdsMetadataService MetadataService { get; set; }
        public static ISdsDataService DataService { get; set; }
        public static IDataViewService DvService { get; set; }

        public static void Main()
        {
            MainRunner();
        }

        public static bool MainRunner()
        {
            MetadataService = null;

            IConfiguration configuration = new ConfigurationBuilder()
                .SetBasePath(Directory.GetCurrentDirectory())
                .AddJsonFile("appsettings.json")
                .AddJsonFile("appsettings.test.json", optional: true)
                .Build();

            var tenantId = configuration["TenantId"];
            var namespaceId = configuration["NamespaceId"];
            var resource = configuration["Resource"];
            var clientId = configuration["ClientId"];
            var clientKey = configuration["ClientKey"];

            DataviewPath = configuration["Dataview"];
            SdsStreamPath = configuration["Stream"];
            SdsTypePath = configuration["Type"];

            SdsStreamDataPath = configuration["Data"];
            SdsStreamMetaPath = configuration["Metadata"];
            SdsStreamTagPath = configuration["Tags"];

            SdsDataOnlyPath = configuration["DataOnly"];

            (configuration as ConfigurationRoot).Dispose();
            var uriResource = new Uri(resource);

            AuthenticationHandler authenticationHandler = new AuthenticationHandler(uriResource, clientId, clientKey);

            SdsService sdsService = new SdsService(new Uri(resource), authenticationHandler);
            MetadataService = sdsService.GetMetadataService(tenantId, namespaceId);
            DataService = sdsService.GetDataService(tenantId, namespaceId);

            if (!string.IsNullOrEmpty(SdsTypePath))
                SendTypes();

            if (!string.IsNullOrEmpty(SdsStreamPath))
                SendStreams();

            if (!string.IsNullOrEmpty(SdsDataOnlyPath))
                SendData();

            if (!string.IsNullOrEmpty(DataviewPath))
            {
                AuthenticationHandler authenticationHandlerDataViews = new AuthenticationHandler(uriResource, clientId, clientKey); // currently this has to be a different auth handler or it throws errors
                var dv_service_factory = new DataViewServiceFactory(new Uri(resource), authenticationHandlerDataViews);
                DvService = dv_service_factory.GetDataViewService(tenantId, namespaceId);

                SendDataView();
            }

            if (ToThrow != null)
                throw ToThrow;

            Console.WriteLine("Success!!!");
            return true;
        }

        private static void LogException(Exception ex)
        {
            Console.WriteLine(ex);
            if (ToThrow == null)
                ToThrow = ex;
        }

        private static void SendDataView()
        {
            string dataviewS = File.ReadAllText(DataviewPath);
            List<DataView> dataviews = JsonConvert.DeserializeObject<List<DataView>>(dataviewS);
            foreach (var dataview in dataviews)
            {
                DvService.CreateOrUpdateDataViewAsync(dataview).Wait();
            }
        }

        private static void SendTypes()
        {
            Console.WriteLine($"Sending types from file: {SdsTypePath}");
            string types = File.ReadAllText(SdsTypePath);
            List<SdsType> typeList = JsonConvert.DeserializeObject<List<SdsType>>(types);
            foreach (var type in typeList)
            {
                MetadataService.GetOrCreateTypeAsync(type).Wait();
            }
        }

        [System.Diagnostics.CodeAnalysis.SuppressMessage("Design", "CA1031:Do not catch general exception types", Justification = "General catching so we can send the other streams and not stop on a 'small' issue")]
        private static void SendStreams()
        {
            Console.WriteLine($"Sending streams from file: {SdsStreamPath}");
            string streams = File.ReadAllText(SdsStreamPath);
            var streamsList = JsonConvert.DeserializeObject<List<SdsStream>>(streams); 
            foreach (var stream in streamsList)
            {
                MetadataService.GetOrCreateStreamAsync(stream).Wait();

                if (!string.IsNullOrEmpty(SdsStreamMetaPath))
                {
                    try
                    {
                        string path = SdsStreamMetaPath + stream.Id + ".json";
                        Console.WriteLine($"Sending stream metadata from file: {path}");
                        string meta = File.ReadAllText(path);
                        MetadataService.UpdateStreamMetadataAsync(stream.Id, JsonConvert.DeserializeObject<IDictionary<string, string>>(meta));
                    }
                    catch (Exception ex)
                    {
                        LogException(ex);
                    }
                }

                if (!string.IsNullOrEmpty(SdsStreamTagPath))
                {
                    try
                    {
                        string path = SdsStreamTagPath + stream.Id + ".json";
                        Console.WriteLine($"Sending stream tag from file: {path}");
                        string meta = File.ReadAllText(path);
                        MetadataService.UpdateStreamTagsAsync(stream.Id, JsonConvert.DeserializeObject<IList<string>>(meta));
                    }
                    catch (Exception ex)
                    {
                        LogException(ex);
                    }
                }

                if (!string.IsNullOrEmpty(SdsStreamDataPath))
                {
                    try
                    {
                        string path = SdsStreamDataPath + stream.Id + ".json";
                        Console.WriteLine($"Sending stream data from file: {path}");
                        string data = File.ReadAllText(path);
                        var dataAsList = JsonConvert.DeserializeObject<List<JObject>>(data);
                        DataService.UpdateValuesAsync(stream.Id, dataAsList).Wait();
                    }
                    catch (Exception ex)
                    {
                        LogException(ex);
                    }
                }
            }
        }

        private static void SendData()
        {
            foreach (string file in Directory.GetFiles(@".", "sdsdata*.json", SearchOption.AllDirectories))
            {
                Console.WriteLine($"Sending stream data from file: {file}");
                string data = File.ReadAllText(file);
                var matches = Regex.Matches(file, @"(?<=sdsdata)(.+?)(?=.json)");
                var streamName = matches.First().Value;
                var dataAsList = JsonConvert.DeserializeObject<List<JObject>>(data);
                DataService.UpdateValuesAsync(streamName, dataAsList).Wait();
            }
        }
    }
}
