package practice7.Bridge;

public class RedDrawAPI implements DrawAPI {
    @Override
    public void drawCircle(int radius, int x, int y) {
        System.out.println("Рисуем красный круг: радиус=" + radius + ", x=" + x + ", y=" + y);
    }

    @Override
    public void drawSquare(int side, int x, int y) {
        System.out.println("Рисуем красный квадрат: сторона=" + side + ", x=" + x + ", y=" + y);
    }
}
