using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.Extensions.Configuration;
using OSIsoft.Data;
using OSIsoft.Data.Http;
using OSIsoft.Data.Reflection;
using OSIsoft.Identity;

namespace SdsClientLibraries
{
    public static class Program
    {
        private static IConfiguration _configuration;
        private static Exception _toThrow = null;

        public static void Main() => MainAsync().GetAwaiter().GetResult();

        [System.Diagnostics.CodeAnalysis.SuppressMessage("Design", "CA1031:Do not catch general exception types", Justification = "Sample needs to ensure cleanup, and will throw last error encountered.")]
        public static async Task<bool> MainAsync(bool test = false)
        {            
            IConfigurationBuilder builder = new ConfigurationBuilder()
                .SetBasePath(Directory.GetCurrentDirectory())
                .AddJsonFile("appsettings.json")
                .AddJsonFile("appsettings.test.json", optional: true);
            _configuration = builder.Build();

            // ==== Client constants ====
            var tenantId = _configuration["TenantId"];
            var namespaceId = _configuration["NamespaceId"];
            var resource = _configuration["Resource"];
            var clientId = _configuration["ClientId"];
            var clientKey = _configuration["ClientKey"];

            // ==== Metadata IDs ====
            string streamId = "SampleStream";
            string streamIdSecondary = "SampleStream_Secondary";
            string streamIdCompound = "SampleStream_Compound";

            string typeId = "SampleType";
            string targetTypeId = "SampleType_Target";
            string targetIntTypeId = "SampleType_TargetInt";
            string autoStreamViewId = "SampleAutoStreamView";
            string manualStreamViewId = "SampleManualStreamView";
            string compoundTypeId = "SampleType_Compound";

            var uriResource = new Uri(resource);
            
            // Step 1 
            // Get Sds Services to communicate with server
            AuthenticationHandler authenticationHandler = new AuthenticationHandler(uriResource, clientId, clientKey);
            
            SdsService sdsService = new SdsService(new Uri(resource), null, HttpCompressionMethod.GZip, authenticationHandler);
            var metadataService = sdsService.GetMetadataService(tenantId, namespaceId);
            var dataService = sdsService.GetDataService(tenantId, namespaceId);
            var tableService = sdsService.GetTableService(tenantId, namespaceId);
            
            Console.WriteLine(Resources.Banner);
            Console.WriteLine();
            Console.WriteLine($"SDS endpoint at {resource}");
            Console.WriteLine();

            try
            {
                // Step 2
                // create an SdsType
                Console.WriteLine(Resources.CreatingType);
                SdsType type = SdsTypeBuilder.CreateSdsType<WaveData>();
                type.Id = typeId;
                type = await metadataService.GetOrCreateTypeAsync(type).ConfigureAwait(false);

                // Step 3
                // create an SdsStream
                Console.WriteLine(Resources.CreatingStream);
                var stream = new SdsStream
                {
                    Id = streamId,
                    Name = "Wave Data Sample",
                    TypeId = type.Id,
                    Description = "This is a sample SdsStream for storing WaveData type measurements",
                };
                stream = await metadataService.GetOrCreateStreamAsync(stream).ConfigureAwait(false);

                // Step 4
                // insert data
                Console.WriteLine(Resources.InsertingData);

                // insert a single event
                var wave = GetWave(0, 2);
                await dataService.InsertValueAsync(stream.Id, wave).ConfigureAwait(false);

                // insert a list of events
                var waves = new List<WaveData>();
                for (var i = 2; i <= 18; i += 2)
                {
                    waves.Add(GetWave(i, 2));
                }

                await dataService.InsertValuesAsync(stream.Id, waves).ConfigureAwait(false);

                // Step 5
                // get last event
                Console.WriteLine(Resources.GettingLatest);
                var latest = await dataService.GetLastValueAsync<WaveData>(streamId).ConfigureAwait(false);
                Console.WriteLine(latest.ToString());
                Console.WriteLine();

                // get all events
                Console.WriteLine(Resources.GettingAll);
                var allEvents = (List<WaveData>)await dataService.GetWindowValuesAsync<WaveData>(streamId, "0", "180").ConfigureAwait(false);
                Console.WriteLine($"Total events found: {allEvents.Count}");
                foreach (var evnt in allEvents)
                {
                    Console.WriteLine(evnt.ToString());
                }

                Console.WriteLine();

                // Step 6
                // getting all events in table format with headers
                var tableEvents = await tableService.GetWindowValuesAsync(stream.Id, "0", "180").ConfigureAwait(false);

                Console.WriteLine(Resources.GettingTable);
                foreach (var evnt in tableEvents.Rows)
                {
                    Console.WriteLine(string.Join(",", evnt.ToArray()));
                }

                Console.WriteLine();

                // Step 7
                // update events
                Console.WriteLine(Resources.UpdatingEvents);

                // update one event
                var updatedWave = UpdateWave(allEvents.First(), 4);
                await dataService.UpdateValueAsync(stream.Id, updatedWave).ConfigureAwait(false);

                // update all events, adding ten more
                var updatedCollection = new List<WaveData>();
                for (int i = 2; i < 40; i += 2)
                {
                    updatedCollection.Add(GetWave(i, 4));
                }

                await dataService.UpdateValuesAsync(stream.Id, updatedCollection).ConfigureAwait(false);

                allEvents = (List<WaveData>)await dataService.GetWindowValuesAsync<WaveData>(stream.Id, "0", "180").ConfigureAwait(false);

                Console.WriteLine(Resources.GettingUpdated);
                Console.WriteLine($"Total events found: {allEvents.Count}");

                foreach (var evnt in allEvents)
                {
                    Console.WriteLine(evnt.ToString());
                }

                Console.WriteLine();

                // Step 8
                // replacing events
                Console.WriteLine(Resources.ReplacingEvents);

                // replace one event
                var replaceEvent = UpdateWave(allEvents.First(), multiplier: 5);

                await dataService.ReplaceValueAsync<WaveData>(streamId, replaceEvent).ConfigureAwait(false);

                // replace all events
                for (int i = 1; i < allEvents.Count; i++)
                {
                    allEvents[i] = UpdateWave(allEvents[i], multiplier: 5);
                }

                await dataService.ReplaceValuesAsync<WaveData>(streamId, allEvents).ConfigureAwait(false);

                Console.WriteLine(Resources.GettingReplaced);
                var replacedEvents = (List<WaveData>)await dataService.GetWindowValuesAsync<WaveData>(streamId, "0", "180").ConfigureAwait(false);
                Console.WriteLine($"Total events found: {replacedEvents.Count}");
                foreach (var evnt in replacedEvents)
                {
                    Console.WriteLine(evnt.ToString());
                }

                Console.WriteLine();

                // Step 9
                // Property Overrides
                Console.WriteLine(Resources.SdsInterpolateOrExtrapolate);
                Console.WriteLine();

                // We will retrieve three events using the default behavior, Continuous
                var retrieved = await dataService
                    .GetRangeValuesAsync<WaveData>(stream.Id, "1", 3, SdsBoundaryType.ExactOrCalculated).ConfigureAwait(false);
                Console.WriteLine(Resources.DefaultContinuous);
                foreach (var value in retrieved)
                {
                    Console.WriteLine(value.ToString());
                }

                Console.WriteLine();

                var retrievedInterpolated = await dataService
                    .GetValuesAsync<WaveData>(stream.Id, "5", "32", 4).ConfigureAwait(false);
                Console.WriteLine(Resources.SdsInterpolate);
                foreach (var value in retrievedInterpolated)
                {
                    Console.WriteLine(value.ToString());
                }

                Console.WriteLine();

                // Step 10
                // We will retrieve events filtered to only get the ones where the radians are less than 50.  Note, this can be done on index properties too.
                var retrievedInterpolatedFiltered = await dataService.GetWindowFilteredValuesAsync<WaveData>(stream.Id, "0", "180", SdsBoundaryType.ExactOrCalculated, "Radians lt 50").ConfigureAwait(false);
                Console.WriteLine(Resources.SdsRadiansLessThan50);
                foreach (var value in retrievedInterpolatedFiltered)
                {
                    Console.WriteLine(value.ToString());
                }

                Console.WriteLine();

                // Step 11
                // We will retrieve a sample of our data
                Console.WriteLine(Resources.SdsSampleTrends);
                Console.WriteLine(Resources.GettingSampled);
                var sampledValues = await dataService.GetSampledValuesAsync<WaveData>(stream.Id, "0",
                    "40", 4, new[] { nameof(WaveData.Sin) }).ConfigureAwait(false);
                foreach (var sample in sampledValues)
                {
                    Console.WriteLine(sample);
                }

                Console.WriteLine();

                // Step 12
                // create a Discrete stream PropertyOverride indicating that we do not want Sds to calculate a value for Radians and update our stream 
                var propertyOverride = new SdsStreamPropertyOverride()
                {
                    SdsTypePropertyId = "Radians",
                    InterpolationMode = SdsInterpolationMode.Discrete,
                };
                var propertyOverrides = new List<SdsStreamPropertyOverride>() { propertyOverride };

                // update the stream
                stream.PropertyOverrides = propertyOverrides;
                await metadataService.CreateOrUpdateStreamAsync(stream).ConfigureAwait(false);

                retrieved = await dataService
                    .GetRangeValuesAsync<WaveData>(stream.Id, "1", 3, SdsBoundaryType.ExactOrCalculated).ConfigureAwait(false);
                Console.WriteLine(Resources.OverrideRadiansInterpolate);
                Console.WriteLine(Resources.SdsReturnDefaultValue);

                foreach (var value in retrieved)
                {
                    Console.WriteLine(value.ToString());
                }

                Console.WriteLine();

                // Step 13
                // StreamViews
                Console.WriteLine(Resources.SdsStreamViews);

                // create target types
                var targetType = SdsTypeBuilder.CreateSdsType<WaveDataTarget>();
                targetType.Id = targetTypeId;

                var targetIntType = SdsTypeBuilder.CreateSdsType<WaveDataInteger>();
                targetIntType.Id = targetIntTypeId;

                await metadataService.GetOrCreateTypeAsync(targetType).ConfigureAwait(false);
                await metadataService.GetOrCreateTypeAsync(targetIntType).ConfigureAwait(false);

                // create StreamViews
                var autoStreamView = new SdsStreamView()
                {
                    Id = autoStreamViewId,
                    SourceTypeId = typeId,
                    TargetTypeId = targetTypeId,
                };

                // create explicit mappings 
                var vp1 = new SdsStreamViewProperty() { SourceId = "Order", TargetId = "OrderTarget" };
                var vp2 = new SdsStreamViewProperty() { SourceId = "Sin", TargetId = "SinInt" };
                var vp3 = new SdsStreamViewProperty() { SourceId = "Cos", TargetId = "CosInt" };
                var vp4 = new SdsStreamViewProperty() { SourceId = "Tan", TargetId = "TanInt" };

                var manualStreamView = new SdsStreamView()
                {
                    Id = manualStreamViewId,
                    SourceTypeId = typeId,
                    TargetTypeId = targetIntTypeId,
                    Properties = new List<SdsStreamViewProperty>() { vp1, vp2, vp3, vp4 },
                };

                await metadataService.CreateOrUpdateStreamViewAsync(autoStreamView).ConfigureAwait(false);
                await metadataService.CreateOrUpdateStreamViewAsync(manualStreamView).ConfigureAwait(false);

                Console.WriteLine(Resources.HereIsSomeData);
                foreach (var evnt in retrieved)
                {
                    Console.WriteLine($"Sin: {evnt.Sin}, Cos: {evnt.Cos}, Tan {evnt.Tan}");
                }

                Console.WriteLine();

                // get autoStreamView data
                var autoStreamViewData = await dataService.GetRangeValuesAsync<WaveDataTarget>(stream.Id, "1", 3, SdsBoundaryType.ExactOrCalculated, autoStreamViewId).ConfigureAwait(false);

                Console.WriteLine(Resources.StreamViewSameShape);

                foreach (var value in autoStreamViewData)
                {
                    Console.WriteLine($"SinTarget: {value.SinTarget} CosTarget: {value.CosTarget} TanTarget: {value.TanTarget}");
                }

                Console.WriteLine();

                // get manualStreamView data
                Console.WriteLine(Resources.StreamViewConvertData);
                var manualStreamViewData = await dataService.GetRangeValuesAsync<WaveDataInteger>(stream.Id, "1", 3, SdsBoundaryType.ExactOrCalculated, manualStreamViewId).ConfigureAwait(false);

                foreach (var value in manualStreamViewData)
                {
                    Console.WriteLine($"SinInt: {value.SinInt} CosInt: {value.CosInt} TanInt: {value.TanInt}");
                }

                Console.WriteLine();

                // get SdsStreamViewMap
                Console.WriteLine(Resources.StreamViewQuerySds);
                var autoStreamViewMap = await metadataService.GetStreamViewMapAsync(autoStreamViewId).ConfigureAwait(false);
                PrintStreamViewMapProperties(autoStreamViewMap);

                Console.WriteLine(Resources.StreamViewExplicitMapping);
                var manualStreamViewMap = await metadataService.GetStreamViewMapAsync(manualStreamViewId).ConfigureAwait(false);
                PrintStreamViewMapProperties(manualStreamViewMap);

                // Step 14
                // Update Stream Type based on SdsStreamView
                Console.WriteLine(Resources.StreamViewUpdateType);

                var firstVal = await dataService.GetFirstValueAsync<WaveData>(stream.Id).ConfigureAwait(false);

                await metadataService.UpdateStreamTypeAsync(stream.Id, autoStreamViewId).ConfigureAwait(false);
                var newStream = await metadataService.GetStreamAsync(stream.Id).ConfigureAwait(false);

                var firstValUpdated = await dataService.GetFirstValueAsync<WaveDataTarget>(stream.Id).ConfigureAwait(false);

                Console.WriteLine($"The new type id {newStream.TypeId} compared to the original one {stream.TypeId}.");
                Console.WriteLine($"The new type value {firstValUpdated} compared to the original one {firstVal}.");
                Console.WriteLine();

                // Step 15
                // Show filtering on Type, works the same as filtering on Streams
                var types = await metadataService.GetTypesAsync().ConfigureAwait(false);
                var typesFiltered = await metadataService.GetTypesAsync("Id:*Target*").ConfigureAwait(false);

                Console.WriteLine($"The number of types returned without filtering: {types.Count()}.  With filtering {typesFiltered.Count()}.");
                Console.WriteLine();

                // Step 16
                // tags and metadata
                Console.WriteLine(Resources.AddTagsMetadata);
                var tags = new List<string> { "waves", "periodic", "2018", "validated" };
                var metadata = new Dictionary<string, string>() { { "Region", "North America" }, { "Country", "Canada" }, { "Province", "Quebec" } };

                await metadataService.UpdateStreamTagsAsync(streamId, tags).ConfigureAwait(false);
                await metadataService.UpdateStreamMetadataAsync(streamId, metadata).ConfigureAwait(false);

                tags = (List<string>)await metadataService.GetStreamTagsAsync(streamId).ConfigureAwait(false);

                Console.WriteLine();
                Console.WriteLine(string.Format(CultureInfo.CurrentCulture, Resources.TagsAssociatedWith, streamId));
                foreach (var tag in tags)
                {
                    Console.WriteLine(tag);
                }

                Console.WriteLine();
                Console.WriteLine(string.Format(CultureInfo.CurrentCulture, Resources.MetadataAssociatedWith, streamId));
                Console.WriteLine("Metadata key Region: " + await metadataService.GetStreamMetadataValueAsync(streamId, "Region").ConfigureAwait(false));
                Console.WriteLine("Metadata key Country: " + await metadataService.GetStreamMetadataValueAsync(streamId, "Country").ConfigureAwait(false));
                Console.WriteLine("Metadata key Province: " + await metadataService.GetStreamMetadataValueAsync(streamId, "Province").ConfigureAwait(false));

                Console.WriteLine();

                // Step 17
                // delete values
                Console.WriteLine(Resources.DeletingValues);

                // delete one event
                await dataService.RemoveValueAsync(stream.Id, 0).ConfigureAwait(false);

                // delete all events
                await dataService.RemoveWindowValuesAsync(stream.Id, 1, 200).ConfigureAwait(false);

                retrieved = await dataService.GetWindowValuesAsync<WaveData>(stream.Id, "0", "200").ConfigureAwait(false);
                if (retrieved.ToList<WaveData>().Count == 0)
                {
                    Console.WriteLine(Resources.DeletedSuccessfully);
                }

                Console.WriteLine();

                // Step 18
                // Adding a new stream with a secondary index.
                Console.WriteLine(Resources.AddingSecondaryIndex);

                SdsStreamIndex measurementIndex = new SdsStreamIndex()
                {
                    SdsTypePropertyId = type.Properties.First(p => p.Id.Equals("Radians", StringComparison.OrdinalIgnoreCase)).Id,
                };

                SdsStream secondary = new SdsStream()
                {
                    Id = streamIdSecondary,
                    TypeId = type.Id,
                    Indexes = new List<SdsStreamIndex>()
                    {
                        measurementIndex,
                    },
                };

                secondary = await metadataService.GetOrCreateStreamAsync(secondary).ConfigureAwait(false);
                Console.WriteLine($"Secondary indexes on streams. {stream.Id}:{stream.Indexes?.Count}. {secondary.Id}:{secondary.Indexes.Count}. ");
                Console.WriteLine();

                // Modifying an existing stream with a secondary index.
                Console.WriteLine(Resources.ModifyingSecondaryIndex);

                stream = await metadataService.GetStreamAsync(stream.Id).ConfigureAwait(false);
                type = await metadataService.GetTypeAsync(stream.TypeId).ConfigureAwait(false);

                SdsStreamIndex measurementTargetIndex = new SdsStreamIndex()
                {
                    SdsTypePropertyId = type.Properties.First(p => p.Id.Equals("RadiansTarget", StringComparison.OrdinalIgnoreCase)).Id,
                };
                stream.Indexes = new List<SdsStreamIndex>() { measurementTargetIndex };

                await metadataService.CreateOrUpdateStreamAsync(stream).ConfigureAwait(false);
                stream = await metadataService.GetStreamAsync(stream.Id).ConfigureAwait(false);

                // Modifying an existing stream to remove the secondary index
                Console.WriteLine(Resources.RemovingSecondaryIndex);

                secondary.Indexes = null;
                await metadataService.CreateOrUpdateStreamAsync(secondary).ConfigureAwait(false);
                secondary = await metadataService.GetStreamAsync(secondary.Id).ConfigureAwait(false);
                Console.WriteLine($"Secondary indexes on streams. {stream.Id}:{stream.Indexes?.Count}. {secondary.Id}:{secondary.Indexes?.Count}. ");
                Console.WriteLine();

                // Step 19
                // Adding Compound Index Type
                Console.WriteLine(Resources.CreatingCompoundType);
                SdsType typeCompound = SdsTypeBuilder.CreateSdsType<WaveDataCompound>();
                typeCompound.Id = compoundTypeId;
                typeCompound = await metadataService.GetOrCreateTypeAsync(typeCompound).ConfigureAwait(false);

                // create an SdsStream
                Console.WriteLine(Resources.CreatingCompoundStream);
                var streamCompound = new SdsStream
                {
                    Id = streamIdCompound,
                    Name = "Wave Data Sample",
                    TypeId = typeCompound.Id,
                    Description = "This is a sample SdsStream for storing WaveData type measurements",
                };
                streamCompound = await metadataService.GetOrCreateStreamAsync(streamCompound).ConfigureAwait(false);

                // Step 20
                // insert compound data
                Console.WriteLine(Resources.InsertingData);
                await dataService.InsertValueAsync(streamCompound.Id, GetWaveMultiplier(1, 10)).ConfigureAwait(false);
                await dataService.InsertValueAsync(streamCompound.Id, GetWaveMultiplier(2, 2)).ConfigureAwait(false);
                await dataService.InsertValueAsync(streamCompound.Id, GetWaveMultiplier(3, 1)).ConfigureAwait(false);
                await dataService.InsertValueAsync(streamCompound.Id, GetWaveMultiplier(10, 3)).ConfigureAwait(false);
                await dataService.InsertValueAsync(streamCompound.Id, GetWaveMultiplier(10, 8)).ConfigureAwait(false);
                await dataService.InsertValueAsync(streamCompound.Id, GetWaveMultiplier(10, 10)).ConfigureAwait(false);

                var latestCompound = await dataService.GetLastValueAsync<WaveDataCompound>(streamCompound.Id).ConfigureAwait(false);
                var firstCompound = await dataService.GetFirstValueAsync<WaveDataCompound>(streamCompound.Id).ConfigureAwait(false);

                var data = await dataService.GetWindowValuesAsync<WaveDataCompound, int, int>(streamCompound.Id, Tuple.Create(2, 1), Tuple.Create(10, 8)).ConfigureAwait(false);

                Console.WriteLine($"First data: {firstCompound}.  Latest data: {latestCompound}.");

                Console.WriteLine();

                Console.WriteLine(Resources.WindowData);

                foreach (var evnt in data)
                {
                    Console.WriteLine(evnt.ToString());
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);
                _toThrow = ex;
            }
            finally
            {
                // Step 21
                Console.WriteLine();
                Console.WriteLine(Resources.CleaningUp);

                // Delete the stream, types and streamViews making sure
                Console.WriteLine(Resources.DeletingStream);
                await RunInTryCatch(metadataService.DeleteStreamAsync, streamId).ConfigureAwait(false);
                await RunInTryCatch(metadataService.DeleteStreamAsync, streamIdSecondary).ConfigureAwait(false);
                await RunInTryCatch(metadataService.DeleteStreamAsync, streamIdCompound).ConfigureAwait(false);
                Console.WriteLine(Resources.DeletingStreamViews);
                await RunInTryCatch(metadataService.DeleteStreamViewAsync, autoStreamViewId).ConfigureAwait(false);
                await RunInTryCatch(metadataService.DeleteStreamViewAsync, manualStreamViewId).ConfigureAwait(false);
                Console.WriteLine(Resources.DeletingTypes);
                await RunInTryCatch(metadataService.DeleteTypeAsync, typeId).ConfigureAwait(false);
                await RunInTryCatch(metadataService.DeleteTypeAsync, compoundTypeId).ConfigureAwait(false);
                await RunInTryCatch(metadataService.DeleteTypeAsync, targetTypeId).ConfigureAwait(false);
                await RunInTryCatch(metadataService.DeleteTypeAsync, targetIntTypeId).ConfigureAwait(false);

                Console.WriteLine(Resources.Complete);
                if (!test)
                    Console.ReadKey();
            }

            if (test && _toThrow != null)
                throw _toThrow;
            return _toThrow == null;
        }

        /// <summary>
        /// Use this to run a method that you don't want to stop the program if there is an error
        /// </summary>
        /// <param name="methodToRun">The method to run.</param>
        /// <param name="value">The value to put into the method to run</param>
        [System.Diagnostics.CodeAnalysis.SuppressMessage("Design", "CA1031:Do not catch general exception types", Justification = "Sample needs to ensure cleanup, and will throw last error encountered.")]
        private static async Task RunInTryCatch(Func<string, Task> methodToRun, string value)
        {
            try
            {
                await methodToRun(value).ConfigureAwait(false);
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

        private static void PrintStreamViewMapProperties(SdsStreamViewMap sdsStreamViewMap)
        {
            foreach (var prop in sdsStreamViewMap.Properties)
            {
                if (prop.TargetId != null)
                {
                    Console.WriteLine($"{prop.SourceId} => {prop.TargetId}");
                }
                else
                {
                    Console.WriteLine($"{prop.SourceId} => Not Mapped");
                }
            }

            Console.WriteLine();
        }

        private static WaveData GetWave(int order, double multiplier)
        {
            var radians = order * (Math.PI / 32);

            return new WaveData
            {
                Order = order,
                Radians = radians,
                Tau = radians / (2 * Math.PI),
                Sin = multiplier * Math.Sin(radians),
                Cos = multiplier * Math.Cos(radians),
                Tan = multiplier * Math.Tan(radians),
                Sinh = multiplier * Math.Sinh(radians),
                Cosh = multiplier * Math.Cosh(radians),
                Tanh = multiplier * Math.Tanh(radians),
            };
        }

        private static WaveData UpdateWave(WaveData wave, double multiplier)
        {
            wave.Tau = wave.Radians / (2 * Math.PI);
            wave.Sin = multiplier * Math.Sin(wave.Radians);
            wave.Cos = multiplier * Math.Cos(wave.Radians);
            wave.Tan = multiplier * Math.Tan(wave.Radians);
            wave.Sinh = multiplier * Math.Sinh(wave.Radians);
            wave.Cosh = multiplier * Math.Cosh(wave.Radians);
            wave.Tanh = multiplier * Math.Tanh(wave.Radians);

            return wave;
        }

        private static WaveDataCompound GetWaveMultiplier(int order, int multiplier)
        {
            var radians = order * (Math.PI / 32);

            return new WaveDataCompound
            {
                Order = order,
                Radians = radians,
                Tau = radians / (2 * Math.PI),
                Sin = multiplier * Math.Sin(radians),
                Cos = multiplier * Math.Cos(radians),
                Tan = multiplier * Math.Tan(radians),
                Sinh = multiplier * Math.Sinh(radians),
                Cosh = multiplier * Math.Cosh(radians),
                Tanh = multiplier * Math.Tanh(radians),
                Multiplier = multiplier,
            };
        }
    }
}