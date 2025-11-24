package practice7.Bridge;

public class GreenDrawAPI implements DrawAPI {
    @Override
    public void drawCircle(int radius, int x, int y) {
        System.out.println("Рисуем зелёный круг: радиус=" + radius + ", x=" + x + ", y=" + y);
    }

    @Override
    public void drawSquare(int side, int x, int y) {
        System.out.println("Рисуем зелёный квадрат: сторона=" + side + ", x=" + x + ", y=" + y);
    }
}
