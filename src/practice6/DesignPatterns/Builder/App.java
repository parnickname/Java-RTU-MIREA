package practice6.DesignPatterns.Builder;

public class App {
    public static void main(String[] args) {
        Order order1 = new Order.OrderBuilder().setDrink("Латте").build();

        Order order2 = new Order.OrderBuilder().setMainCourse("Стейк филе-миньон medium").setSideDish("овощи гриль с тимьяном").setDessert("Тирамису").setDrink("Бокал белого вина (Шардоне)").build();

        System.out.println(order1);
        System.out.println(order2);

    }
}
