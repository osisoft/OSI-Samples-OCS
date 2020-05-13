using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using OSIsoft.Data.Http;
using OSIsoft.Identity;
using OSIsoft.OmfIngress;
using OSIsoft.OmfIngress.Models;

namespace OmfIngressClientLibraries
{
    public class OmfIngressClient
    {
        private readonly IOmfIngressService _omfIngressService;
        private readonly string _tenantId;
        private readonly string _namespaceId;

        public OmfIngressClient(string address, string tenantId, string namespaceId, string clientId, string clientSecret)
        {
            // Get Ingress Services to communicate with server and handle ingress management
            AuthenticationHandler authenticationHandler = new AuthenticationHandler(new Uri(address), clientId, clientSecret);
            _tenantId = tenantId;
            _namespaceId = namespaceId;
            OmfIngressService baseOmfIngressService = new OmfIngressService(new Uri(address), null, HttpCompressionMethod.None, authenticationHandler);
            _omfIngressService = baseOmfIngressService.GetOmfIngressService(tenantId, namespaceId);
        }

        public async Task<OmfConnection> CreateOmfConnectionAsync(string deviceClientId, string connectionName, string destinationNamespaceId)
        {
            // Create a Topic
            Console.WriteLine($"Creating a Topic in Namespace {_namespaceId} for Client with Id {deviceClientId}");
            Console.WriteLine();
            CreateTopic topic = new CreateTopic()
            {
                Name = connectionName,
                Description = "This is a sample Topic",
            };
            topic.ClientIds.Add(deviceClientId);
            Topic createdTopic = await _omfIngressService.CreateTopicAsync(topic).ConfigureAwait(false);
            Console.WriteLine($"Created a Topic with Id {createdTopic.Id}");
            Console.WriteLine();

            // Create a Subscription
            Console.WriteLine($"Creating a Subscription in Namespace {destinationNamespaceId} for Topic with Id {createdTopic.Id}");
            Console.WriteLine();
            CreateSubscription subscription = new CreateSubscription()
            {
                Name = $"{connectionName}-{destinationNamespaceId}",
                Description = "This is a sample Subscription",
                TopicId = createdTopic.Id,
                TopicTenantId = _tenantId,
                TopicNamespaceId = _namespaceId,
            };
            Subscription createdSubscription = await _omfIngressService.CreateSubscriptionAsync(subscription).ConfigureAwait(false);
            Console.WriteLine($"Created a Subscription with Id {createdSubscription.Id}");
            Console.WriteLine();
            OmfConnection omfConnection = new OmfConnection(new List<string> { deviceClientId }, createdTopic, createdSubscription);
            return omfConnection;
        }

        public async Task DeleteOmfConnectionAsync(OmfConnection omfConnection)
        {
            if (omfConnection == null)
            {
                throw new ArgumentException("Omf Connection cannot be null", nameof(omfConnection));
            }

            // Delete the Topic and Subscription
            Console.WriteLine($"Deleting the Subscription with Id {omfConnection.Subscription.Id}");
            Console.WriteLine();

            await _omfIngressService.DeleteSubscriptionAsync(omfConnection.Subscription.Id).ConfigureAwait(false);

            Console.WriteLine($"Deleted the Subscription with Id {omfConnection.Subscription.Id}");
            Console.WriteLine();

            // Delete the Topic
            Console.WriteLine($"Deleting the Topic with Id {omfConnection.Topic.Id}");
            Console.WriteLine();

            await _omfIngressService.DeleteTopicAsync(omfConnection.Topic.Id).ConfigureAwait(false);

            Console.WriteLine($"Deleted the Topic with Id {omfConnection.Topic.Id}");
            Console.WriteLine();
        }
    }
}
