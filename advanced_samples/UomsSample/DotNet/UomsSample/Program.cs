using System;
using System.Collections.Generic;
using System.IO;
using System.Threading.Tasks;
using Microsoft.Extensions.Configuration;
using OSIsoft.Data;
using OSIsoft.Data.Reflection;
using OSIsoft.Identity;

namespace UomsSample
{
    public static class Program
    {
        private static readonly Random _random = new Random();
        private static IConfiguration _configuration;
        private static Exception _toThrow = null;

        public static void Main()
        {
            MainAsync().GetAwaiter().GetResult();
        }

        [System.Diagnostics.CodeAnalysis.SuppressMessage("Design", "CA1031:Do not catch general exception types", Justification = "Sample needs to ensure cleanup, and will throw last error encountered.")]
        public static async Task<bool> MainAsync(bool test = false)
        {
            IConfigurationBuilder builder = new ConfigurationBuilder()
                .SetBasePath(Directory.GetCurrentDirectory())
                .AddJsonFile("appsettings.json")
                .AddJsonFile("appsettings.test.json", optional: true);
            _configuration = builder.Build();

            string tenantId = _configuration["TenantId"];
            string namespaceId = _configuration["NamespaceId"];
            string resource = _configuration["Resource"];
            string clientId = _configuration["ClientId"];
            string clientKey = _configuration["ClientKey"];
            string apiVersion = _configuration["ApiVersion"];

            string resourcePrefix = "UomSample";
            string typeId = $"{resourcePrefix} Uom";
            string streamWithPropertyOverridden = $"{resourcePrefix} UomPropertyOverridden";
            string streamWithoutPropertyOverridden = $"{resourcePrefix} UomNoPropertyOverridden";

            // Step 1 
            AuthenticationHandler authenticationHandler = new AuthenticationHandler(new Uri(resource), clientId, clientKey);
            SdsService service = new SdsService(new Uri(resource), authenticationHandler);

            ISdsMetadataService metadataService = service.GetMetadataService(tenantId, namespaceId);
            ISdsDataService sataService = service.GetDataService(tenantId, namespaceId);
            try
            {
                /*
                 * The following code provides an implementation for getting all the SdsUom ID's for each quantity.
                 * If you are not aware with which SdsUom ID to use, you can uncomment the below code and find out the
                 * uom id.
                 * 
                 * e.g. I am using degree_fahrenheit and  degree_celsius UOMS for temperature SdsQuantity.
                 * 
                 * 
                IEnumerable<SdsUomQuantity> sdsUomQuantities = await MetadataService.GetQuantitiesAsync();
                IEnumerable<SdsUom> sdsUoms = null;

                foreach (SdsUomQuantity sdsUomQuantity in sdsUomQuantities)
                {
                    sdsUoms = await MetadataService.GetQuantityUomsAsync(sdsUomQuantity.Id);

                    foreach (SdsUom sdsUom in sdsUoms)
                    {
                        Console.WriteLine(sdsUom.Id);
                    }
                }
                */

                // Step 2
                // Creating a Sdstype
                SdsType sdsType = SdsTypeBuilder.CreateSdsType<Widget>();
                sdsType.Id = typeId;

                sdsType = await metadataService.GetOrCreateTypeAsync(sdsType).ConfigureAwait(false);

                // Step 3
                // Creating a Stream overriding the distance property.
                SdsStream sdsStreamOne = new SdsStream()
                {
                    Id = streamWithPropertyOverridden,
                    TypeId = typeId,
                    Name = "UomStreamSourceWithPropertyOverridden",
                    PropertyOverrides = new List<SdsStreamPropertyOverride>(),
                };

                // Overriding the UOM of the distance property to be kilometer instead of mile.
                sdsStreamOne.PropertyOverrides.Add(new SdsStreamPropertyOverride()
                {
                    Uom = "kilometer",
                    SdsTypePropertyId = "Distance",
                });

                sdsStreamOne = await metadataService.GetOrCreateStreamAsync(sdsStreamOne).ConfigureAwait(false);

                // Step 4
                // Creating a Stream without overriding properties.
                SdsStream sdsStreamTwo = new SdsStream()
                {
                    Id = streamWithoutPropertyOverridden,
                    TypeId = typeId,
                    Name = "UomStreamSourceWithNoPropertyOverridden",
                };

                sdsStreamTwo = await metadataService.GetOrCreateStreamAsync(sdsStreamTwo).ConfigureAwait(false);

                // Step 5
                // Generating data
                IList<Widget> data = new List<Widget>();
                for (int i = 0; i < 10; i++)
                {
                    Widget widget = new Widget
                    {
                        Time = DateTime.UtcNow.AddSeconds(i),
                        Temperature = _random.Next(1, 100),
                        Distance = _random.Next(1, 100),
                    };
                    data.Add(widget);
                }

                /* In stream one, the temperature value will be inserted as Fahrenheit since we have defined the 
                 * default uom as Fahrenheit for Temperature in the Widget class. The distance value will be 
                 * inserted as kilometer, as we have overridden the Distance property in stream one, 
                 * regardless of the default uom for Distance in the Widget class.
                 */
                await sataService.InsertValuesAsync<Widget>(sdsStreamOne.Id, data).ConfigureAwait(false);

                /* In stream two, the temperature value will be inserted as Fahrenheit and the distance will be inserted as mile.
                 *
                 */
                await sataService.InsertValuesAsync<Widget>(sdsStreamTwo.Id, data).ConfigureAwait(false);

                // Step 6
                /*
                 * The last value stored in stream one. 
                 */
                Widget widgetFromStreamOne = await sataService.GetLastValueAsync<Widget>(sdsStreamOne.Id).ConfigureAwait(false);

                Console.WriteLine($"In stream one, the distance is {widgetFromStreamOne.Distance} kilometers and the temperature is {widgetFromStreamOne.Temperature} degrees fahrenheit");
                Console.WriteLine();
                /*
                 * The last value stored in stream two. 
                 */
                Widget widgetFromStreamTwo = await sataService.GetLastValueAsync<Widget>(sdsStreamTwo.Id).ConfigureAwait(false);

                Console.WriteLine($"In stream two, the distance is {widgetFromStreamTwo.Distance} miles and the temperature is {widgetFromStreamTwo.Temperature} degrees fahrenheit");
                Console.WriteLine();

                // Step 7
                /*
                 * If you want your data to be in specified uom, you can override your properties while making a call.
                 * In the following, I want the temperature to be in Celsius, and the distance to be in feet.
                 * 
                 * Then you can pass IList<SdsStreamPropertyOverride> to DataService while getting values.
                 * 
                 */
                IList<SdsStreamPropertyOverride> requestOverrides = new List<SdsStreamPropertyOverride>
                {
                    new SdsStreamPropertyOverride()
                    {
                        Uom = "degree celsius",
                        SdsTypePropertyId = "Temperature",
                    },
                    new SdsStreamPropertyOverride()
                    {
                        Uom = "foot",
                        SdsTypePropertyId = "Distance",
                    },
                };

                /*
                 * In the following call, data will be converted from Fahrenheit to Celsius for the temperature property,
                 * and from kilometer to foot for the distance property.
                 * 
                 * Uoms in Stream one (Temperature : Fahrenheit, Distance : Kilometer)
                 * 
                 */
                widgetFromStreamOne = await sataService.GetLastValueAsync<Widget>(sdsStreamOne.Id, requestOverrides).ConfigureAwait(false);

                Console.WriteLine($"In stream one, the distance is {widgetFromStreamOne.Distance} foot and the temperature is {widgetFromStreamOne.Temperature} degrees celsius");
                Console.WriteLine();

                /*
                 * In the following call, data will be converted from Fahrenheit to Celsius for the temperature property, 
                 * and from mile to foot for the distance property.
                 * 
                 * Uoms in Stream two (Temperature : Fahrenheit, Distance : Mile) 
                 * 
                 */
                widgetFromStreamTwo = await sataService.GetLastValueAsync<Widget>(sdsStreamTwo.Id, requestOverrides).ConfigureAwait(false);

                Console.WriteLine($"In stream two, the distance is {widgetFromStreamTwo.Distance} foot and the temperature is {widgetFromStreamTwo.Temperature} degrees celsius");
                Console.WriteLine();
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);
                _toThrow = ex;
            }
            finally
            {
                // Step 8
                Console.WriteLine("Deleting");
                RunInTryCatch(metadataService.DeleteStreamAsync, streamWithPropertyOverridden);
                RunInTryCatch(metadataService.DeleteStreamAsync, streamWithoutPropertyOverridden);
                RunInTryCatch(metadataService.DeleteTypeAsync, typeId);
                Console.WriteLine("Complete!");
                if (!test)
                    Console.ReadLine();
            }

            if (test && _toThrow != null)
                throw _toThrow;
            return _toThrow == null;
        }

        /// <summary>
        /// Use this to run a method that you don't want to stop the program if there is an error and you don't want to report the error
        /// </summary>
        /// <param name="methodToRun">The method to run.</param>
        /// <param name="value">The value to put into the method to run</param>
        [System.Diagnostics.CodeAnalysis.SuppressMessage("Design", "CA1031:Do not catch general exception types", Justification = "Sample needs to ensure cleanup, and will throw last error encountered.")]
        private static void RunInTryCatch(Func<string, Task> methodToRun, string value)
        {
            try
            {
                methodToRun(value).Wait(100);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Got error in {methodToRun.Method.Name} with value {value} but continued on:" + ex.Message);
                if (_toThrow == null)
                {
                    _toThrow = ex;
                }                    
            }
        }
    }
}
