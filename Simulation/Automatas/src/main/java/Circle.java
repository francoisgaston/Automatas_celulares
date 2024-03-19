import java.util.HashSet;
import java.util.Random;

public class Circle {
    private int id;
    private double x;
    private double y;
    private final HashSet<Particle> marked;
    private static final Random random = new Random();
    private int counter;

    public Circle(double L, int id) {
        this.id = id;
        this.x = random.nextDouble(L);
        this.y = random.nextDouble(L);
        this.counter = 0;
        marked = new HashSet<>();
    }

    public void resetCounter(){
        this.counter = 0;
    }
    public int getCounter() {
        return counter;
    }
    public void increaseCounter() {
        this.counter += 1;
    }
    public boolean containsParticle(Particle particle){
        return marked.contains(particle);
    }
    public boolean addParticle(Particle particle){
        return marked.add(particle);
    }
    public int size(){
        return marked.size();
    }
    public double getX() {
        return x;
    }
    public void setX(double x) {
        this.x = x;
    }
    public double getY() {
        return y;
    }
    public void setY(double y) {
        this.y = y;
    }
    public int getId() {
        return id;
    }
    public void setId(int id) {
        this.id = id;
    }
}
