package practice7.State;

public class ShippedState implements State {
    @Override
    public void handle(Order order) {
        System.out.println("Заказ уже отправлен. Ожидайте доставку.");
    }
}
