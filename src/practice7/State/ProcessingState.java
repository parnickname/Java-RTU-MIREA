package practice7.State;

public class ProcessingState implements State {
    @Override
    public void handle(Order order) {
        System.out.println("Заказ обрабатывается. Отправка...");
        order.setState(new ShippedState());
    }
}
