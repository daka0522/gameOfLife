type Cell = 0 | 1
type Grid = Uint8Array;

/**
 * 
 * # Game of Life
 * ## Settings 
- N = live neighbors
- Cell = Live or Dead
- Cell neighbors = 8 (3 x 3 grid - 1 cell)

## Rules 
1. N < 2: Dies. Under population
2. N > 2 or 3: Lives
3. N > : Dies. Over population
4. Dead cell, N == 3: becomes live, reproduction
 * 
 */
export class Game {
  grid: Grid;
  GRID_WIDTH: number = 100
  GRID_HEIGHT: number = 100
  seed: number
  canvas: HTMLCanvasElement
  ctx: CanvasRenderingContext2D

  constructor(canvas: HTMLCanvasElement) {
    this.canvas = canvas
    const context = this.canvas.getContext("2d")
    if (!context) {
      throw new Error("2D context not found/")
    }
    this.ctx = context
    this.seed = 0.4
    this.grid = this.createGrid()
    this.seedGrid()
  }
  // ...
  createGrid(): Grid {
    return new Uint8Array(this.GRID_WIDTH * this.GRID_HEIGHT);
  }
  getCell(x: number, y: number): Cell {
    return this.grid[x * this.GRID_WIDTH + y] as Cell
  }
  setCell(x: number, y: number, value: Cell) {
    this.grid[x * this.GRID_WIDTH + y] = value;
  }
  // Random seed with live cell 0.2
  seedGrid(): void {
    for (let x = 0; x < this.GRID_HEIGHT; x++) {
      for (let y = 0; y < this.GRID_WIDTH; y++) {
        const seed: Cell = Math.random() < this.seed ? 1 : 0;
        this.setCell(x, y, seed)
      }
    }
  }

  countNeighbors(x: number, y: number): number {
    let count = 0;
    for (let dx = -1; dx <= 1; dx++) {
      for (let dy = -1; dy <= 1; dy++) {
        if (dx === 0 && dy === 0) continue;
        const nx = x + dx;
        const ny = y + dy;
        if (
          nx >= 0 &&
          ny >= 0 &&
          nx < this.GRID_HEIGHT &&
          ny < this.GRID_WIDTH
        ) {
          count += this.getCell(nx, ny);
        }
      }
    }
    return count;
  }

  nextGeneration() {
    const newGrid = this.createGrid();
    for (let x = 0; x < this.GRID_HEIGHT; x++) {
      for (let y = 0; y < this.GRID_WIDTH; y++) {
        const alive = this.getCell(x, y) === 1;
        const neighbors = this.countNeighbors(x, y);

        // Rules 1. if alive and neighbor are 2 or 3, then alive
        if (alive && (neighbors === 2 || neighbors === 3)) {
          newGrid[x * this.GRID_WIDTH + y] = 1;
        }
        // Rule 2. if dead and nieghbors are 3, then alive
        else if (!alive && neighbors === 3) {
          newGrid[x * this.GRID_WIDTH + y] = 1;
        }
        // Rule 3
        else if (alive && neighbors > 3) {
          newGrid[x * this.GRID_WIDTH + y] = 0;
        }
        // Rule 4
        else if (alive && neighbors < 2) {
          newGrid[x * this.GRID_WIDTH + y] = 0;
        }
        // Else, die.
        else {
          newGrid[x * this.GRID_WIDTH + y] = 0;
        }
      }
    }
    this.grid = newGrid;
  }

  // Optimized rendering
  drawGrid(): void {
    const imageData = this.ctx.createImageData(this.canvas.width, this.canvas.height);
    const data = imageData.data;
    const cellSize = this.canvas.width / this.GRID_WIDTH // do NOT use Math.floor

    for (let x = 0; x < this.GRID_HEIGHT; x++) {
      for (let y = 0; y < this.GRID_WIDTH; y++) {
        const idx = (x * this.GRID_WIDTH + y);
        const alive = this.grid[idx];
        for (let dx = 0; dx < cellSize; dx++) {
          for (let dy = 0; dy < cellSize; dy++) {
            const px = ((x * cellSize + dx) * this.canvas.width + (y * cellSize + dy)) * 4;
            data[px] = alive ? 255 : 17;      // R
            data[px + 1] = alive ? 255 : 17;  // G
            data[px + 2] = alive ? 255 : 17;    // B
            data[px + 3] = 255;               // A
          }
        }
      }
    }
    this.ctx.putImageData(imageData, 0, 0);
  }
}


