public class SimulationConfig {
    private int frameSize;
    private double noise;
    private double L;
    private double speed;
    private int N;
    private double interactionRadius;
    private boolean boundaryConditions;
    private int totalTime;

    public SimulationConfig(){

    }

    public int getFrameSize() {
        return frameSize;
    }

    public double getNoise() {
        return noise;
    }

    public double getL() {
        return L;
    }

    public double getSpeed() {
        return speed;
    }

    public int getN() {
        return N;
    }

    public double getInteractionRadius() {
        return interactionRadius;
    }

    public boolean getBoundaryConditions() {
        return boundaryConditions;
    }

    public int getTotalTime() {
        return totalTime;
    }
}
