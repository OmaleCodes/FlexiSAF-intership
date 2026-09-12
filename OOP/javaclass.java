/* this code show that i have grasp the concept of class in java language*/

public class Car{
    private string colour;
    private string model;
    private int speed;


    public car (string colour, string model) {
        this.colour = colour;
        this.model = model;
        this.speed = 0;
    }

    public void acceleration(){
        this.speed += 10;
    }

    public void deceleration(){
        this.seed -=10;
    }

    public static void main (string[] args) {
        car mycar = new car ("red", "toyota");
        mycar.accelerate();
        system.out.println(mycar.speed);
    }




}