package practice1;

import java.util.Scanner;

public class Cars {
    public static void  main(String[] args) {
        String cl, lc;
        int year;
        Scanner input = new Scanner(System.in);

        Car vw = new Car(
                "Tiguan",
                "Silver",
                "B456KX177",
                2018
        );

        vw.To_String();

        System.out.print("Enter new color: ");
        cl = input.nextLine();
        System.out.print("Enter new license plate: ");
        lc = input.nextLine();
        System.out.print("Enter new year: ");
        year = input.nextInt();

        vw.setColor(cl);
        vw.setLicense(lc);
        vw.setYear(year);

        vw.To_String();

        vw.calcAge(2025);

    }
}
