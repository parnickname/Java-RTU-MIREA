package practice5.ArraysAndCircle;

public class Test2DArrayMaxSearch {
    public record Result<T>(T value, int row, int col) {
    }

    public static <T extends Comparable<? super T>> Result<T> max(T[][] arr) {
        if (arr == null || arr.length == 0) {
            throw new IllegalArgumentException("массив пуст");
        }

        int maxI = -1;
        int maxJ = -1;
        T max = null;

        for (int i = 0; i < arr.length; i++) {
            if (arr[i] == null) continue;
            for (int j = 0; j < arr[i].length; j++) {
                T target = arr[i][j];
                if (target == null) continue;
                if (max == null || target.compareTo(max) > 0) {
                    max = target;
                    maxI = i;
                    maxJ = j;
                }
            }
        }

        if (max == null) throw new IllegalArgumentException("массив пуст");
        return new Result<>(max, maxI, maxJ);
    }

    public static void main(String[] args) {
        Integer[][] intArr = {
                {15, 42, 8},
                {91, 37, 63},
                {22, -105, 58}
        };

        Result<Integer> res = max(intArr);
        System.out.println(res.value() + ", координаты:  " + res.row() + "," + res.col());
    }
}
