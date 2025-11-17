package practice4.figures.geometry;

import practice4.figures.exceptions.IllegalTriangleException;

public class Triangle extends  GeometricObject {
    double side1 = 1.0;
    double side2 = 1.0;
    double side3 = 1.0;

    public Triangle(){}

    public Triangle(double side1, double side2, double side3) throws IllegalTriangleException {
        validateSides(side1, side2, side3);
        this.side1 = side1;
        this.side2 = side2;
        this.side3 = side3;
    }

    public Triangle(double side1, double side2, double side3, String color, boolean filled) throws IllegalTriangleException {
        this(side1, side2, side3);
        setColor(color);
        setFilled(filled);
    }

    private void validateSides(double side1, double side2, double side3) throws IllegalTriangleException {
        if (side1 + side2 <= side3 || side2 + side3 <= side1 || side1 + side3 <= side2) {
            throw new IllegalTriangleException(
                    "The triangle sides are not valid: " + side1 + ", " + side2 + ", " + side3
            );
        }
    }


    public double getSide1() {
        return side1;
    }
    public double getSide2() {
        return side2;
    }
    public double getSide3() {
        return side3;
    }

    public double getPerimeter() {
        return (side1 + side2 + side3);
    }

    public double getArea(){
        double p = getPerimeter() / 2.0;
        return Math.sqrt(p*(p-side1)*(p-side2)*(p-side3));
    }

    @Override
    public String toString(){
        return "\nТреугольник: " + super.toString() + ", 1-я сторона = " + side1
                + ", 2-я сторона = " + side2
                + ", 3-я сторона = " + side3;
    }
}
