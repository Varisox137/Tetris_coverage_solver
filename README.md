# Tetris_coverage_solver

#### What does this do

Solves puzzles that require players to use some 4-tiled Tetris blocks to cover a rectangular grid.

#### Inspiration

At first this program is meant to help solving puzzles of the Steam game ***Sigils of Elohim***.

While searching for inspiration and suitable algorithms, I happened to see [this post]([跳跃的舞者，舞蹈链（Dancing Links）算法——求解精确覆盖问题 - 万仓一黍 - 博客园 (cnblogs.com)]) , linking the problem to the so-called ***Exact-Covering Problem*** , and by using the smart ***Dancing Links*** data structure, great improvements are made out of plain brute-force enumeration.

#### Usage

For the usage of the program, simply input the 9 needed data for the puzzle, including the row and column of the board, and numbers of each type (there’re 7 of them) of 4-tiled Tetris.

#### Example

For the following puzzle (A-Red-8) :

![4fe865fae788dd9a6f2c6dd117c9dd8](.\4fe865fae788dd9a6f2c6dd117c9dd8.png)

Program input:

![903fd82458ee3ed69e5daf58a305d00](.\903fd82458ee3ed69e5daf58a305d00.png)

You can see the searching procedure as the program recursively dance the links and prints the current candidate rows (from the solution space matrix). However, due to the nature of the algorithm, only one fixed result is generated, and ***turtle*** will paint something like this :

![f43f4f19fad018bcd7c22a4ba3c3c2e](.\f43f4f19fad018bcd7c22a4ba3c3c2e.png)

Great job done!
