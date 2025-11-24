package practice8.NoteHttpServer;

import java.io.*;
import java.net.*;
import java.nio.charset.StandardCharsets;
import java.util.*;

public class NoteHttpServer {
    private static final int PORT = 8080;
    private static final List<String> notes = new ArrayList<>();

    public static void main(String[] args) {
        try (ServerSocket serverSocket = new ServerSocket(PORT)) {
            System.out.println("Note HTTP Server started on port " + PORT);
            
            while (true) {
                try (Socket client = serverSocket.accept()) {
                    handleRequest(client);
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private static void handleRequest(Socket client) throws IOException {
        BufferedReader in = new BufferedReader(new InputStreamReader(client.getInputStream()));
        PrintWriter out = new PrintWriter(client.getOutputStream(), true);

        String requestLine = in.readLine();
        if (requestLine == null) return;

        // Skip headers
        while (in.readLine() != null && !in.readLine().isEmpty());

        String[] parts = requestLine.split(" ");
        String method = parts[0];
        String path = parts[1];

        String response = routeRequest(method, path);
        out.print(response);
    }

    private static String routeRequest(String method, String path) {
        if (method.equals("GET") && path.equals("/notes")) {
            return buildNotesPage();
        }
        
        if (method.equals("POST") && path.equals("/add")) {
            notes.add("New note");
            return buildResponse(200, "Note added");
        }
        
        if (method.equals("POST") && path.equals("/remove")) {
            if (!notes.isEmpty()) {
                notes.remove(notes.size() - 1);
                return buildResponse(200, "Note removed");
            }
            return buildResponse(400, "No notes to remove");
        }
        
        if (method.equals("POST") && path.startsWith("/edit")) {
            return handleEdit(path);
        }
        
        return buildResponse(404, "Not Found");
    }

    private static String handleEdit(String path) {
        Map<String, String> params = parseQuery(path);
        
        int index = parseInt(params.get("index"));
        String text = params.get("text");

        if (index < 0 || index >= notes.size() || text == null || text.isEmpty()) {
            return buildResponse(400, "Invalid parameters");
        }

        notes.set(index, text);
        return buildResponse(200, "Note updated");
    }

    private static Map<String, String> parseQuery(String path) {
        Map<String, String> params = new HashMap<>();
        
        if (!path.contains("?")) return params;

        String query = path.split("\\?")[1];
        for (String param : query.split("&")) {
            String[] kv = param.split("=", 2);
            String key = URLDecoder.decode(kv[0], StandardCharsets.UTF_8);
            String value = kv.length > 1 ? URLDecoder.decode(kv[1], StandardCharsets.UTF_8) : "";
            params.put(key, value);
        }
        
        return params;
    }

    private static int parseInt(String value) {
        try {
            return value != null ? Integer.parseInt(value) : -1;
        } catch (NumberFormatException e) {
            return -1;
        }
    }

    private static String buildNotesPage() {
        StringBuilder html = new StringBuilder("<html><body><h1>Notes</h1><ul>");
        for (String note : notes) {
            html.append("<li>").append(note).append("</li>");
        }
        html.append("</ul></body></html>");
        
        return "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + html;
    }

    private static String buildResponse(int code, String message) {
        String status = code == 200 ? "OK" : code == 400 ? "Bad Request" : "Not Found";
        return String.format("HTTP/1.1 %d %s\r\nContent-Type: text/html\r\n\r\n<html><body><h1>%s</h1></body></html>", 
                           code, status, message);
    }
}