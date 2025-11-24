package practice7.Command;

public class App {
    public static void main(String[] args) {
        Device tv = new TV();
        Device ac = new AirConditioner();

        Command tvOn = new TurnOnCommand(tv);
        Command tvOff = new TurnOffCommand(tv);
        Command acOn = new TurnOnCommand(ac);
        Command acOff = new TurnOffCommand(ac);

        RemoteControl remote = new RemoteControl();

        remote.setCommand(tvOn);
        remote.pressButton();

        remote.setCommand(acOn);
        remote.pressButton();

        remote.setCommand(tvOff);
        remote.pressButton();

        remote.setCommand(acOff);
        remote.pressButton();
    }
}
