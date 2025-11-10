package practice3.app;

import practice3.vehicles.*;

public class TestCar {
    public static void main(String[] args) {
        Vehicle passat = new Car(
                "BMW 5 Series",
                "M555BM99",
                "Gray",
                2017,
                "Vladimir S",
                "INS67890",
                "Petrol"
        );

        Vehicle spectre = new ElectricCar(
                "Porsche Taycan",
                "P888PT77",
                "White",
                2023,
                "Elena R",
                "INS24680",
                85
        );

        passat.setYear(2020);
        passat.setOwnerName("Nikolai Sokolov");

        spectre.setInsuranceNumber("INS33344");
        spectre.setOwnerName("Maria Petrova");

        System.out.println("Информация о Car:");
        System.out.println(passat);

        System.out.println("\nИнформация о Electric Car:");
        System.out.println(spectre);

        ((ElectricCar) spectre).setBatteryCapacity(93);
        int battery = ((ElectricCar) spectre).getBatteryCapacity();
        System.out.println("Battery capacity (после изменения): " + battery + " kWh");
    }
}