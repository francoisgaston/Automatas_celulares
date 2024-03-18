import java.util.*;

public class Grid {
    private final int M;
    private final double L;
    private final double Msize;
    private final double interactionRadius;
    private final boolean boundaryConditions;
    private final ParticlesList[][] ParticleGrid;

    public Grid(int M, double L, double interactionRadius, boolean boundaryConditions) {
        this.M = M;
        this.L = L;
        this.Msize = L/M;
        this.interactionRadius = interactionRadius;
        this.boundaryConditions = boundaryConditions;
        this.ParticleGrid = new ParticlesList[M][M];
    }

    public boolean addParticle(Particle particle){
        int gridX = (int) Math.floor(particle.getX() / Msize);
        int gridY = (int) Math.floor(particle.getY() / Msize);

        particle.setxCell(gridX);
        particle.setyCell(gridY);
        particle.setNeighbourCells(generateNeighbourCells(gridX, gridY));

        if (ParticleGrid[gridX][gridY] == null){
            ParticleGrid[gridX][gridY] = new ParticlesList(new ArrayList<>());
        }

        return ParticleGrid[gridX][gridY].addParticle(particle);
    }

    public int[][] generateNeighbourCells(int gridX, int gridY) {
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

    public boolean isNeighbour(Particle particle1, Particle particle2){
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

        //System.out.println(dy + "---" + dx);
        double hypotenuse = Math.pow(Math.pow(dx, 2) + Math.pow(dy, 2), 0.5);
        return interactionRadius>hypotenuse;
    }


    public void CIM(List<Particle> particlesList){
        for(Particle particle1 : particlesList){
            for(int[] neighbourCell : particle1.getNeighbourCells()){
                ParticlesList aux = ParticleGrid[neighbourCell[0]][neighbourCell[1]];
                if(aux != null){
                    for(Particle particle2 : aux.getParticles()) {
                        if (!particle2.equals(particle1)) {
                            if (isNeighbour(particle1, particle2)) {
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

    public void reposition(Particle particle){
        ParticleGrid[particle.getxCell()][particle.getyCell()].removeParticle(particle);

        particle.setX((particle.getX()+L)%L);
        particle.setY((particle.getY()+L)%L);

        int gridX = (int) Math.floor(particle.getX() / Msize);
        int gridY = (int) Math.floor(particle.getY() / Msize);

        particle.setxCell(gridX);
        particle.setyCell(gridY);
        particle.setNeighbourCells(generateNeighbourCells(gridX, gridY));

        if (ParticleGrid[gridX][gridY] == null){
            ParticleGrid[gridX][gridY] = new ParticlesList(new ArrayList<>());
        }

        ParticleGrid[gridX][gridY].addParticle(particle);
    }
}
