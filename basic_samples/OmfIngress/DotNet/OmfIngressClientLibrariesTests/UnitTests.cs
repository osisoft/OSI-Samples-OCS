using System;
using System.Diagnostics;
using System.Net;
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
                await PollUntilTrueAsync(async () =>
                {
                    try
                    {
                        firstValueForStream = await sdsDataService.GetFirstValueAsync<DataPointType>(Program.StreamId).ConfigureAwait(false);
                        return firstValueForStream != null;
                    }
                    catch
                    {
                        return false;
                    }
                }, TimeSpan.FromSeconds(180), TimeSpan.FromSeconds(1)).ConfigureAwait(false);
                Assert.NotNull(firstValueForStream);
            }
            finally
            {
                // Delete the Type and Stream
                await Program.DeleteTypeAndContainerAsync().ConfigureAwait(false);

                // Verify the Type was successfully deleted in Sds
                bool deleted = await PollUntilTrueAsync(async () =>
                {
                    try
                    {
                        SdsType sdsType = await sdsMetadataService.GetTypeAsync("DataPointType").ConfigureAwait(false);
                        return false;
                    }
                    catch (Exception ex) when (ex is SdsHttpClientException sdsHttpClientException
                        && sdsHttpClientException.StatusCode == HttpStatusCode.NotFound)
                    {
                        return true;
                    }
                    catch
                    {
                        return false;
                    }
                }, TimeSpan.FromSeconds(180), TimeSpan.FromSeconds(1)).ConfigureAwait(false);
                Assert.True(deleted);

                await Program.DeleteOmfConnectionAsync(omfConnection).ConfigureAwait(false);
            }
        }

        private static async Task<bool> PollUntilTrueAsync(Func<Task<bool>> condition, TimeSpan timeout, TimeSpan waitBetweenPolls)
        {
            Stopwatch sw = Stopwatch.StartNew();

            while (sw.Elapsed < timeout)
            {
                if (await condition.Invoke().ConfigureAwait(false))
                {
                    return true;
                }

                await Task.Delay(waitBetweenPolls).ConfigureAwait(false);
            }

            return false;
        }
    }
}
