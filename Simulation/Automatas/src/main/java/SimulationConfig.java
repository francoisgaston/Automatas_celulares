public class SimulationConfig {
    private int frameSize;
    private double noise;
    private double L;
    private double speed;
    private int N;
    private double interactionRadius;
    private boolean boundaryConditions;
    private int totalTime;
    private String PolarizationPath;
    private String SimulationPath;

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

    public void setFrameSize(int frameSize) {
        this.frameSize = frameSize;
    }

    public void setNoise(double noise) {
        this.noise = noise;
    }

    public void setL(double l) {
        L = l;
    }

    public void setSpeed(double speed) {
        this.speed = speed;
    }

    public void setN(int n) {
        N = n;
    }

    public void setInteractionRadius(double interactionRadius) {
        this.interactionRadius = interactionRadius;
    }

    public boolean isBoundaryConditions() {
        return boundaryConditions;
    }

    public void setBoundaryConditions(boolean boundaryConditions) {
        this.boundaryConditions = boundaryConditions;
    }

    public void setTotalTime(int totalTime) {
        this.totalTime = totalTime;
    }

    public String getPolarizationPath() {
        return PolarizationPath;
    }

    public void setPolarizationPath(String polarizationPath) {
        PolarizationPath = polarizationPath;
    }

    public String getSimulationPath() {
        return SimulationPath;
    }

    public void setSimulationPath(String outputSimulation) {
        SimulationPath = outputSimulation;
    }
}
