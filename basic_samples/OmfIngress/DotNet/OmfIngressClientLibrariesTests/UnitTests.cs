using System;
using System.Diagnostics;
using System.Net;
using System.Threading;
using System.Threading.Tasks;
using OmfIngressClientLibraries;
using OSIsoft.Data;
using OSIsoft.Data.Http;
using OSIsoft.Identity;
using Xunit;

namespace OmfIngressClientLibrariesTests
{
    public class UnitTests
    {
        [Fact]
        [System.Diagnostics.CodeAnalysis.SuppressMessage("Design", "CA1031:Do not catch general exception types", Justification = "Used only for retry logic when waiting for values to return from tests.")]
        public async Task OmfIngressClientLibrariesTest()
        {
            // Setting things up
            Program.Setup();

            // Initializing Sds Service
            ISdsMetadataService sdsMetadataService = SdsService.GetMetadataService(new Uri(Program.Address), Program.TenantId, Program.NamespaceId,
                new AuthenticationHandler(new Uri(Program.Address), Program.ClientId, Program.ClientSecret));
            ISdsDataService sdsDataService = SdsService.GetDataService(new Uri(Program.Address), Program.TenantId, Program.NamespaceId,
                new AuthenticationHandler(new Uri(Program.Address), Program.ClientId, Program.ClientSecret));

            OmfConnection omfConnection = null;

            try
            {
                // Create the Connection, send OMF
                omfConnection = await Program.CreateOmfConnectionAsync().ConfigureAwait(false);
                await Program.SendTypeContainerAndDataAsync().ConfigureAwait(false);

                // Check if Data was successfully stored in Sds
                DataPointType firstValueForStream = null;
                Stopwatch sw = Stopwatch.StartNew();
                while (sw.Elapsed < TimeSpan.FromSeconds(180) && firstValueForStream == null)
                {
                    try
                    {
                        firstValueForStream = await sdsDataService.GetFirstValueAsync<DataPointType>(Program.StreamId).ConfigureAwait(false);
                    }
                    catch { }

                    if (firstValueForStream != null)
                    {
                        break;
                    }
                    else
                    {
                        Thread.Sleep(TimeSpan.FromSeconds(1));
                    }
                }

                Assert.NotNull(firstValueForStream);
            }
            finally
            {
                // Delete the Type and Stream
                await Program.DeleteTypeAndContainerAsync().ConfigureAwait(false);

                // Verify the Type was successfully deleted in Sds
                bool deleted = false;
                Stopwatch sw = Stopwatch.StartNew();
                while (sw.Elapsed < TimeSpan.FromSeconds(180) && !deleted)
                {
                    try
                    {
                        SdsType sdsType = await sdsMetadataService.GetTypeAsync("DataPointType").ConfigureAwait(false);
                    }
                    catch (Exception ex) when (ex is SdsHttpClientException sdsHttpClientException
                        && sdsHttpClientException.StatusCode == HttpStatusCode.NotFound)
                    {
                        deleted = true;
                    }
                    catch { }

                    if (deleted)
                    {
                        break;
                    }
                    else
                    {
                        Thread.Sleep(TimeSpan.FromSeconds(1));
                    }
                }

                Assert.True(deleted);

                await Program.DeleteOmfConnectionAsync(omfConnection).ConfigureAwait(false);
            }
        }
    }
}
