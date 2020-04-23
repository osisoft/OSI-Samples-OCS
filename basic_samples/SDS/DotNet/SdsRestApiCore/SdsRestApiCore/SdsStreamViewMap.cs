using System.Collections.Generic;

namespace SdsRestApiCore
{
    [System.Diagnostics.CodeAnalysis.SuppressMessage("Usage", "CA2227:Collection properties should be read only", Justification = "Data Transfer Object (DTO) requires setter")]
    public class SdsStreamViewMap
    {
        public string SourceTypeId { get; set; }

        public string TargetTypeId { get; set; }

        public IList<SdsStreamViewProperty> Properties { get; set; }
    }
}
