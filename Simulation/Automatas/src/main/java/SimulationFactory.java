import com.google.gson.Gson;

import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public class SimulationFactory {
    private List<Particle> ParticlesList;
    private Grid SimulatedGrid;
    private final int totalTime;
    private final int frameSize;
    private final double noise;

    public SimulationFactory(int frameSize, double noise, double L, double speed, int N, double interactionRadius, boolean boundaryConditions, boolean CircleBoundaryConditions, int totalTime) {
        this.noise = noise;
        int M = (int) Math.floor(L/interactionRadius);
        this.totalTime = totalTime;
        this.frameSize = frameSize;

        this.SimulatedGrid = new Grid(M, L, boundaryConditions, CircleBoundaryConditions);
        this.ParticlesList = new ArrayList<>();
        for (int i = 0; i < N; i++) {
            Particle auxParticle = new Particle(L,speed, interactionRadius);
            while (!this.SimulatedGrid.addParticle(auxParticle)) {
                auxParticle = new Particle(L,speed, interactionRadius);
            }
            this.ParticlesList.add(auxParticle);
        }
        //Particle 1000
        //Particle borderParticle = new Particle(0.1, 0.1, radiusParticle);
        //this.SimulatedGrid.addParticle(borderParticle);
        //this.ParticlesList.add(borderParticle);
    }

    public void simulation(String PolarizationPath, String SimulationPath){
        try {
            FileWriter writer_polarization = new FileWriter(PolarizationPath);
            writer_polarization.write("tiempo,polarization");
            FileWriter writer_data = new FileWriter(SimulationPath);
            writer_data.write("x,y,vel,angulo,id,time");

            double VxSum, VySum;
            for(int t = 0; t < totalTime; t++){
                Grid NextGrid = new Grid(SimulatedGrid);
                List<Particle> NextParticleList = new ArrayList<>();
                VxSum = 0;
                VySum = 0;

                SimulatedGrid.CIM(ParticlesList);
                for(Particle particle : ParticlesList){
                    Particle NextParticle = particle.nextParticle(frameSize, noise);
                    NextGrid.addParticle(NextParticle);
                    NextParticleList.add(NextParticle);
                    VxSum += particle.getSpeed() * Math.sin(particle.getAngle());
                    VySum += particle.getSpeed() * Math.cos(particle.getAngle());

                    System.out.println(particle + ", Time:" + t);
                    writer_data.write( "\n" + particle.getX() + "," + particle.getY() + "," +
                            particle.getSpeed() + "," + particle.getAngle() + "," + particle.getId() + "," + t);
                }
                SimulatedGrid = NextGrid;
                ParticlesList = NextParticleList;

                double polarization = Math.sqrt(Math.pow(VxSum, 2) +  Math.pow(VySum, 2))/(ParticlesList.size() * ParticlesList.get(0).getSpeed());
                writer_polarization.write( "\n" + t + "," + polarization);
            }
            writer_data.close();
            writer_polarization.close();

        } catch(IOException e){
            System.out.println("Error al escribir en el archivo: " + e.getMessage());
        }
    }

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
