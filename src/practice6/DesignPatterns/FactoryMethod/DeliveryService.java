package practice6.DesignPatterns.FactoryMethod;

/*
Реализация порождающего паттерна Factory Method.
 */

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.Map;

abstract public class DeliveryService {
    private LocalDateTime orderDate;
    private String deliveryName;
    private Map<String, Double> stock = new LinkedHashMap<>();
    private final Map<String, Integer> order = new LinkedHashMap<>();
    private final ArrayList<String> notInStock = new ArrayList<>();

    abstract public void createOrder(Map<String, Integer> order);

    public void setStock(Map<String, Double> stock) {
        this.stock = stock;
    }

    public void setOrder(Map<String, Integer> order) {
        notInStock.clear();
        this.order.clear();

        for (Map.Entry<String, Integer> entry : order.entrySet()) {
            if (stock.containsKey(entry.getKey())) {
                this.order.put(entry.getKey(), entry.getValue());
            } else {
                notInStock.add(entry.getKey());
            }
        }
        this.orderDate = LocalDateTime.now();
    }

    public double getTotalPrice() {
        double price = 0.0;
        for (Map.Entry<String, Integer> entry : order.entrySet()) {
            price += entry.getValue() * stock.get(entry.getKey());
        }
        return price;
    }

    public void setDeliveryName(String deliveryName) {
        this.deliveryName = deliveryName;
    }

    private String deliver() {
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("dd.MM.yyyy HH:mm:ss");
        StringBuilder sb = new StringBuilder(deliveryName);
        sb.append(String.format("%nСоздан: %s%n", orderDate.format(formatter)));
        sb.append("Ваш заказ:\n");
        sb.append(String.format("%-20s %-12s %-10s%n", "Товар", "Количество", "Цена (в рублях)"));

        for (Map.Entry<String, Integer> entry : order.entrySet()) {
            double price = entry.getValue() * stock.get(entry.getKey());
            sb.append(String.format("%-20s %-12d %-10.2f%n", entry.getKey(), entry.getValue(), price));
        }
        if (!notInStock.isEmpty()) {
            sb.append("\nВ наличии не было: ").append(String.join(", ", notInStock)).append("\n");
        }
        sb.append(String.format("\nИтог: %.2f рублей\nДоставим за 2 часа", getTotalPrice()));
        return sb.toString();
    }


    @Override
    public String toString() {
        return this.deliver();
    }
}
