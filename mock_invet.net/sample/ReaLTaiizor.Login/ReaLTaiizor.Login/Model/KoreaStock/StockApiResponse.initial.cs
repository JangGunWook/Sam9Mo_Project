using System.Text.Json.Serialization;

public partial class StockApiResponse
{
    public class InitialProperty
    {
        [JsonPropertyName("prdy_vrss")]
        public string prdy_vrss { get; set; }

        [JsonPropertyName("prdy_vrss_sign")]
        public string prdy_vrss_sign { get; set; }

        [JsonPropertyName("prdy_ctrt")]
        public string prdy_ctrt { get; set; }

        [JsonPropertyName("stck_prdy_clpr")]
        public string stck_prdy_clpr { get; set; }

        [JsonPropertyName("acml_vol")]
        public string acml_vol { get; set; }

        [JsonPropertyName("acml_tr_pbmn")]
        public string acml_tr_pbmn { get; set; }

        [JsonPropertyName("hts_kor_isnm")]
        public string hts_kor_isnm { get; set; }

        [JsonPropertyName("stck_prpr")]
        public string stck_prpr { get; set; }

        [JsonPropertyName("stck_shrn_iscd")]
        public string stck_shrn_iscd { get; set; }

        [JsonPropertyName("prdy_vol")]
        public string prdy_vol { get; set; }

        [JsonPropertyName("stck_mxpr")]
        public string stck_mxpr { get; set; }

        [JsonPropertyName("stck_llam")]
        public string stck_llam { get; set; }

        [JsonPropertyName("stck_oprc")]
        public string stck_oprc { get; set; }

        [JsonPropertyName("stck_hgpr")]
        public string stck_hgpr { get; set; }

        [JsonPropertyName("stck_lwpr")]
        public string stck_lwpr { get; set; }

        [JsonPropertyName("stck_prdy_oprc")]
        public string stck_prdy_oprc { get; set; }

        [JsonPropertyName("stck_prdy_hgpr")]
        public string stck_prdy_hgpr { get; set; }

        [JsonPropertyName("stck_prdy_lwpr")]
        public string stck_prdy_lwpr { get; set; }

        [JsonPropertyName("askp")]
        public string askp { get; set; }

        [JsonPropertyName("bidp")]
        public string bidp { get; set; }

        [JsonPropertyName("prdy_vrss_vol")]
        public string prdy_vrss_vol { get; set; }

        [JsonPropertyName("vol_tnrt")]
        public string vol_tnrt { get; set; }

        [JsonPropertyName("stck_fcam")]
        public string stck_fcam { get; set; }

        [JsonPropertyName("lstn_stcn")]
        public string lstn_stcn { get; set; }

        [JsonPropertyName("cpfn")]
        public string cpfn { get; set; }

        [JsonPropertyName("hts_avls")]
        public string hts_avls { get; set; }

        [JsonPropertyName("per")]
        public string per { get; set; }

        [JsonPropertyName("eps")]
        public string eps { get; set; }

        [JsonPropertyName("pbr")]
        public string pbr { get; set; }

        [JsonPropertyName("itewhol_loan_rmnd_ratem name")]
        public string itewhol_loan_rmnd_ratemname { get; set; }

        [JsonPropertyName("COMPANY")]
        public string COMPANY { get; set; }
    }
}
