package practice5.ArraysAndCircle;

import java.util.*;

public class DeleteDuplicatesAndLinearSearch {
    static <T> int linearSearch(ArrayList<T> list, T target) {
        return list.indexOf(target);
    }

    static <T> ArrayList<T> deleteDuplicates(ArrayList<T> list) {
        ArrayList<T> result = new ArrayList<>();
        for (T item : list) {
            if (!result.contains(item)) {
                result.add(item);
            }
        }
        return result;
    }

    public static void main(String[] args) {
        ArrayList<Integer> list = new ArrayList<>(List.of(7, 7, 3, 7, 3, 9, 3, 9, 2));
        System.out.println(list);
        list = deleteDuplicates(list);
        System.out.println(list);

        System.out.println(linearSearch(list, 3));
    }
}
