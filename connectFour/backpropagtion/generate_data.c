// Training, insgesamt ca. 26 Stunden auf Laptop und PC --> Generiert: 245.000 Positionen
//
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <time.h>
#include <unistd.h>

#define WIDTH 7
#define HEIGHT 6
#define MAX_POSITIONS 1000

// ==================== SPIELLOGIK ====================

int check_win(int field[][HEIGHT]) {
    // Horizontal
    for (int y = 0; y < HEIGHT; y++) {
        for (int x = 0; x < WIDTH - 3; x++) {
            if (field[x][y] != 0 &&
                field[x][y] == field[x+1][y] &&
                field[x][y] == field[x+2][y] &&
                field[x][y] == field[x+3][y]) {
                return field[x][y];
            }
        }
    }

    // Vertikal
    for (int x = 0; x < WIDTH; x++) {
        for (int y = 0; y < HEIGHT - 3; y++) {
            if (field[x][y] != 0 &&
                field[x][y] == field[x][y+1] &&
                field[x][y] == field[x][y+2] &&
                field[x][y] == field[x][y+3]) {
                return field[x][y];
            }
        }
    }

    // Diagonal aufsteigend
    for (int x = 0; x < WIDTH - 3; x++) {
        for (int y = 3; y < HEIGHT; y++) {
            if (field[x][y] != 0 &&
                field[x][y] == field[x+1][y-1] &&
                field[x][y] == field[x+2][y-2] &&
                field[x][y] == field[x+3][y-3]) {
                return field[x][y];
            }
        }
    }

    // Diagonal absteigend
    for (int x = 0; x < WIDTH - 3; x++) {
        for (int y = 0; y < HEIGHT - 3; y++) {
            if (field[x][y] != 0 &&
                field[x][y] == field[x+1][y+1] &&
                field[x][y] == field[x+2][y+2] &&
                field[x][y] == field[x+3][y+3]) {
                return field[x][y];
            }
        }
    }

    return 0;
}

bool is_column_full(int field[][HEIGHT], int col) {
    return field[col][0] != 0;
}

int make_move(int field[][HEIGHT], int col, int player) {
    for (int y = HEIGHT - 1; y >= 0; y--) {
        if (field[col][y] == 0) {
            field[col][y] = player;
            return y;
        }
    }
    return -1;
}

void undo_move(int field[][HEIGHT], int col, int y) {
    field[col][y] = 0;
}

bool is_valid_field(int field[][HEIGHT]) {
    for (int x = 0; x < WIDTH; x++) {
        for (int y = 0; y < HEIGHT - 1; y++) {
            if (field[x][y] != 0 && field[x][y+1] == 0) {
                return false;
            }
        }
    }
    return true;
}

void count_pieces(int field[][HEIGHT], int *p1, int *p2) {
    *p1 = *p2 = 0;
    for (int x = 0; x < WIDTH; x++) {
        for (int y = 0; y < HEIGHT; y++) {
            if (field[x][y] == 1) (*p1)++;
            else if (field[x][y] == 2) (*p2)++;
        }
    }
}

// ==================== FELDGENERATION ====================

void generate_random_field(int field[][HEIGHT], int *current_player) {
    memset(field, 0, sizeof(int) * WIDTH * HEIGHT);

    int num_moves = (rand() % 35) + 1;
    *current_player = 1;

    int moves = 0;
    int attempts = 0;

    while (moves < num_moves && attempts < 1000) {
        int col = rand() % WIDTH;
        if (!is_column_full(field, col)) {
            int y = make_move(field, col, *current_player);

            if (check_win(field) != 0) {
                undo_move(field, col, y);
                break;
            }

            moves++;
            *current_player = (*current_player == 1) ? 2 : 1;
        }
        attempts++;
    }
}

// ==================== EVALUATOR ====================

int get_best_move(int field[][HEIGHT], int current_player,
                  const char *eval_program, int max_depth) {
    static int file_counter = 0;
    char in[256], out[256];

    snprintf(in, sizeof(in), "data/connect4_input_%d.txt", file_counter);
    snprintf(out, sizeof(out), "data/connect4_output_%d.txt", file_counter);
    file_counter++;

    FILE *f = fopen(in, "w");
    if (!f) return -1;

    fprintf(f, "%d\n", current_player);
    for (int x = 0; x < WIDTH; x++) {
        for (int y = 0; y < HEIGHT; y++) {
            fprintf(f, "%d ", field[x][y]);
        }
        fprintf(f, "\n");
    }
    fclose(f);

    char cmd[512];
#ifdef _WIN32
    snprintf(cmd, sizeof(cmd), "%s %d 0 < %s > %s 2>nul",
             eval_program, max_depth, in, out);
#else
    snprintf(cmd, sizeof(cmd), "%s %d 0 < %s > %s 2>/dev/null",
             eval_program, max_depth, in, out);
#endif
    system(cmd);

    FILE *fo = fopen(out, "r");
    if (!fo) return -1;

    int best = -1;
    char line[128];
    while (fgets(line, sizeof(line), fo)) {
        sscanf(line, "%d", &best);
    }
    fclose(fo);

    remove(in);
    remove(out);

    return best;
}

// ==================== CSV (KORREKTES SCHEMA) ====================

void write_csv_line(FILE *f, int field[][HEIGHT], int best_move) {
    // spaltenweise: x außen, y innen
    for (int x = 0; x < WIDTH; x++) {
        for (int y = 0; y < HEIGHT; y++) {
            fprintf(f, "%d", field[x][y]);
            if (!(x == WIDTH-1 && y == HEIGHT-1)) {
                fprintf(f, ",");
            }
        }
    }
    fprintf(f, ",%d\n", best_move);
}

// ==================== MAIN ====================

int main(int argc, char *argv[]) {
    const char *eval_program = "minmax_alpha_beta.exe";
    int num_positions = 100000;
    int max_depth = 10;
    const char *output_file = "data/training_data.csv";

    if (argc > 1) eval_program = argv[1];
    if (argc > 2) num_positions = atoi(argv[2]);
    if (argc > 3) max_depth = atoi(argv[3]);
    if (argc > 4) output_file = argv[4];

    srand(time(NULL));

#ifdef _WIN32
    system("if not exist data mkdir data");
#else
    system("mkdir -p data");
#endif

    FILE *fout = fopen(output_file, "w");
    if (!fout) return 1;

    // Header passend zum Schema
    int idx = 0;
    for (int x = 0; x < WIDTH; x++) {
        for (int y = 0; y < HEIGHT; y++) {
            fprintf(fout, "pos%d,", idx++);
        }
    }
    fprintf(fout, "best_move\n");

    int generated = 0;
    int attempts = 0;

    while (generated < num_positions && attempts < num_positions * 3) {
        attempts++;

        int field[WIDTH][HEIGHT];
        int current_player;

        generate_random_field(field, &current_player);

        if (!is_valid_field(field)) continue;
        if (check_win(field) != 0) continue;

        int c1, c2;
        count_pieces(field, &c1, &c2);
        if (abs(c1 - c2) > 1) continue;

        int best = get_best_move(field, current_player, eval_program, max_depth);
        if (best >= 0 && best < WIDTH) {
            write_csv_line(fout, field, best);
            generated++;
        }
    }

    fclose(fout);
    return 0;
}
