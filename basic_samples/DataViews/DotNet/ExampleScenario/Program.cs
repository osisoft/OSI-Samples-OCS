using System;
using System.IO;
using System.Threading.Tasks;
using Microsoft.Extensions.Configuration;
using OSIsoft.Data;
using OSIsoft.Identity;

namespace ExampleScenario
{
    public static class Program
    {
        public static void Main()
        {
            MainAsync().GetAwaiter().GetResult();
        }

        public static async Task MainAsync()
        {
            // authenticate on OCS
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

            (configuration as ConfigurationRoot).Dispose();
            var uriResource = new Uri(resource);

            AuthenticationHandler authenticationHandler = new AuthenticationHandler(uriResource, clientId, clientKey);

            SdsService sdsService = new SdsService(new Uri(resource), authenticationHandler);
            var metadataService = sdsService.GetMetadataService(tenantId, namespaceId);
            var dataService = sdsService.GetDataService(tenantId, namespaceId);

            // create types
            var types = ExampleTypes.GetExampleTypes();
            foreach (var type in types)
            {
                await metadataService.GetOrCreateTypeAsync(type).ConfigureAwait(false);
            }

            DataGenerator dataGenerator = new DataGenerator();
            var streams = ExampleStreams.GetExampleStreams();
            foreach (var stream in streams)
            {
                // create stream
                await metadataService.GetOrCreateStreamAsync(stream).ConfigureAwait(false);

                // add stream metadata
                await metadataService.UpdateStreamMetadataAsync(stream.Id, ExampleStreams.GetMetadata(stream)).ConfigureAwait(false);
                await metadataService.UpdateStreamTagsAsync(stream.Id, ExampleStreams.GetTags(stream.Id)).ConfigureAwait(false);

                // insert data
                switch (stream.TypeId)
                {
                    case ExampleTypes.InverterType:
                        await dataService.InsertValuesAsync(stream.Id, dataGenerator.GetInverterValues()).ConfigureAwait(false);
                        break;
                    case ExampleTypes.WeatherGen1Type:
                        await dataService.InsertValuesAsync(stream.Id, dataGenerator.GetWeatherGen1Values()).ConfigureAwait(false);
                        break;
                    case ExampleTypes.WeatherGen2Type:
                        await dataService.InsertValuesAsync(stream.Id, dataGenerator.GetWeatherGen2Values()).ConfigureAwait(false);
                        break;
                    default:
                        break;
                }
            }
        }
    }
}
