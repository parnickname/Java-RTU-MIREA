package practice8.ContactHttpServer;

import java.io.*;
import java.net.*;
import java.nio.charset.StandardCharsets;
import java.util.*;

public class ContactHttpServer {
    private static final int PORT = 8080;
    private static final List<Contact> contacts = new ArrayList<>();

    public static void main(String[] args) {
        try (ServerSocket serverSocket = new ServerSocket(PORT)) {
            System.out.println("Contact HTTP Server started on port " + PORT);

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
        String line;
        while ((line = in.readLine()) != null && !line.isEmpty());

        String[] parts = requestLine.split(" ");
        String method = parts[0];
        String path = parts[1];

        String response = routeRequest(method, path);
        out.print(response);
    }

    private static String routeRequest(String method, String path) {
        if (method.equals("GET") && path.equals("/contacts")) {
            return buildContactsPage();
        }

        if (method.equals("POST") && path.startsWith("/add")) {
            return handleAdd(path);
        }

        if (method.equals("POST") && path.startsWith("/remove")) {
            return handleRemove(path);
        }

        if (method.equals("POST") && path.startsWith("/edit")) {
            return handleEdit(path);
        }

        return buildResponse(404, "Not Found");
    }

    private static String handleAdd(String path) {
        Map<String, String> params = parseQuery(path);

        String name = params.get("name");
        String phone = params.get("phone");

        if (name == null || name.isEmpty() || phone == null || phone.isEmpty()) {
            return buildResponse(400, "Name and phone are required");
        }

        contacts.add(new Contact(name, phone));
        return buildResponse(200, "Contact added: " + name);
    }

    private static String handleRemove(String path) {
        Map<String, String> params = parseQuery(path);

        int index = parseInt(params.get("index"));

        if (index < 0 || index >= contacts.size()) {
            return buildResponse(400, "Invalid index");
        }

        Contact removed = contacts.remove(index);
        return buildResponse(200, "Contact removed: " + removed.name);
    }

    private static String handleEdit(String path) {
        Map<String, String> params = parseQuery(path);

        int index = parseInt(params.get("index"));
        String name = params.get("name");
        String phone = params.get("phone");

        if (index < 0 || index >= contacts.size()) {
            return buildResponse(400, "Invalid index");
        }

        if ((name == null || name.isEmpty()) && (phone == null || phone.isEmpty())) {
            return buildResponse(400, "Name or phone required");
        }

        Contact contact = contacts.get(index);
        if (name != null && !name.isEmpty()) {
            contact.name = name;
        }
        if (phone != null && !phone.isEmpty()) {
            contact.phone = phone;
        }

        return buildResponse(200, "Contact updated");
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

    private static String buildContactsPage() {
        StringBuilder html = new StringBuilder("<html><body><h1>Contacts</h1>");

        if (contacts.isEmpty()) {
            html.append("<p>No contacts</p>");
        } else {
            html.append("<table border='1'><tr><th>#</th><th>Name</th><th>Phone</th></tr>");
            for (int i = 0; i < contacts.size(); i++) {
                Contact c = contacts.get(i);
                html.append("<tr><td>").append(i).append("</td>")
                    .append("<td>").append(c.name).append("</td>")
                    .append("<td>").append(c.phone).append("</td></tr>");
            }
            html.append("</table>");
        }

        html.append("</body></html>");
        return "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + html;
    }

    private static String buildResponse(int code, String message) {
        String status = code == 200 ? "OK" : code == 400 ? "Bad Request" : "Not Found";
        return String.format("HTTP/1.1 %d %s\r\nContent-Type: text/html\r\n\r\n<html><body><h1>%s</h1></body></html>",
                           code, status, message);
    }

    private static class Contact {
        String name;
        String phone;

        Contact(String name, String phone) {
            this.name = name;
            this.phone = phone;
        }
    }
}
