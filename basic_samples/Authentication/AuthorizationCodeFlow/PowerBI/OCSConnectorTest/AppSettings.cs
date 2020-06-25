using System;
using System.Collections.Generic;
using System.Text;

namespace OCSConnectorTest
{
    public class AppSettings
    {
        public Uri OcsUri { get; set; }
        public string OcsTenantId { get; set; }
        public string Login { get; set; }
        public string Password { get; set; }
    }
}
