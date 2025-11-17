package practice5.MyStack;

import java.util.ArrayList;
import java.util.Scanner;

public class MyStackExtArrL<E> extends ArrayList<E> {
    public MyStackExtArrL() {
        super();
    }

    public MyStackExtArrL(MyStackExtArrL<E> list) {
        super(list);
    }

    public static void main(String[] args) {
        MyStackExtArrL<String> myStack = new MyStackExtArrL<>();
        Scanner sc = new Scanner(System.in);

        for (int i = 0; i < 5; i++) {
            myStack.add(sc.next());
        }

        while (!myStack.isEmpty()) {
            System.out.println(myStack.removeLast());
        }
    }
}

