using System.Collections.Generic;

namespace SdsRestApiCore
{
    public class SdsStreamViewMap
    {
        public string SourceTypeId { get; set; }

        public string TargetTypeId { get; set; }

        public IList<SdsStreamViewProperty> Properties { get; set; }
    }
}
