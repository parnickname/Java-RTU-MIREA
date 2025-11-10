package practice2.app;

import practice2.vehicles.*;

public class TestCar {
    public static void main(String[] args) {
        Vehicle passat = new Car(
                "Audi A6",
                "C789MN99",
                "Blue",
                2016,
                "Dmitry P",
                "INS54321",
                "Diesel"
        );

        Vehicle spectre = new ElectricCar("Tesla Model S",
                "E123TT77",
                "Red",
                2022,
                "Oleg K",
                "INS87654",
                95
        );

        passat.setColor("Black");
        passat.setOwnerName("Maxim Petrov");
        passat.setYear(2019);

        spectre.setOwnerName("Anna Volkova");
        spectre.setInsuranceNumber("INS11122");

        ((ElectricCar) spectre).setBatteryCapacity(105);

        System.out.println(passat);
        System.out.println("\n");
        System.out.println(spectre);

    }
}
