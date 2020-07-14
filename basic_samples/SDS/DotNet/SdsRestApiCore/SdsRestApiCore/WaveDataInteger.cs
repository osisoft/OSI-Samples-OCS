using System.ComponentModel.DataAnnotations;
using System.Text;

namespace SdsRestApiCore
{
    public class WaveDataInteger
    {
        [Key]
        public int OrderTarget { get; set; }

        public int SinInt { get; set; }

        public int CosInt { get; set; }

        public int TanInt { get; set; }

        public override string ToString()
        {
            var builder = new StringBuilder();
            builder.Append($"OrderTarget: {OrderTarget}");
            builder.Append($", SinInt: {SinInt}");
            builder.Append($", CosInt: {CosInt}");
            builder.Append($", TanInt: {TanInt}");
            return builder.ToString();
        }
    }
}
