package practice3.bikeproject;

public class BikeDriver {
    public static void main(String[] args) {

        RoadBike bike1 = new RoadBike();
        RoadBike bike2 = new RoadBike("drop", "racing", "narrow", "sport", 16, 28, 22);
        MountainBike bike3 = new MountainBike();
        Bike bike4 = new Bike();

        bike1.printDescription();
        bike2.printDescription();
        bike3.printDescription();
        bike4.printDescription();
        bike1.setPostHeigth(24);
        bike1.printDescription();
    }
}
