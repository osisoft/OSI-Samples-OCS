using Microsoft.Extensions.Configuration;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using OSIsoft.Data;
using OSIsoft.DataViews.Contracts;
using OSIsoft.Identity;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Threading.Tasks;
using System.Text.RegularExpressions;
using OSIsoft.DataViews;
using System;

namespace Bulk_Uploader
{
    public class Program
    {
        public static string dataviewPath;
        public static string sdsTypePath;
        public static string sdsStreamPath;
        public static string sdsStreamMetaPath;
        public static string sdsStreamTagPath;
        public static string sdsStreamDataPath;
        public static string sdsDataOnlyPath;

        public static Exception toThrow = null;
        public static bool success = true;
        public static ISdsMetadataService metadataService;
        public static ISdsDataService dataService;
        public static IDataViewService dvService;


        public static void Main()
        {
            MainAsync().GetAwaiter().GetResult();
        }

        public static async Task<bool> MainAsync(bool test = false)
        {
            success = true;
            metadataService = null;


            try
            {
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

                dataviewPath = (configuration["Dataview"]);
                sdsStreamPath = (configuration["Stream"]);
                sdsTypePath = (configuration["Type"]);

                sdsStreamDataPath = (configuration["Data"]);
                sdsStreamMetaPath = (configuration["Metadata"]);
                sdsStreamTagPath = (configuration["Tags"]);

                sdsDataOnlyPath = (configuration["DataOnly"]);

                (configuration as ConfigurationRoot).Dispose();
                var uriResource = new Uri(resource);

                AuthenticationHandler authenticationHandler = new AuthenticationHandler(uriResource, clientId, clientKey);

                SdsService sdsService = new SdsService(new Uri(resource), authenticationHandler);
                metadataService = sdsService.GetMetadataService(tenantId, namespaceId);
                dataService = sdsService.GetDataService(tenantId, namespaceId);
                var tableService = sdsService.GetTableService(tenantId, namespaceId);

                if(!String.IsNullOrEmpty(sdsTypePath))
                    SendTypes();
                if (!String.IsNullOrEmpty(sdsStreamPath))
                    SendStreams();
                if(!String.IsNullOrEmpty(sdsDataOnlyPath))
                    SendData();

                if (!String.IsNullOrEmpty(dataviewPath))
                {
                    AuthenticationHandler authenticationHandlerDataViews = new AuthenticationHandler(uriResource, clientId, clientKey); //currently this has to be a different auth handler or it throws errors
                    var dvServiceFactory = new DataViewServiceFactory(new Uri(resource), authenticationHandlerDataViews);
                    dvService = dvServiceFactory.GetDataViewService(tenantId, namespaceId);

                    SendDataView();
                }
            }
            catch (Exception ex)
            {
                success = false;
                Console.WriteLine(ex.Message);
                toThrow = ex;
            }
            finally
            {

            }


            if (test && !success)
                throw toThrow;
            Console.WriteLine("Success!!!");

            return success;
        }


        private static void SendDataView()
        {
            string dataviewS = File.ReadAllText(dataviewPath);
            List<DataView> dataviews = JsonConvert.DeserializeObject<List<DataView>>(dataviewS);
            foreach (var dataview in dataviews)
            {
                dvService.CreateOrUpdateDataViewAsync(dataview).Wait();
            }
        }

        private static void SendTypes()
        {
            Console.WriteLine($"Sending types from file: {sdsTypePath}");
            string types = File.ReadAllText(sdsTypePath);
            List<SdsType> typeList = JsonConvert.DeserializeObject<List<SdsType>>(types);
            foreach (var type in typeList)
            {
                metadataService.GetOrCreateTypeAsync(type).Wait();
            }
        }

        private static void SendStreams()
        {
            Console.WriteLine($"Sending streams from file: {sdsStreamPath}");
            string streams = File.ReadAllText(sdsStreamPath);
            var streamsList = JsonConvert.DeserializeObject<List<SdsStream>>(streams); 
            foreach (var stream in streamsList)
            {
                metadataService.GetOrCreateStreamAsync(stream).Wait();

                if (!String.IsNullOrEmpty(sdsStreamMetaPath))
                {
                    try
                    {
                        string path = sdsStreamMetaPath + stream.Id + ".json";
                        Console.WriteLine($"Sending stream metadata from file: {path}");
                        string meta = File.ReadAllText(path);
                        metadataService.UpdateStreamMetadataAsync(stream.Id, JsonConvert.DeserializeObject<IDictionary<string,string>>(meta));
                    }
                    catch (Exception ex)
                    {
                        success = false;
                        toThrow = ex;
                    }
                }
                if (!String.IsNullOrEmpty(sdsStreamTagPath))
                {
                    try
                    {
                        string path = sdsStreamTagPath + stream.Id + ".json";
                        Console.WriteLine($"Sending stream tag from file: {path}");
                        string meta = File.ReadAllText(path);
                        metadataService.UpdateStreamTagsAsync(stream.Id, JsonConvert.DeserializeObject<IList<string>>(meta));
                    }
                    catch (Exception ex)
                    {
                        success = false;
                        toThrow = ex;
                    }
                }

                if (!String.IsNullOrEmpty(sdsStreamDataPath))
                {
                    try
                    {
                        string path = sdsStreamDataPath + stream.Id + ".json";
                        Console.WriteLine($"Sending stream data from file: {path}");
                        string data = File.ReadAllText(path);
                        var dataAsList = JsonConvert.DeserializeObject<List<JObject>>(data);
                        dataService.UpdateValuesAsync(stream.Id, dataAsList).Wait();
                    }
                    catch (Exception ex)
                    {
                        success = false;
                        toThrow = ex;
                    }
                }
            }
        }

        private static void SendData()
        {
            foreach (String file in Directory.GetFiles(@".", "sdsdata*.json", SearchOption.AllDirectories))
            {
                Console.WriteLine($"Sending stream data from file: {file}");
                string data = File.ReadAllText(file);
                var matches = Regex.Matches(file, @"(?<=sdsdata)(.+?)(?=.json)");
                var streamName = matches.First().Value;
                try
                {
                    var dataAsList = JsonConvert.DeserializeObject<List<JObject>>(data);
                    dataService.UpdateValuesAsync(streamName, dataAsList).Wait();  
                }
                catch (Exception ex)
                {
                    success = false;
                    Console.WriteLine(streamName);
                    Console.WriteLine(ex.Message);
                    Console.WriteLine(ex.StackTrace);
                    success = false;
                    toThrow = ex;
                }
            }
        }
    }
}
