package practice4.figures.app;

import practice4.figures.exceptions.IllegalTriangleException;
import practice4.figures.geometry.*;

public class TestColorable {
    public static void main(String[] args) {
        GeometricObject[] figures = null;
        try{
            figures = new GeometricObject[] {
                new Circle(12, "Желтый", true),
                new ComparableCircle(8, "Оранжевый", false),
                new Rectangle(7, 9, "Голубой", true),
                new Square(6),
                new Triangle(5, 6, 7, "Розовый", true),
            };
        } catch(IllegalTriangleException e) {
            System.out.println("Ошибка: " + e.getMessage());
        }

        for (GeometricObject fig : figures){
            System.out.println(fig + ", площадь: " + fig.getArea());

            if (fig instanceof Colorable){
                ((Colorable) fig).howToColor();
            }
            System.out.print("\n");
        }
    }

}
