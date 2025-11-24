package practice7.Command;

public class TV implements Device {
    @Override
    public void turnOn() {
        System.out.println("Телевизор включен");
    }

    @Override
    public void turnOff() {
        System.out.println("Телевизор выключен");
    }

    @Override
    public String getName() {
        return "Телевизор";
    }
}
