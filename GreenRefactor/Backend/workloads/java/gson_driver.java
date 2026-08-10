import com.google.gson.Gson;
import com.google.gson.JsonArray;

public class GsonDriver {
    public static void main(String[] args) {
        String jsonInput = "[{\"id\":1,\"name\":\"Alice\",\"isActive\":true,\"roles\":[\"admin\",\"user\"],\"metadata\":{\"lastLogin\":\"2023-01-01\",\"score\":95.5}},{\"id\":2,\"name\":\"Bob\",\"isActive\":false,\"roles\":[\"user\"],\"metadata\":{\"lastLogin\":\"2023-01-02\",\"score\":82.1}},{\"id\":3,\"name\":\"Charlie\",\"isActive\":true,\"roles\":[\"admin\"],\"metadata\":{\"lastLogin\":\"2023-01-03\",\"score\":70.0}},{\"id\":4,\"name\":\"David\",\"isActive\":false,\"roles\":[\"user\",\"moderator\"],\"metadata\":{\"lastLogin\":\"2023-01-04\",\"score\":88.8}},{\"id\":5,\"name\":\"Eve\",\"isActive\":true,\"roles\":[\"admin\"],\"metadata\":{\"lastLogin\":\"2023-01-05\",\"score\":99.9}}]";
        Gson gson = new Gson();
        String lastOutput = "";
        
        for (int i = 0; i < 20000; i++) {
            JsonArray parsed = gson.fromJson(jsonInput, JsonArray.class);
            lastOutput = gson.toJson(parsed);
        }
        System.out.println("Result length: " + lastOutput.length());
    }
}
