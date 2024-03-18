import com.google.gson.Gson;

import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public class SimulationFactory {
    private final List<Particle> ParticlesList;
    private final Grid SimulatedGrid;
    private final int totalTime;
    private final int frameSize;
    private final double noise;

    public SimulationFactory(int frameSize, double noise, double L, double speed, int N, double interactionRadius, boolean boundaryConditions, int totalTime) {
        this.noise = noise;
        int M = (int) Math.floor(L/interactionRadius);
        this.SimulatedGrid = new Grid(M, L, interactionRadius, boundaryConditions);
        this.ParticlesList = new ArrayList<>();
        this.totalTime = totalTime;
        this.frameSize = frameSize;
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

    public void simulation(){
        try {
            FileWriter writer_polarization = new FileWriter("output/DataPolarization.csv");
            writer_polarization.write("tiempo,polarization");
            double VxSum = 0, VySum = 0;

            FileWriter writer_data = new FileWriter("output/DataSimulation.csv");
            writer_data.write("x,y,gridX, gridY,vel,angulo,id,time");
            Random random = new Random();
            for(int t = 0; t < totalTime; t++){
                SimulatedGrid.CIM(ParticlesList);
                VxSum = 0;
                VySum = 0;
                for(Particle particle : ParticlesList){
                    double new_angle = particle.interaction(particle.getNeighbours());
                    new_angle += random.nextDouble(2*noise) - noise;
                    particle.setAngle(new_angle);
                    particle.move(frameSize);
                    SimulatedGrid.reposition(particle);
                    System.out.println(particle);
                    writer_data.write( "\n" + particle.getX() + "," + particle.getY() + "," + particle.getxCell() + "," +
                            particle.getyCell() + "," + particle.getSpeed() + "," + particle.getAngle() + "," + particle.getId() + "," + t);

                    VxSum += particle.getVx();
                    VySum += particle.getVy();
                }
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
        SimulationFactory simulator = new SimulationFactory(config.getFrameSize(), config.getNoise(), config.getL(), config.getSpeed(), config.getN(), config.getInteractionRadius(), config.getBoundaryConditions(), config.getTotalTime());

        simulator.simulation();
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
