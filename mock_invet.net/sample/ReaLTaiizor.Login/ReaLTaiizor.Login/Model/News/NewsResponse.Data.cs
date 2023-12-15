using System.Collections.Generic;
using System.Text.Json.Serialization;

public partial class NewsResponse
{
    public class Data
    {
        [JsonPropertyName("newsData")]
        public List<NewsData> newsData { get; set; }

        [JsonPropertyName("totalItems")]
        public int? totalItems { get; set; }

        [JsonPropertyName("totalPages")]
        public int? totalPages { get; set; }

        [JsonPropertyName("currentPage")]
        public int? currentPage { get; set; }


    }
}