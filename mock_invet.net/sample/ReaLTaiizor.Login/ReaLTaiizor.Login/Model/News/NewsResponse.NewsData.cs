using System.Text.Json.Serialization;

public partial class NewsResponse
{
    public class NewsData
    {
        [JsonPropertyName("id")]
        public string id { get; set; }

        [JsonPropertyName("newsYear")]
        public string newsYear { get; set; }

        [JsonPropertyName("newsMonth")]
        public string newsMonth { get; set; }

        [JsonPropertyName("newsDay")]
        public string newsDay { get; set; }

        [JsonPropertyName("newsId")]
        public string newsId { get; set; }

        [JsonPropertyName("newsCompany")]
        public string newsCompany { get; set; }

        [JsonPropertyName("newsCategory")]
        public string newsCategory { get; set; }

        [JsonPropertyName("newsLink")]
        public string newsLink { get; set; }

        [JsonPropertyName("newsImg")]
        public string newsImg { get; set; }

        [JsonPropertyName("newsTitle")]
        public string newsTitle { get; set; }

        [JsonPropertyName("stockCompany")]
        public string stockCompany { get; set; }

        [JsonPropertyName("newsTime")]
        public string newsTime { get; set; }

        [JsonPropertyName("contentSummary")]
        public string contentSummary { get; set; }

        [JsonPropertyName("keyword")]
        public string keyword { get; set; }

        [JsonPropertyName("newsSentiment")]
        public string newsSentiment { get; set; }

        [JsonPropertyName("dataInputTime")]
        public string dataInputTime { get; set; }

        [JsonPropertyName("newsContent")]
        public string newsContent { get; set; }

        public int page { get; set; }
    }
}