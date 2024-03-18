import java.util.*;

public class Grid {
    private final int M;
    private final double L;
    private final double Msize;
    private final boolean boundaryConditions;
    private final ParticlesList[][] ParticleGrid;

    public Grid(int M, double L, boolean boundaryConditions) {
        this.M = M;
        this.L = L;
        this.Msize = L/M;
        this.boundaryConditions = boundaryConditions;
        this.ParticleGrid = new ParticlesList[M][M];
    }

    public Grid(Grid prevGrid){
        this.M = prevGrid.M;
        this.L = prevGrid.L;
        this.Msize = L/M;
        this.boundaryConditions = prevGrid.boundaryConditions;
        this.ParticleGrid = new ParticlesList[M][M];
    }

    public boolean addParticle(Particle particle){
        particle.setX((particle.getX()+L)%L);
        particle.setY((particle.getY()+L)%L);

        int gridX = (int) Math.floor(particle.getX() / Msize);
        int gridY = (int) Math.floor(particle.getY() / Msize);

        if (ParticleGrid[gridX][gridY] == null){
            ParticleGrid[gridX][gridY] = new ParticlesList(new ArrayList<>());
        }
        return ParticleGrid[gridX][gridY].addParticle(particle);
    }

    public int[][] generateNeighbourCells(Particle particle) {
        int gridX = (int) Math.floor(particle.getX() / Msize);
        int gridY = (int) Math.floor(particle.getY() / Msize);

        if (boundaryConditions) {
            return new int[][]{
                    {gridX, gridY},
                    {gridX, (gridY + 1) % M},
                    {(gridX + 1) % M, (gridY + 1) % M},
                    {(gridX + 1) % M, gridY},
                    {(gridX + 1) % M, (gridY - 1 + M) % M}};
        }
        if (gridY + 1 == M) {
            if (gridX + 1 == M) {
                return new int[][]{{gridX, gridY}};
            }
            return new int[][]{
                    {gridX, gridY},
                    {gridX + 1, gridY},
                    {gridX + 1, gridY - 1}};
        } else {
            if (gridX + 1 == M) {
                return new int[][]{
                        {gridX, gridY},
                        {gridX, gridY + 1}};
            } else {
                if(gridY - 1 < 0){
                    return new int[][]{
                            {gridX, gridY},
                            {gridX, (gridY + 1)},
                            {(gridX + 1), (gridY + 1)},
                            {(gridX + 1), gridY}};
                }else{
                    return new int[][]{
                            {gridX, gridY},
                            {gridX, (gridY + 1)},
                            {(gridX + 1), (gridY + 1)},
                            {(gridX + 1), gridY},
                            {(gridX + 1), (gridY - 1)}};
                }
            }
        }
    }

    public double gridDistance(Particle particle1, Particle particle2){
        double directx = Math.abs(particle1.getX() - particle2.getX());
        double dx, dy;
        if(directx*2 > L && boundaryConditions){
            dx = (L - directx);
        }else{
            dx = directx;
        }

        double directy = Math.abs(particle1.getY() - particle2.getY());
        if(directy*2 > L && boundaryConditions){
            dy = (L - directy);
        }else{
            dy = directy;
        }

        return Math.pow(Math.pow(dx, 2) + Math.pow(dy, 2), 0.5);
    }


    public void CIM(List<Particle> particlesList){
        for(Particle particle1 : particlesList){
            for(int[] neighbourCell : generateNeighbourCells(particle1)){
                ParticlesList aux = ParticleGrid[neighbourCell[0]][neighbourCell[1]];
                if(aux != null){
                    for(Particle particle2 : aux.getParticles()) {
                        if (!particle2.equals(particle1)) {
                            if (particle1.isNeighbour(particle2, this)) {
                                System.out.println("SON VECINOS");
                                if (!particle1.getNeighbours().contains(particle2)) {
                                    particle1.getNeighbours().add(particle2);
                                }
                                if (!particle2.getNeighbours().contains(particle1)) {
                                    particle2.getNeighbours().add(particle1);
                                }
                            }
                        }
                    }
                }
            }
        }
    }

}
