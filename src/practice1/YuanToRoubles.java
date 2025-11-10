package practice1;

import java.util.Scanner;

public class YuanToRoubles {
    public static void main(String[] args) {
        final double ROUBLES_PER_YUAN = 12.45;
        int yuan, digit;
        double roubles;
        String s;

        Scanner input = new Scanner(System.in);

        System.out.print("Введите количество юаней: ");
        yuan = input.nextInt();

        roubles = ROUBLES_PER_YUAN * yuan;

        digit = yuan % 10;

        if (yuan % 100 >= 11 && yuan % 100 <= 14) {
            s = "ей";
        } else if (digit == 1) {
            s = "ь";
        } else if (digit >= 2 && digit <= 4) {
            s = "я";
        } else {
            s = "ей";
        }

        System.out.printf("Сумма в юанях: %d юан%s\nСумма в рублях: %d", yuan, s, (int)Math.round(roubles));

        input.close();
    }
}
