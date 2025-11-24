package practice6.StackOnQueue;

public class TestStackOnQueue {
    public static void main(String[] args) {
        StackOnQueue<Integer> myStack = new StackOnQueue<>();

        myStack.push(39);
        myStack.push(67);
        myStack.push(84);

        System.out.println(myStack);

        System.out.println(myStack.top());

        myStack.pop();

        System.out.println("Стек пуст? " + myStack.empty());
        System.out.println(myStack);
    }
}
