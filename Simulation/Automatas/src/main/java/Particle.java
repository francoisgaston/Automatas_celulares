import java.util.ArrayList;
import java.util.List;
import java.util.Objects;
import java.util.Random;

public class Particle {
    private int id;
    private static int nextId = 0;
    private double x;
    private double y;
    private double speed;
    private double angle;
    private double interactionRadius;
    private final List<Particle> neighbours;

    public Particle(double x, double y, double speed, double angle, double interactionRadius) {
        this.id = nextId++;
        this.x = x;
        this.y = y;
        this.speed = speed;
        this.angle = angle;
        this.interactionRadius = interactionRadius;
        this.neighbours = new ArrayList<>();
    }

    public Particle(double x, double y, double speed, double angle, double interactionRadius, int id) {
        this.id = id;
        this.x = x;
        this.y = y;
        this.speed = speed;
        this.angle = angle;
        this.interactionRadius = interactionRadius;
        this.neighbours = new ArrayList<>();
    }

    public Particle(double L, double speed, double interactionRadius){
        this.id = nextId++;
        this.x = Math.random() * L;
        this.y = Math.random() * L;
        this.speed = speed;
        this.angle = Math.random() * 2 * Math.PI;
        //random.nextDouble(2* Math.PI);
        this.interactionRadius = interactionRadius;
        this.neighbours = new ArrayList<>();
    }

    public Particle nextParticle(double FrameSize, double noise){
        double new_angle = new_angle();
        new_angle +=  noise * Math.random() - noise / 2;

        double new_x = x + FrameSize * speed * Math.cos(new_angle);
        double new_y = y + FrameSize * speed * Math.sin(new_angle);

        return new Particle(new_x, new_y, speed, new_angle, interactionRadius, id);
    }

    private double new_angle(){
        double sinProm = Math.sin(this.angle);
        double cosProm = Math.cos(this.angle);

        for(Particle particle : neighbours){
            sinProm += Math.sin(particle.angle);
            cosProm += Math.cos(particle.angle);
        }

        sinProm = sinProm/(neighbours.size()+1);
        cosProm = cosProm/(neighbours.size()+1);
        return Math.atan2(sinProm, cosProm);
    }

    public boolean isNeighbour(Particle particle, Grid SimulatedGrid){
        double distance = SimulatedGrid.gridDistance(x, y, particle.x, particle.y);
        return interactionRadius>distance;
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

    public double getSpeed() {
        return speed;
    }

    public void setSpeed(double speed) {
        this.speed = speed;
    }

    public double getAngle() {
        return angle;
    }

    public void setAngle(double angle) {
        this.angle = angle;
    }

    public double getInteractionRadius() {
        return interactionRadius;
    }

    public void setInteractionRadius(double interactionRadius) {
        this.interactionRadius = interactionRadius;
    }

    public int getId() {
        return id;
    }
    public void newId(){
        this.id = nextId++;
    }

    public List<Particle> getNeighbours() {
        return this.neighbours;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Particle particle = (Particle) o;
        return id == particle.id;
    }

    @Override
    public int hashCode() {
        return Objects.hash(id);
    }

    @Override
    public String toString() {
        return "x:" + x + ", Y:" + y + ", vel:" + speed + ", angulo:" + angle + ", id:" + id;
    }

}
