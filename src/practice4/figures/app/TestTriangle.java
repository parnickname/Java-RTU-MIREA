package practice4.figures.app;

import practice4.figures.exceptions.IllegalTriangleException;
import practice4.figures.geometry.Triangle;

import java.util.Locale;
import java.util.Scanner;

public class TestTriangle {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        sc.useLocale(Locale.US);

        try {
            System.out.print("Введите длины сторон треугольника (например: 3 4 5): ");
            String line = sc.nextLine().trim();

            if (line.isEmpty()) {
                System.out.println("Значения не были заданы — будут использованы по умолчанию: 5.0, 6.0, 7.0");
                line = "5.0 6.0 7.0";
            }

            String[] parts = line.split("\\s+");
            if (parts.length < 3) {
                System.out.println("Ошибка: нужно ввести три стороны!");
                return;
            }

            double side1 = Double.parseDouble(parts[0]);
            double side2 = Double.parseDouble(parts[1]);
            double side3 = Double.parseDouble(parts[2]);

            Triangle triangle = new Triangle(side1, side2, side3);

            System.out.print("Введите цвет треугольника: ");
            String color = sc.nextLine().trim();
            triangle.setColor(color);

            System.out.print("Треугольник закрашен? (true/false): ");
            boolean isFilled = sc.nextBoolean();
            triangle.setFilled(isFilled);

            System.out.print(triangle);
            System.out.print("\nПлощадь: " + triangle.getArea());
            System.out.print("\nПериметр: " + triangle.getPerimeter());


        } catch (IllegalTriangleException e) {
            System.out.println("Ошибка: " + e.getMessage());
        } catch (Exception e) {
            System.out.println("Ошибка ввода: " + e.getMessage());
        }
    }
}