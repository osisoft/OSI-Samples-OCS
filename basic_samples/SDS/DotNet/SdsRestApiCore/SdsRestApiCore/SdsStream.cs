using System.Collections.Generic;

namespace SdsRestApiCore
{
    [System.Diagnostics.CodeAnalysis.SuppressMessage("Usage", "CA2227:Collection properties should be read only", Justification = "Data Transfer Object (DTO) requires setter")]
    public class SdsStream
    {
        public string Id { get; set; }

        public string Name { get; set; }

        public string Description { get; set; }

        public string TypeId { get; set; }

        public IList<SdsStreamIndex> Indexes { get; set; }

        public SdsInterpolationMode? InterpolationMode { get; set; }

        public SdsExtrapolationMode? ExtrapolationMode { get; set; }

        public IList<SdsStreamPropertyOverride> PropertyOverrides { get; set; }
    }
}
