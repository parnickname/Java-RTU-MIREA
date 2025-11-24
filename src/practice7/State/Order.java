package practice7.State;

public class Order {
    private State state;

    public Order() {
        this.state = new NewState();
    }

    public void setState(State state) {
        this.state = state;
    }

    public State getState() {
        return state;
    }

    public void nextState() {
        state.handle(this);
    }
}
