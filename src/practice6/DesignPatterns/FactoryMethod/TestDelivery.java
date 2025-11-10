package practice6.DesignPatterns.FactoryMethod;

/*
Тестовый класс для DeliveryService. Можно реализовать ввод с клавиатуры (при необходимости)
 */

import java.util.LinkedHashMap;
import java.util.Map;

public class TestDelivery {
    public static void main(String[] args) {
        Map<String, Integer> pizzaOrder;
        Map<String, Integer> groceryOrder = new LinkedHashMap<>();
        DeliveryService pizzaDelivery = new PizzaDelivery();
        DeliveryService groceryDelivery = new GroceryDelivery();

        pizzaDelivery.setStock(Map.of(
                "Маргарита", 380.0,
                "Пепперони", 470.0,
                "Четыре сыра", 550.0,
                "Спрайт 0.5л", 110.0,
                "Соус сырный", 60.0
        ));
        pizzaOrder = Map.of(
                "Пепперони", 1,
                "Спрайт 0.5л", 2,
                "Соус сырный", 2
        );

        groceryDelivery.setStock(Map.of(
                "Яблоки (1 кг)", 135.0,
                "Бананы (1 кг)", 110.0,
                "Картофель (1 кг)", 55.0,
                "Помидоры (1 кг)", 150.0,
                "Огурцы (1 кг)", 145.0,
                "Молоко 1л", 85.0,
                "Хлеб ржаной", 50.0,
                "Яйца (10 шт.)", 95.0,
                "Сыр гауда (1 кг)", 720.0,
                "Индейка (1 кг)", 320.0
        ));
        groceryOrder = Map.of(
                "Бананы (1 кг)", 3,
                "Молоко 1л", 2,
                "Хлеб ржаной", 2,
                "Индейка (1 кг)", 1,
                "Лимонад", 1
        );


        pizzaDelivery.createOrder(pizzaOrder);
        groceryDelivery.createOrder(groceryOrder);
        System.out.println(pizzaDelivery + "\n");
        System.out.println(groceryDelivery);


    }
}
