using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http.Headers;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
public class HttpClientApi
{
    private HttpClient _client;

    public HttpClientApi(string apiUrl)
    {
        _client = new HttpClient();
        _client.BaseAddress = new Uri(apiUrl);
        _client.DefaultRequestHeaders.Accept.Clear();
        _client.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));
        _client.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", ProgramInformationManager.Instance.AccessToken);
        _client.DefaultRequestHeaders.Add("Refresh-Token", "Bearer " + ProgramInformationManager.Instance.RefreshToken);
        _client.DefaultRequestHeaders.Add("Finance-Agent", "Sam9moFinance/0.0.1");
        _client.Timeout = TimeSpan.FromSeconds(5);
    }

    public async Task<string> actionHttpApi(String method, String myContent, String requetUri)
    {
        HttpResponseMessage? response = null;
        if (method == "POST")
        {
            var buffer = Encoding.UTF8.GetBytes(myContent);
            var byteContent = new ByteArrayContent(buffer);
            byteContent.Headers.ContentType = new MediaTypeHeaderValue("application/json");

            response = await _client.PostAsync(requetUri, byteContent);
        } else if (method == "PUT")
        {
            var buffer = Encoding.UTF8.GetBytes(myContent);
            var byteContent = new ByteArrayContent(buffer);
            byteContent.Headers.ContentType = new MediaTypeHeaderValue("application/json");

            response = await _client.PutAsync(requetUri, byteContent);
        } else if(method == "DELETE")
        {
            var buffer = Encoding.UTF8.GetBytes(myContent);
            var byteContent = new ByteArrayContent(buffer);
            byteContent.Headers.ContentType = new MediaTypeHeaderValue("application/json");

            response = await _client.DeleteAsync(requetUri);
        } else if(method == "GET")
        {
            response = await _client.GetAsync(requetUri);
        }

        if (response.IsSuccessStatusCode)
        {
            HttpHeaders headers = response.Headers;
            IEnumerable<string> values;

            if (headers.TryGetValues("New-Access-Token", out values))
            {
                ProgramInformationManager.Instance.AccessToken = values.First();
            }

            var avail = await response.Content.ReadAsStringAsync().ContinueWith(postTask =>
            {
                return postTask.Result;
            });
            
            return avail;
        }
        return null;
    }

}
