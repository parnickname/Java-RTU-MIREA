package practice5.ArraysAndCircle;

public class Circle implements Comparable<Circle> {
    private int radius = 0;

    Circle(int radius) {
        this.radius = radius;
    }

    public int compareTo(Circle o) {
        return Integer.compare(this.radius, o.radius);
    }
}
