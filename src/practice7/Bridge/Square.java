package practice7.Bridge;

public class Square extends Shape {
    private int x, y, side;

    public Square(int x, int y, int side, DrawAPI drawAPI) {
        super(drawAPI);
        this.x = x;
        this.y = y;
        this.side = side;
    }

    @Override
    public void draw() {
        drawAPI.drawSquare(side, x, y);
    }
}
