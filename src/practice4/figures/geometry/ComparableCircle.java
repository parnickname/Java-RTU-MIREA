package practice4.figures.geometry;

public class ComparableCircle extends Circle {
    public ComparableCircle(double radius) {
        super(radius);
    }

    public ComparableCircle(double radius, String color, boolean filled) {
        super(radius, color, filled);
    }

    @Override
    public String toString() {
        return "ComparableCircle " + super.toString();
    }
}
