using System.Collections.Generic;

namespace SdsRestApiCore
{
    [System.Diagnostics.CodeAnalysis.SuppressMessage("Usage", "CA2227:Collection properties should be read only", Justification = "Data Transfer Object (DTO) requires setter")]
    public class SdsType
    {
        public string Id { get; set; }

        public string Name { get; set; }

        public string Description { get; set; }

        public SdsTypeCode SdsTypeCode { get; set; }

        public IList<SdsTypeProperty> Properties { get; set; }
    }
}
