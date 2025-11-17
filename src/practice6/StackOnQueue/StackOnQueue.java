package practice6.StackOnQueue;

import java.util.*;


public class StackOnQueue<E> {
    private Queue<E> myStack;
    private Queue<E> copyStack;

    StackOnQueue() {
        myStack = new LinkedList<>();
        copyStack = new LinkedList<>();
    }

    StackOnQueue(Queue<E> queue) {
        if (queue == null) throw new NullPointerException("стек пуст");
        this.myStack = queue;
        copyStack = new LinkedList<>();
    }


    public void push(E e) {
        myStack.add(e);
    }


    public E top() {
        if (myStack.isEmpty()) throw new NoSuchElementException("стек пуст");
        E lastObject = null;
        while (!myStack.isEmpty()) {
            lastObject = myStack.poll();
            copyStack.add(lastObject);
        }
        swapStacks();
        return lastObject;
    }

    public E pop() {
        if (myStack.isEmpty()) throw new NoSuchElementException("стек пуст");
        while (myStack.size() > 1) {
            copyStack.add(myStack.poll());
        }
        E o = myStack.poll();
        swapStacks();
        return o;
    }

    public boolean empty() {
        return myStack.isEmpty();
    }

    private void swapStacks() {
        Queue<E> tmp = myStack;
        myStack = copyStack;
        copyStack = tmp;
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder("[");
        E o = null;
        while (!myStack.isEmpty()) {
            o = myStack.poll();
            sb.append(o);
            if (!myStack.isEmpty()) sb.append(", ");
            copyStack.add(o);
        }
        sb.append("]");
        swapStacks();
        return sb.toString();
    }
}
