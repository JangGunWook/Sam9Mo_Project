using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Text.Json.Serialization;
using System.Threading.Tasks;

public class SignInResponse
{
    [JsonPropertyName("status")]
    public string status { get; set; }

    [JsonPropertyName("message")]
    public object message { get; set; }

    [JsonPropertyName("data")]
    public Data data { get; set; }

    public class Data
    {
        [JsonPropertyName("name")]
        public string name { get; set; }

        [JsonPropertyName("type")]
        public string type { get; set; }

        [JsonPropertyName("accessToken")]
        public string? accessToken { get; set; }

        [JsonPropertyName("refreshToken")]
        public string? refreshToken { get; set; }

        [JsonPropertyName("lastConnectedTime")]
        public string? lastConnectedTime { get; set; }
    }
}
