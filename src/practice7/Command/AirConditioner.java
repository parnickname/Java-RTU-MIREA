package practice7.Command;

public class AirConditioner implements Device {
    @Override
    public void turnOn() {
        System.out.println("Кондиционер включен");
    }

    @Override
    public void turnOff() {
        System.out.println("Кондиционер выключен");
    }

    @Override
    public String getName() {
        return "Кондиционер";
    }
}
