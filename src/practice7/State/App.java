package practice7.State;

public class App {
    public static void main(String[] args) {
        Order order = new Order();

        System.out.println("Текущее состояние: " + order.getState().getClass().getSimpleName());
        order.nextState();

        System.out.println("\nТекущее состояние: " + order.getState().getClass().getSimpleName());
        order.nextState();

        System.out.println("\nТекущее состояние: " + order.getState().getClass().getSimpleName());
        order.nextState();

        System.out.println("\nПопытка перехода из конечного состояния:");
        order.nextState();
    }
}
