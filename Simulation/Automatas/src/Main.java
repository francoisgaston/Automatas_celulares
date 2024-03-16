public class Main {

    public static void main(String[] args) {

        int frameSize = 1;
        double noise = 1;
        double L = 100;
        double speed = 1;
        int N = 3;
        double interactionRadius = 2;
        boolean boundaryConditions = true;
        int totalTime = 20;

        SimulationFactory simulator = new SimulationFactory(frameSize, noise, L, speed, N, interactionRadius, boundaryConditions, totalTime);

        simulator.simulation();

    }
}