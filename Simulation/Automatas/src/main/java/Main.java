import com.google.gson.Gson;

import java.io.FileReader;
import java.io.IOException;

public class Main {
    public static void main(String[] args) {
        // Realizar solo una simulación para realizar una animación
        //Simulation();

        // Realizar simulaciones para luego analizar variación de polarizacion vs tiempo segun el nivel de ruido
        //NoiseMultiSimulation();

        // Realizar simulaciones para luego analizar variación de polarizacion vs tiempo segun la densidad (variando numero de particulas)
        //DensityMultiSimulation();

        // Realizar simulaciones para luego analizar comportamiento en funcion a 4 circulos.
        CircleNoiseMultiSimulation();
    }

    public static void Simulation(){
        SimulationConfig config = readConfig("input/input.json");
        if(config == null) {
            return;
        }
        SimulationFactory simulator =
                new SimulationFactory(1, config.getNoise(), config.getL(), config.getSpeed(),
                        config.getN(), config.getInteractionRadius(), false,
                        config.getCircleBoundaryConditions(),config.getTotalTime());

        simulator.simulation(config.getL(), config.getN());
    }

    public static void NoiseMultiSimulation(){
        SimulationConfig config = readConfig("input/NoiseInput.json");
        if(config == null) {
            return;
        }

        for(double noise = 0.3; noise <= 1; noise+=0.5){
            SimulationFactory simulator =
                    new SimulationFactory(1, noise, config.getL(), config.getSpeed(),
                            config.getN(), config.getInteractionRadius(), false,
                            config.getCircleBoundaryConditions(),config.getTotalTime());

            simulator.simulation(config.getL(), config.getN());
        }
    }

    public static void DensityMultiSimulation(){
        SimulationConfig config = readConfig("input/DensityInput.json");
        if(config == null) {
            return;
        }

        for(int N = 10; N <= 4000; N+=4000){
            SimulationFactory simulator =
                    new SimulationFactory(1, config.getNoise(), config.getL(), config.getSpeed(),
                            N, config.getInteractionRadius(), true,
                            config.getCircleBoundaryConditions(),config.getTotalTime());

            simulator.simulation(config.getL(), N);
        }
    }

    public static void CircleNoiseMultiSimulation(){
        SimulationConfig config = readConfig("input/CircleNoiseInput.json");
        if(config == null) {
            return;
        }

        for(double noise = 5; noise <= 6; noise+=0.5){
            SimulationFactory simulator =
                    new SimulationFactory(1, noise, config.getL(), config.getSpeed(),
                            config.getN(), config.getInteractionRadius(), true,
                            config.getCircleBoundaryConditions(),config.getTotalTime());

            simulator.simulation(config.getL(), config.getN());
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
