using System;
using System.Text.Json.Serialization;

public partial class MembersResponse
{
    public class MembersData
    {
        [JsonPropertyName("id")]
        public string id { get; set; }

        [JsonPropertyName("account")]
        public string? account { get; set; }

        [JsonPropertyName("name")]
        public string? name { get; set; }

        [JsonPropertyName("ip")]
        public string? ip { get; set; }

        [JsonPropertyName("userAgent")]
        public string? userAgent { get; set; }

        [JsonPropertyName("type")]
        public string? type { get; set; }

        [JsonPropertyName("createdAt")]
        public DateTime? createdAt { get; set; }

        [JsonPropertyName("lastConnectedAt")]
        public DateTime? lastConnectedAt { get; set; }
    }

}