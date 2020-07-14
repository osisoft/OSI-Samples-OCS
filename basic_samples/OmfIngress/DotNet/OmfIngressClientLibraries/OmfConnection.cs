using System.Collections.Generic;
using OSIsoft.OmfIngress.Models;

namespace OmfIngressClientLibraries
{
    public class OmfConnection
    {
        public OmfConnection(List<string> clientIds, Topic topic, Subscription subscription)
        {
            ClientIds = clientIds;
            Topic = topic;
            Subscription = subscription;
        }

        public List<string> ClientIds { get; }
        public Topic Topic { get; set; }
        public Subscription Subscription { get; set; }
    }
}
