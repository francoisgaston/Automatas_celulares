import com.google.gson.Gson;

import java.io.FileReader;
import java.io.IOException;

public class Main {
    public static void main(String[] args) {
        NoiseMultiSimulation();
        //Simulation();
        //DensityMultiSimulation();
    }

    public static void Simulation(){
        SimulationConfig config = readConfig("input/input.json");
        if(config == null) {
            return;
        }
        SimulationFactory simulator =
                new SimulationFactory(1, config.getNoise(), config.getL(), config.getSpeed(),
                        config.getN(), config.getInteractionRadius(), true,
                        config.getCircleBoundaryConditions(),config.getTotalTime());

        simulator.simulation(config.getNCircles(), config.getRCircles(), config.getL(), config.getN());
    }

    public static void NoiseMultiSimulation(){
        SimulationConfig config = readConfig("input/NoiseInput.json");
        if(config == null) {
            return;
        }

        for(double noise = 0; noise <= 5; noise+=0.5){
            SimulationFactory simulator =
                    new SimulationFactory(1, noise, config.getL(), config.getSpeed(),
                            config.getN(), config.getInteractionRadius(), true,
                            config.getCircleBoundaryConditions(),config.getTotalTime());

            simulator.simulation(config.getNCircles(), config.getRCircles(), config.getL(), config.getN());
        }
    }

    public static void DensityMultiSimulation(){
        SimulationConfig config = readConfig("input/DensityInput.json");
        if(config == null) {
            return;
        }

        for(int N = 10; N <= 4020; N+=800){
            SimulationFactory simulator =
                    new SimulationFactory(1, config.getNoise(), config.getL(), config.getSpeed(),
                            N, config.getInteractionRadius(), true,
                            config.getCircleBoundaryConditions(),config.getTotalTime());

            simulator.simulation(config.getNCircles(), config.getRCircles(), config.getL(), N);
        }
    }

    public static SimulationConfig readConfig(String path){
        Gson gson = new Gson();
        SimulationConfig sConfig = null;
        try (FileReader reader = new FileReader(path)) {
            sConfig = gson.fromJson(reader, SimulationConfig.class);
        } catch (IOException e) {
            e.printStackTrace();
        }
        return sConfig;
    }

}
