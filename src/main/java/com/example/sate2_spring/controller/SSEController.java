package com.example.sate2_spring.controller;
import org.json.JSONArray;
import org.json.JSONObject;

import com.example.sate2_spring.mapper.StationMapper;
import lombok.var;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.http.codec.ServerSentEvent;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import reactor.core.publisher.Flux;
import java.io.*;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.time.Duration;
import java.util.Arrays;
import java.util.List;
import java.util.Map;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.core.type.TypeReference;
import java.util.List;
import java.util.concurrent.atomic.AtomicInteger;

import com.example.sate2_spring.bean.Station;

import static org.apache.logging.log4j.message.MapMessage.MapFormat.JSON;

@RestController
public class SSEController {
    @Autowired
    private StationMapper stationMapper;
    private Integer Return_Sum=0;
    private Integer Return_Sum2=0;
    // 模拟初始的完整 JSON 数组
    private List<String> initialJsonArray = Arrays.asList(
            "{\"id\":\"document1\",\"name\":\"first\"}",
            "{\"id\":\"document2\",\"name\":\"first\"}",
            "{\"id\":\"document3\",\"name\":\"first\"}"
    );

//    @GetMapping(value = "/SseInterval", produces = "text/event-stream")
//    public ResponseEntity<Flux<String>> Send_Interval3(@RequestParam("StartTime") String startTime,
//                                                      @RequestParam("StopTime") String stopTime,
//                                                      @RequestParam("array") String arrayString) {
//
//        String x=Czml_Interval(startTime,stopTime,arrayString);
//        Flux<String> eventFlux = Flux.just(x);
//
//        return ResponseEntity.ok()
//                .header("Content-Type", "text/event-stream")
//                .header("Cache-Control", "no-cache")
//                .header("Connection", "keep-alive")
//                .header("retry", "1000") // 设置重连时间为1秒
//                .body(eventFlux);
//    }

    //某一时间间隔
    @GetMapping(value = "/SseInterval", produces = "text/event-stream")
    public Flux<ServerSentEvent<String>> Send_Interval(@RequestParam("StartTime") String startTime,
                                                       @RequestParam("StopTime") String stopTime,
                                                       @RequestParam("Systems") String Systems) throws IOException {

        //返回一个 Flux 对象
        return Flux.just(Interval_ServerSentEvent(startTime,stopTime,Systems));

    }
    private ServerSentEvent<String>Interval_ServerSentEvent(String startTime, String stopTime,String Systems) throws IOException {
        //获取服务器中地面站信息
        List<Station> stations=stationMapper.getAllBook();
        String stations_info=stations.toString();
//System.out.println(stations_info);
        //创建czml文件
        String eventData=Czml_Interval(startTime, stopTime,Systems,stations_info);
//      System.out.println(eventData);
//        String xp="[{\"id\": \"document\",\"version\": \"1.0\",\"name\": \"first\",\"clock\": {\"interval\": \"2023-12-26T00:00:00Z/2023-12-27T00:00:00Z\",\"currentTime\": \"2023-12-26T00:00:00Z\",\"multiplier\": 120,\"range\": \"LOOP_STOP\",\"step\": \"SYSTEM_CLOCK_MULTIPLIER\"}}]";
        //ServerSentEvent 对象
        return ServerSentEvent.<String>builder()
                .event("custom-event")
                .id("this is ID")
                .data(eventData)
                .build();
    }
    private String Czml_Interval(String StartTime,String StopTime,String Systems,String stations_info) {

        StringBuilder output = new StringBuilder();
        try {
            String pythonScriptPath = "src/main/resources/static/PythonCode/interval.py";
            String pythonLibPath = "src/main/resources/static/PythonCode/site-packages";
            String[] command = {"python", pythonScriptPath,StartTime,StopTime,Systems,stations_info};

//            String pythonScriptPath = "/usr/local/MyApp/interval.py";
//            String[] command = {"python", pythonScriptPath,StartTime,StopTime,Systems,stations_info};
            ProcessBuilder pb = new ProcessBuilder(command);
            pb.environment().put("PYTHONPATH", pythonLibPath);
            Process process = pb.start();
            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            String line;
            while ((line = reader.readLine()) != null) {

                output.append(line).append("\n");
            }
            int exitCode = process.waitFor();
            System.out.println("Python script exited with code " + exitCode);

        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
        }

        return output.toString();
    }



    //实时
    @GetMapping(value = "/SseRealTime", produces = "text/event-stream")
    public Flux<ServerSentEvent<String>> Send_RealTime(@RequestParam("Systems") String Systems) {
        //返回一个 Flux 对象
        return Flux.interval(Duration.ZERO,Duration.ofMinutes(10))
                .map(sequence -> {
                    try {
                        return CreateServerSentEvent(Systems);
                    } catch (IOException e) {
                        throw new RuntimeException(e);
                    }
                });
    }
    private ServerSentEvent<String>CreateServerSentEvent(String Systems) throws IOException {
        //获取时间
        ReturnTime StartAndStop=GetTime();
        String StartTime = StartAndStop.getStart_time();
        String StopTime = StartAndStop.getStop_time();
        String CurrentTime=StartAndStop.getCurrent_time();
//        System.out.println("this");
        //获取服务器中地面站信息
        List<Station> stations=stationMapper.getAllBook();
        String stations_info=stations.toString();

        //创建czml文件
        String eventData=Czml_RealTime(StartTime,StopTime,CurrentTime,Systems,stations_info);
//      System.out.println(eventData);

        //ServerSentEvent 对象
        return ServerSentEvent.<String>builder()
                .event("custom-event")
                .id("this is ID")
                .data(eventData)
                .build();
    }
    private String Czml_RealTime(String StartTime, String StopTime, String CurrentTime, String systems, String stations_info) throws IOException {
        StringBuilder output = new StringBuilder();
        try {
            String pythonScriptPath = "src/main/resources/static/PythonCode/RealTime.py";
            String pythonLibPath = "src/main/resources/static/PythonCode/site-packages";
            String[] command = {"python", pythonScriptPath, StartTime, StopTime, CurrentTime, systems};
//            String pythonScriptPath = "/usr/local/MyApp/realtime.py";
//            String[] command = {"python", pythonScriptPath, StartTime, StopTime, CurrentTime, systems,stations_info};

            ProcessBuilder pb = new ProcessBuilder(command);
            pb.environment().put("PYTHONPATH", pythonLibPath);
            Process process = pb.start();
            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            String line;
            while ((line = reader.readLine()) != null) {

                output.append(line).append("\n");
            }
            int exitCode = process.waitFor();
            //记录传数据次数
            Return_Sum++;
            //返回码
            System.out.println(Return_Sum+" times Python script exited with code " + exitCode);

        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
        }

        return output.toString();

    }
    public  ReturnTime GetTime() {
        // 获取当前时间
        LocalDateTime now = LocalDateTime.now();
        // 减去 10 分钟
        LocalDateTime Start_Time = now.minusMinutes(10);
        // 减去 10 分钟
        LocalDateTime  Stop_Time= now.plusMinutes(10);
        // 转换为指定格式的字符串
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd'T'HH:mm:ss'Z'");

        String StartTime = Start_Time.format(formatter);
        String StopTime = Stop_Time.format(formatter);
        String CurrentTime=now.format(formatter);
        //返回一个时间类对象
        ReturnTime StartAndStop=new ReturnTime(StartTime,StopTime,CurrentTime);
        return StartAndStop;
    }



    @GetMapping(value = "/Ssetest", produces = "text/event-stream")
    public Flux<ServerSentEvent<String>> Send_Realtime() {
        String arrayString="[GPS]";
        return Flux.interval(Duration.ZERO,Duration.ofMinutes(1))
                .map(sequence -> {
                    try {
                        return CreateServerSentEvent(arrayString);
                    } catch (IOException e) {
                        throw new RuntimeException(e);
                    }
                });
    }
    private String Server_Czml_RealTime(String StartTime,String StopTime,String CurrentTime,String arrayString) throws IOException {
        StringBuilder output = new StringBuilder();
        try {
            String pythonScriptPath = "/usr/local/MyApp/server_realtime.py";
            String[] command = {"python", pythonScriptPath, StartTime, StopTime, CurrentTime, arrayString};
//            String[] command = {"python", pythonScriptPath};

            ProcessBuilder pb = new ProcessBuilder(command);
            Process process = pb.start();
            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            String line;
            while ((line = reader.readLine()) != null) {
                output.append(line).append("\n");
            }
            int exitCode = process.waitFor();

            Return_Sum++;

            System.out.println("Return:" + Return_Sum + "    Python script exited with code " + exitCode);

        } catch (IOException | InterruptedException e) {
            System.err.println("Error message: " + e.getMessage()); // 输出异常消息
            e.printStackTrace(); // 输出异常信息到标准错误流
        }

        return output.toString();
    }



    @GetMapping(value = "/test", produces = "text/event-stream")
    public Flux<ServerSentEvent<String>> tes() {

        return Flux.interval(Duration.ZERO,Duration.ofMinutes(1))
                .map(sequence ->{
                    return testx();
                });
    }
    private ServerSentEvent<String> testx()   {
        List<Station> stations=stationMapper.getAllBook();
        System.out.println(stations.toString());

//        StringBuilder output = new StringBuilder();
//        try {
//            String pythonScriptPath = "src/main/resources/static/PythonCode/test.py";
//            String pythonLibPath = "src/main/resources/static/PythonCode/site-packages";
//            String[] command = {"python", pythonScriptPath, stations.toString()};
//            ProcessBuilder pb = new ProcessBuilder(command);
//            pb.environment().put("PYTHONPATH", pythonLibPath);
//            Process process = pb.start();
//            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
//            String line;
//            while ((line = reader.readLine()) != null) {
//
//                output.append(line).append("\n");
//            }
//            int exitCode = process.waitFor();
//            Return_Sum++;
//            System.out.println(Return_Sum+" times Python script exited with code " + exitCode);
//
//        } catch (IOException | InterruptedException e) {
//            e.printStackTrace();
//        }
//        System.out.println(output.toString());
        return ServerSentEvent.<String>builder()
                .event("custom-event")
                .id("this is ID")
                .data("eventData")
                .build();
    }


    @GetMapping("/datax")
    public String getData(@RequestParam Map<String, String> allParams) {
        System.out.println(allParams);
        // 遍历参数或根据键获取特定参数
//        String start_time = allParams.get("stop_time");
//        String stop_time= allParams.get("stop_time");
//        System.out.println(start_time);
//        System.out.println(stop_time);
        // ...处理参数

        return "Received all parameters";
    }

    @GetMapping(value = "/data", produces = "text/event-stream")
    public Flux<ServerSentEvent<String>> tesx(@RequestParam Map<String, String> allParams) throws IOException {
        String startTime = allParams.get("start_time");
        String stopTime= allParams.get("stop_time");
        String Systems=allParams.get("checkList");
        String color1=allParams.get("color1");
        String color2=allParams.get("color2");
        String width1=allParams.get("width1");
        String width2=allParams.get("width2");
        String tle=allParams.get("tle");
//        System.out.println(allParams);
        //返回一个 Flux 对象
        return Flux.just(Interval_ServerSentEvent(startTime,stopTime,Systems,color1,color2,width1,width2,tle));
    }
    private ServerSentEvent<String> testxx()   {
        String eventData="ssss";
        return ServerSentEvent.<String>builder()
                .event("custom-event")
                .id("this is ID")
                .data(eventData)
                .build();
    }


    private ServerSentEvent<String>Interval_ServerSentEvent(String startTime, String stopTime,String Systems,
                                                            String color1,String color2,String width1,String width2,String tle) throws IOException {
        //获取服务器中地面站信息
        List<Station> stations=stationMapper.getAllBook();
        String stations_info=stations.toString();
//System.out.println(stations_info);
        //创建czml文件
        String eventData=Czml_Interval(startTime, stopTime,Systems,stations_info,
               color1,color2,width1,width2,tle);
//      System.out.println(startTime+stopTime+Systems+stations_info+
//              color1+color2+width1+width2+tle);
//        System.out.println(eventData);
//        String xp="[{\"id\": \"document\",\"version\": \"1.0\",\"name\": \"first\",\"clock\": {\"interval\": \"2023-12-26T00:00:00Z/2023-12-27T00:00:00Z\",\"currentTime\": \"2023-12-26T00:00:00Z\",\"multiplier\": 120,\"range\": \"LOOP_STOP\",\"step\": \"SYSTEM_CLOCK_MULTIPLIER\"}}]";
        //ServerSentEvent 对象
        return ServerSentEvent.<String>builder()
                .event("custom-event")
                .id("this is ID")
                .data(eventData)
                .build();
    }
    private String Czml_Interval(String StartTime,String StopTime,String Systems,String stations_info,
                                 String color1,String color2,String width1,String width2,String tle) {

        StringBuilder output = new StringBuilder();
        try {
            String pythonScriptPath = "src/main/resources/static/PythonCode/interval.py";
            String pythonLibPath = "src/main/resources/static/PythonCode/site-packages";
            String[] command = {"python", pythonScriptPath,StartTime,StopTime,Systems,stations_info,
                    color1,color2,width1,width2,tle};

//            String pythonScriptPath = "/usr/local/MyApp/interval.py";
//            String[] command = {"python", pythonScriptPath,StartTime,StopTime,Systems,stations_info};
            ProcessBuilder pb = new ProcessBuilder(command);
            pb.environment().put("PYTHONPATH", pythonLibPath);
            Process process = pb.start();
            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            String line;
            while ((line = reader.readLine()) != null) {

                output.append(line).append("\n");
            }
            int exitCode = process.waitFor();
            System.out.println("Python script exited with code " + exitCode);

        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
        }

        return output.toString();
    }


    //实时
    @GetMapping(value = "/dataSseRealTime", produces = "text/event-stream")
    public Flux<ServerSentEvent<String>> Send_RealTime(@RequestParam Map<String, String> allParams) throws IOException {
        String Systems=allParams.get("checkList");
        String color1=allParams.get("color1");
        String color2=allParams.get("color2");
        String width1=allParams.get("width1");
        String width2=allParams.get("width2");
        String tle=allParams.get("tle");
        Return_Sum=0;
        Return_Sum2=0;
        AtomicInteger x = new AtomicInteger(0);
        String eventdata=CreateServerSentEvent(Systems,color1,color2,width1,width2,tle);
        System.out.println(eventdata);
//        JSONObject jsonObject =  JSON.parseObject(tt);
        JSONArray jsonArray1 = new JSONArray(eventdata);

        return Flux.interval(Duration.ZERO, Duration.ofMinutes(2))
                .flatMap(sequence -> {
                    if(Return_Sum2==0){
                        Return_Sum2++;
                        LocalDateTime currentDateTime = LocalDateTime.now();
                        System.out.println("first---------"+ currentDateTime);
                        System.out.println(Return_Sum2);
                        return  Flux.just(ServerSentEvent.<String>builder()
                                .event("custom-event")
                                .id("this is ID")
                                .data("firstpacket"+jsonArray1.toString())
                                .build()
                        );
                    }
                    return Flux.fromIterable(jsonArray1)
                            .zipWith(Flux.interval(Duration.ofSeconds(1)), (data, timer) -> {
                                try {
                                    System.out.println(data.toString());
                                    // 在这里对每个元素执行你的操作，例如调用 Ctest 方法
                                    if (timer== 0) {
                                        return Ctest("Realstart" + data, x);
                                    } else if (timer == jsonArray1.length() - 1) {
                                        return Ctest("Realend" + data, x);
                                    } else {
                                        return Ctest(data.toString(), x);
                                    }
                                } catch (IOException e) {
                                    throw new RuntimeException(e);
                                }
                            });
                });
    }
    private String CreateServerSentEvent(String Systems,String color1,String color2,String width1,
                                                         String width2,String tle) throws IOException {
        //获取时间
        ReturnTime StartAndStop=GetTime();
        String StartTime = StartAndStop.getStart_time();
        String StopTime = StartAndStop.getStop_time();
        String CurrentTime=StartAndStop.getCurrent_time();
//        System.out.println("this");
        //获取服务器中地面站信息
        List<Station> stations=stationMapper.getAllBook();
        String stations_info=stations.toString();

        //创建czml文件
        String eventData=Czml_RealTime(StartTime,StopTime,CurrentTime,Systems,stations_info,
                color1,color2,width1,width2,tle);

        return eventData;

    }

    private String Czml_RealTime(String StartTime, String StopTime, String CurrentTime, String systems, String stations_info,
                                 String color1,String color2,String width1,String width2,String tle) throws IOException {
        StringBuilder output = new StringBuilder();
        try {
            String pythonScriptPath = "src/main/resources/static/PythonCode/realTime.py";
            String pythonLibPath = "src/main/resources/static/PythonCode/site-packages";
            String[] command = {"python", pythonScriptPath, StartTime, StopTime, CurrentTime, systems,stations_info,
                    color1,color2,width1,width2,tle};
//            String pythonScriptPath = "/usr/local/MyApp/realtime.py";
//            String[] command = {"python", pythonScriptPath, StartTime, StopTime, CurrentTime, systems,stations_info};

            ProcessBuilder pb = new ProcessBuilder(command);
            pb.environment().put("PYTHONPATH", pythonLibPath);
            Process process = pb.start();
            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            String line;
            while ((line = reader.readLine()) != null) {

                output.append(line).append("\n");
            }
            int exitCode = process.waitFor();
            //记录传数据次数
            Return_Sum++;
            //返回码
            System.out.println(Return_Sum+" times Python script exited with code " + exitCode);

        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
        }

        return output.toString();

    }

//    @GetMapping(value = "/datatest", produces = "text/event-stream")
//    public Flux<ServerSentEvent<String>> Send_RealTimexx() {
//    @GetMapping(value = "/dataStream", produces = "text/event-stream")
//    public  Flux<ServerSentEvent<String>>sendDataStream() {
//        Return_Sum = 0;
//
//        AtomicInteger x = new AtomicInteger(0);
//        System.out.println(1111);
//        return Flux.interval(Duration.ZERO, Duration.ofMinutes(1))
//                .flatMap(sequence -> {
//                    return Flux.interval(Duration.ofSeconds(3))
//                            .zipWith(Flux.fromIterable(initialJsonArray), (time, data) -> {
//                                try {
//                                    return Ctest(data,x);
//                                } catch (IOException e) {
//                                    throw new RuntimeException(e);
//                                }
//                            });
//                });
//
//    }

    private ServerSentEvent<String>Ctest(String  data, AtomicInteger x) throws IOException {
//        System.out.println(data);
//        ObjectMapper objectMapper = new ObjectMapper();
        // 将 JSON 字符串转换为 Java 对象
//        Object jsonObject = objectMapper.readValue(data, Object.class);
//        String su="[{\"id\":\"document1\",\"name\":\"first\"},{\"id\":\"document2\",\"name\":\"first\"},{\"id\":\"document3\",\"name\":\"first\"}]";
//        System.out.println(su);
        // 将 JSON 字符串转换为 Map 对象
//        Map<String, Object> jsonMap = objectMapper.readValue(data, Map.class);


        LocalDateTime currentDateTime = LocalDateTime.now();
        System.out.println( currentDateTime+"----"+x);
        x.incrementAndGet();
//        System.out.println(currentDateTime+"----"+(String)jsonMap.get("id"));
        String eventData=data;
        if(Return_Sum==0){
            Return_Sum++;
            //ServerSentEvent 对象
            return ServerSentEvent.<String>builder()
                    .event("custom-event")
                    .id("this is ID")
                    .data(eventData)
                    .build();
        }
        else {
            //ServerSentEvent 对象
            return ServerSentEvent.<String>builder()
                    .event("custom-event")
                    .id("this is ID")
                    .data(eventData)
                    .build();
        }

    }



}