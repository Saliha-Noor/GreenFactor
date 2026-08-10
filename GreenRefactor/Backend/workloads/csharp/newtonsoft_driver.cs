using System;
using Newtonsoft.Json.Linq;

class NewtonsoftDriver {
    static void Main() {
        string jsonInput = "[{\"id\":1,\"name\":\"Alice\",\"isActive\":true,\"roles\":[\"admin\",\"user\"],\"metadata\":{\"lastLogin\":\"2023-01-01\",\"score\":95.5}},{\"id\":2,\"name\":\"Bob\",\"isActive\":false,\"roles\":[\"user\"],\"metadata\":{\"lastLogin\":\"2023-01-02\",\"score\":82.1}},{\"id\":3,\"name\":\"Charlie\",\"isActive\":true,\"roles\":[\"admin\"],\"metadata\":{\"lastLogin\":\"2023-01-03\",\"score\":70.0}},{\"id\":4,\"name\":\"David\",\"isActive\":false,\"roles\":[\"user\",\"moderator\"],\"metadata\":{\"lastLogin\":\"2023-01-04\",\"score\":88.8}},{\"id\":5,\"name\":\"Eve\",\"isActive\":true,\"roles\":[\"admin\"],\"metadata\":{\"lastLogin\":\"2023-01-05\",\"score\":99.9}}]";
        string lastOutput = "";
        
        for (int i = 0; i < 20000; i++) {
            JArray parsed = JArray.Parse(jsonInput);
            lastOutput = parsed.ToString(Newtonsoft.Json.Formatting.None);
        }
        Console.WriteLine("Result length: " + lastOutput.Length);
    }
}
