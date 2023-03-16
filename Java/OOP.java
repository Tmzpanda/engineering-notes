// abstract class 
abstract class Product {
    private String name;
    private double price;

    public Product(String name, double price) {
        this.name = name;
        this.price = price;
    }

    public String getName() {
        return name;
    }

    public double getPrice() {
        return price;
    }

    public abstract double getDiscountedPrice();
}


// inheritance
class Clothing extends Product {
    private String size;
    private String color;

    public Clothing(String name, double price, String size, String color) {
        super(name, price);
        this.size = size;
        this.color = color;
    }

    public double getDiscountedPrice() {
        if (size.equals("S")) {
            return getPrice() * 0.9;
        } else {
            return getPrice() * 0.8;
        }
    }
}

// interface
interface PaymentMethod {
    void makePayment(double amount);
}


// implementation
class CreditCard implements PaymentMethod {
    private String cardNumber;
    private String expiryDate;

    public CreditCard(String cardNumber, String expiryDate) {
        this.cardNumber = cardNumber;
        this.expiryDate = expiryDate;
    }

    public void makePayment(double amount) {
        System.out.printf("Processing credit card payment for $%.2f\n", amount);
    }
}
