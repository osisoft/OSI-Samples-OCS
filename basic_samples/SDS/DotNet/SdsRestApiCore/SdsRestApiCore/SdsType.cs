using System.Collections.Generic;

namespace SdsRestApiCore
{
    public class SdsType
    {
        public string Id { get; set; }

        public string Name { get; set; }

        public string Description { get; set; }

        public SdsTypeCode SdsTypeCode { get; set; }

        public IList<SdsTypeProperty> Properties { get; set; }
    }
}
