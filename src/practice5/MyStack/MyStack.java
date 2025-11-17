package practice5.MyStack;

import java.util.ArrayList;
import java.util.Scanner;

public class MyStack<E> {
    ArrayList<E> list = new ArrayList<>();

    MyStack(){}

    MyStack(ArrayList<E> list){
        this.list = list;
    }

    public void push(E o) {
        list.add(o);
    }

    public E pop() {
        return list.removeLast();
    }

    public E peek() {
        return list.getLast();
    }

    public int getSize(){
        return list.size();
    }

    public boolean isEmpty(){
        return list.isEmpty();
    }

    public static void main(String[] args) {
        MyStack myStack = new MyStack();
        Scanner sc = new Scanner(System.in);

        for (int i = 0; i < 5; i++) {
            myStack.push(sc.next());
        }

        while (!myStack.isEmpty()) {
            System.out.println(myStack.pop());
        }
    }
}
