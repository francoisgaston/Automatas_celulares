public class Main {

    public static void main(String[] args) {

        int frameSize = 1;
        double noise = 0.001;
        double L = 10;
        double speed = 2;
        int N = 2;
        double interactionRadius = 1;
        boolean boundaryConditions = true;
        int totalTime = 20;

        SimulationFactory simulator = new SimulationFactory(frameSize, noise, L, speed, N, interactionRadius, boundaryConditions, totalTime);

        simulator.simulation();

    }
}