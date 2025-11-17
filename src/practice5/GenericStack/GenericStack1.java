package practice5.GenericStack;

import java.util.Arrays;

public class GenericStack1<E> {
    private E[] arr;
    private int top;

    public GenericStack1(E[] arr) {
        this.arr = arr;
        top = arr.length - 1;
    }

    public int getSize() {
        return top + 1;
    }

    public E peek() {
        return arr[top];
    }

    public void push(E o) {
        if (top == arr.length - 1) {
            arr = Arrays.copyOf(arr, arr.length * 2);
        }
        arr[++top] = o;
    }

    public E pop() {
        return arr[top--];
    }

    public boolean isEmpty() {
        return top < 0;
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i <= top; i++) {
            sb.append(arr[i]).append(" ");
        }
        return sb.toString();
    }

    public static void main(String[] args) {
        Integer[] arr = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
        GenericStack1<Integer> stack = new GenericStack1<>(arr);
        System.out.println(stack);
        System.out.println(stack + "\nРазмер стека: " + stack.getSize() + ", верхний элемент: " + stack.peek());

        stack.push(14567);
        stack.push(45678);
        System.out.println(stack + "\nРазмер стека: " + stack.getSize() + ", верхний элемент: " + stack.peek());

        System.out.println("Извлеченный элемент: " + stack.pop());
        stack.push(3456789);
        stack.push(234567890);
        System.out.println(stack + "\nРазмер стека: " + stack.getSize() + ", верхний элемент: " + stack.peek());

        System.out.println("Стек пустой?: " + stack.isEmpty());
    }
}

