package practice7.Proxy;

public class App {
    public static void main(String[] args) {
        Image image1 = new ProxyImage("photo1.jpg");
        Image image2 = new ProxyImage("photo2.jpg");

        System.out.println("Изображения созданы, но еще не загружены\n");

        System.out.println("Первый вызов display() для image1:");
        image1.display();

        System.out.println("\nВторой вызов display() для image1:");
        image1.display();

        System.out.println("\nПервый вызов display() для image2:");
        image2.display();
    }
}
