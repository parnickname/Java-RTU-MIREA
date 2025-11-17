package practice5.ArraysAndCircle;

import java.util.List;
import java.util.ArrayList;

public class TestFindMaxCircle {
    static int findMaxCircle(ArrayList<Circle> circles) {
        int maxIndex = 0;
        for (int i = 1; i < circles.size(); i++) {
            if (circles.get(i).compareTo(circles.get(maxIndex)) > 0) {
                maxIndex = i;
            }
        }
        return maxIndex;
    }


    public static void main(String[] args) {
        ArrayList<Circle> arr = new ArrayList<>(List.of(
                new Circle(25),
                new Circle(89),
                new Circle(512),
                new Circle(743),
                new Circle(156),
                new Circle(298)
        ));

        System.out.println("Индекс круга с наибольшим радиусом: " + findMaxCircle(arr));
    }

}
