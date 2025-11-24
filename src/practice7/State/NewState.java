package practice7.State;

public class NewState implements State {
    @Override
    public void handle(Order order) {
        System.out.println("Заказ создан. Переход в обработку...");
        order.setState(new ProcessingState());
    }
}
