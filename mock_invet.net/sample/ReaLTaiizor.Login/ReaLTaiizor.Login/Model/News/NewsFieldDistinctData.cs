using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Text.Json.Serialization;
using System.Threading.Tasks;

public class NewsFieldDistinctData
{
    [JsonPropertyName("status")]
    public string status { get; set; }

    [JsonPropertyName("message")]
    public object message { get; set; }

    [JsonPropertyName("data")]
    public Data data { get; set; }

    public class Data
    {
        [JsonPropertyName("stockCompany")]
        public string[] stockCompany { get; set; }
        [JsonPropertyName("newsCategory")]
        public string[] newsCategory { get; set; }
        [JsonPropertyName("newsYear")]
        public string[] newsYear { get; set; }
        [JsonPropertyName("newsMonth")]
        public string[] newsMonth { get; set; }
        [JsonPropertyName("newsDay")]
        public string[] newsDay { get; set; }
    }
}
