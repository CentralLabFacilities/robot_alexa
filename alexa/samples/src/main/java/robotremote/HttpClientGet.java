package robotremote;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import org.apache.http.HttpResponse;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.DefaultHttpClient;

public class HttpClientGet {

    public DefaultHttpClient httpClient;

    public HttpClientGet() {
        httpClient = new DefaultHttpClient();
	}

  public String getContent(String url){
   try {
        HttpGet getRequest = new HttpGet(url);
        getRequest.addHeader("accept", "application/json");

        HttpResponse response = httpClient.execute(getRequest);

        if (response.getStatusLine().getStatusCode() != 200) {
            throw new RuntimeException("Failed : HTTP error code : "
               + response.getStatusLine().getStatusCode());
        }

        BufferedReader br = new BufferedReader(
                         new InputStreamReader((response.getEntity().getContent())));

        String output;
        System.out.println("Output from Server .... \n");
        while ((output = br.readLine()) != null) {
            System.out.println(output);
        }

        // httpClient.getConnectionManager().shutdown();
        return output;


   } catch (ClientProtocolException e) {
        e.printStackTrace();
        return null;

   } catch (IOException e) {
        e.printStackTrace();
        return null;
  }
}

}