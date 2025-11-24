package practice7.Bridge;

public class App {
    public static void main(String[] args) {
        Shape redCircle = new Circle(100, 100, 10, new RedDrawAPI());
        Shape greenCircle = new Circle(200, 200, 20, new GreenDrawAPI());
        Shape redSquare = new Square(50, 50, 30, new RedDrawAPI());
        Shape greenSquare = new Square(150, 150, 40, new GreenDrawAPI());

        redCircle.draw();
        greenCircle.draw();
        redSquare.draw();
        greenSquare.draw();
    }
}
