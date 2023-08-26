// base class
type Product struct {
    name  string
    price float64
}

// inheritance
type Clothing struct {
    *Product
    size  string
    color string
}

func (c *Clothing) getDiscountedPrice() float64 {
    if c.size == "S" {
        return c.price * 0.9
    }
    return c.price * 0.8
}


// interface
type PaymentMethod interface {
    makePayment(amount float64)
}

// implementation
type CreditCard struct {
    cardNumber  string
    expiryDate  string
}

func (cc *CreditCard) makePayment(amount float64) {
    fmt.Printf("Processing credit card payment for $%.2f\n", amount)
}
