using System.Collections.Generic;
using System.Text.Json.Serialization;

public partial class MembersResponse
{
    [JsonPropertyName("status")]
    public string status { get; set; }

    [JsonPropertyName("message")]
    public object message { get; set; }

    [JsonPropertyName("data")]
    public Data data { get; set; }
}