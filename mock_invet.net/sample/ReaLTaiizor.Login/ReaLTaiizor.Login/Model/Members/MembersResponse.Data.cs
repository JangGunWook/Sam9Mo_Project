using System.Collections.Generic;
using System.Text.Json.Serialization;

public partial class MembersResponse
{
    public class Data
    {
        [JsonPropertyName("membersData")]
        public List<MembersData> membersData { get; set; }

        [JsonPropertyName("totalItems")]
        public int? totalItems { get; set; }

        [JsonPropertyName("totalPages")]
        public int? totalPages { get; set; }

        [JsonPropertyName("currentPage")]
        public int? currentPage { get; set; }
    }

}