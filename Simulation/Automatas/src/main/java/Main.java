import com.google.gson.Gson;

import java.io.FileReader;
import java.io.IOException;

public class Main {
    public static void main(String[] args) {
        SimulationConfig config = readConfig("input/input.json");
        if(config == null) {
            return;
        }
        SimulationFactory simulator =
                new SimulationFactory(config.getFrameSize(), config.getNoise(), config.getL(), config.getSpeed(),
                config.getN(), config.getInteractionRadius(), config.getBoundaryConditions(),
                config.getCircleBoundaryConditions(),config.getTotalTime());

        simulator.simulation(config.getPolarizationPath(), config.getSimulationPath());
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
