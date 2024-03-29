import com.google.gson.Gson;

import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Random;
import org.json.JSONObject;
import java.io.FileWriter;
import java.io.IOException;

public class SimulationFactory {
    private List<Particle> ParticlesList;
    private Grid SimulatedGrid;
    private final int totalTime;
    private final int frameSize;
    private final double noise;

    public SimulationFactory(int frameSize, double noise, double L, double speed, int N, double interactionRadius, boolean boundaryConditions, boolean CircleBoundaryConditions, int totalTime) {

        writeStatus(noise, L, speed, N, interactionRadius, boundaryConditions, totalTime);

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
        //Particle borderParticle = new Particle(1, 5, 1, 0, 1, 1);
        //this.SimulatedGrid.addParticle(borderParticle);
        //this.ParticlesList.add(borderParticle);
        //Particle borderParticle2 = new Particle(5.5, 5, 1, Math.PI, 1, 2);
        //this.SimulatedGrid.addParticle(borderParticle2);
        //this.ParticlesList.add(borderParticle2);
    }

    public void simulation(double L, int N){
        try {
            FileWriter writer_data = new FileWriter("output/SimulationData_" + N + "_" + (int) L + "_" + noise + ".csv");
            writer_data.write("id,x,y,vel,angulo,time");

            for(int t = 0; t < totalTime; t++){
                Grid NextGrid = new Grid(SimulatedGrid);
                List<Particle> NextParticleList = new ArrayList<>();

                SimulatedGrid.CIM(ParticlesList);
                for(Particle particle : ParticlesList){
                    //System.out.println(particle + ", Time:" + t);

                    Particle NextParticle = particle.nextParticle(frameSize, this.noise);
                    NextGrid.addParticle(NextParticle);
                    NextParticleList.add(NextParticle);

                    writer_data.write( "\n" + particle.getId() + "," + particle.getX() + "," + particle.getY() + "," + particle.getSpeed() + "," + particle.getAngle() + "," + t);
                }
                SimulatedGrid = NextGrid;
                ParticlesList = NextParticleList;
            }

            writer_data.close();
        } catch(IOException e){
            System.out.println("Error al escribir en el archivo: " + e.getMessage());
        }
    }

    public void writeStatus(double noise, double L, double speed, int N, double interactionRadius, boolean boundaryConditions, int totalTime){
        try {
            JSONObject jsonObject = new JSONObject();
            jsonObject.put("N", N);
            jsonObject.put("L", L);
            jsonObject.put("speed",speed);
            jsonObject.put("totalTime", totalTime);
            jsonObject.put("noise", noise);
            jsonObject.put("radius", interactionRadius);
            jsonObject.put("boundary", boundaryConditions);

            FileWriter writer_status = new FileWriter("output/StateData_" + N + "_" + (int) L + "_" + noise + ".json");
            writer_status.write(jsonObject.toString());
            writer_status.close();

        } catch(IOException e){
            System.out.println("Error al escribir en el archivo: " + e.getMessage());
        }
    }

}
