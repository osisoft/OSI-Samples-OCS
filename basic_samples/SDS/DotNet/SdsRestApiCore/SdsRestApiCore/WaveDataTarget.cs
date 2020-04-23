using System.ComponentModel.DataAnnotations;
using System.Text;

namespace SdsRestApiCore
{
    public class WaveDataTarget
    {
        [Key]
        public int OrderTarget { get; set; }

        public double TauTarget { get; set; }

        public double RadiansTarget { get; set; }

        public double SinTarget { get; set; }

        public double CosTarget { get; set; }

        public double TanTarget { get; set; }

        public double SinhTarget { get; set; }

        public double CoshTarget { get; set; }

        public double TanhTarget { get; set; }

        public override string ToString()
        {
            var builder = new StringBuilder();
            builder.Append($"OrderTarget: {OrderTarget}");
            builder.Append($", RadiansTarget: {RadiansTarget}");
            builder.Append($", TauTarget: {TauTarget}");
            builder.Append($", SinTarget: {SinTarget}");
            builder.Append($", CosTarget: {CosTarget}");
            builder.Append($", TanTarget: {TanTarget}");
            builder.Append($", SinhTarget: {SinhTarget}");
            builder.Append($", CoshTarget: {CoshTarget}");
            builder.Append($", TanhTarget: {TanhTarget}");
            return builder.ToString();
        }
    }
}
