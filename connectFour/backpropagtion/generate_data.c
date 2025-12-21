#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <time.h>
#include <unistd.h>

#define WIDTH 7
#define HEIGHT 6
#define MAX_POSITIONS 100000

// Prüft ob das Spielfeld einen Gewinner hat
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
    
    // Diagonal (aufsteigend)
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
    
    // Diagonal (absteigend)
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
    
    return 0; // Kein Gewinner
}

// Prüft ob eine Spalte voll ist
bool is_column_full(int field[][HEIGHT], int col) {
    return field[col][0] != 0;
}

// Macht einen Zug in einer Spalte
int make_move(int field[][HEIGHT], int col, int player) {
    for (int y = HEIGHT - 1; y >= 0; y--) {
        if (field[col][y] == 0) {
            field[col][y] = player;
            return y;
        }
    }
    return -1; // Spalte voll
}

// Macht einen Zug rückgängig
void undo_move(int field[][HEIGHT], int col, int y) {
    field[col][y] = 0;
}

// Prüft ob das Feld physikalisch korrekt ist (keine schwebenden Steine)
bool is_valid_field(int field[][HEIGHT]) {
    for (int x = 0; x < WIDTH; x++) {
        for (int y = 0; y < HEIGHT - 1; y++) {
            if (field[x][y] != 0 && field[x][y+1] == 0) {
                return false; // Stein schwebt
            }
        }
    }
    return true;
}

// Zählt die Anzahl der Steine auf dem Feld
void count_pieces(int field[][HEIGHT], int *p1_count, int *p2_count) {
    *p1_count = 0;
    *p2_count = 0;
    for (int x = 0; x < WIDTH; x++) {
        for (int y = 0; y < HEIGHT; y++) {
            if (field[x][y] == 1) (*p1_count)++;
            else if (field[x][y] == 2) (*p2_count)++;
        }
    }
}

// Generiert ein zufälliges legales Spielfeld
void generate_random_field(int field[][HEIGHT], int *current_player) {
    // Leeres Feld
    memset(field, 0, sizeof(int) * WIDTH * HEIGHT);
    
    // Zufällige Anzahl von Zügen (1 bis 35)
    int num_moves = (rand() % 35) + 1;
    
    *current_player = 1;
    int moves_made = 0;
    int attempts = 0;
    
    while (moves_made < num_moves && attempts < 1000) {
        // Zufällige Spalte wählen
        int col = rand() % WIDTH;
        
        if (!is_column_full(field, col)) {
            make_move(field, col, *current_player);
            
            // Prüfen ob jemand gewonnen hat
            if (check_win(field) != 0) {
                // Letzten Zug rückgängig machen
                for (int y = 0; y < HEIGHT; y++) {
                    if (field[col][y] == *current_player) {
                        undo_move(field, col, y);
                        break;
                    }
                }
                break; // Spielfeld fertig (vor Gewinn)
            }
            
            moves_made++;
            *current_player = (*current_player == 1) ? 2 : 1;
        }
        attempts++;
    }
}

// Ruft das Bewertungsprogramm auf und holt den besten Zug
int get_best_move(int field[][HEIGHT], int current_player, const char *eval_program, int max_depth) {
    // Temporäre Dateien für Ein- und Ausgabe im data-Ordner
    static int file_counter = 0;
    char input_file[256];
    char output_file[256];
    
    snprintf(input_file, sizeof(input_file), "data/connect4_input_%d.txt", file_counter);
    snprintf(output_file, sizeof(output_file), "data/connect4_output_%d.txt", file_counter);
    file_counter++;
    
    // Input-Datei schreiben
    FILE *fin = fopen(input_file, "w");
    if (!fin) {
        perror("fopen input");
        return -1;
    }
    
    fprintf(fin, "%d\n", current_player);
    for (int x = 0; x < WIDTH; x++) {
        for (int y = 0; y < HEIGHT; y++) {
            fprintf(fin, "%d ", field[x][y]);
        }
        fprintf(fin, "\n");
    }
    fclose(fin);
    
    // Bewertungsprogramm aufrufen
    char command[1024];
    #ifdef _WIN32
        snprintf(command, sizeof(command), "%s %d 0 < %s > %s 2>nul", 
                 eval_program, max_depth, input_file, output_file);
    #else
        snprintf(command, sizeof(command), "%s %d 0 < %s > %s 2>/dev/null", 
                 eval_program, max_depth, input_file, output_file);
    #endif
    
    int result = system(command);
    
    // Output-Datei lesen
    FILE *fout = fopen(output_file, "r");
    if (!fout) {
        perror("fopen output");
        remove(input_file);
        remove(output_file);
        return -1;
    }
    
    int best_move = -1;
    char line[256];
    
    // Letzte Zeile mit der Zahl finden
    while (fgets(line, sizeof(line), fout)) {
        if (sscanf(line, " %d", &best_move) == 1) {
            // Gefunden
        }
    }
    
    fclose(fout);
    
    // Temporäre Dateien löschen
    remove(input_file);
    remove(output_file);
    
    return best_move;
}

// Schreibt eine Zeile in die CSV-Datei
void write_csv_line(FILE *f, int field[][HEIGHT], int best_move) {
    // 42 Feldwerte schreiben
    for (int y = 0; y < HEIGHT; y++) {
        for (int x = 0; x < WIDTH; x++) {
            fprintf(f, "%d", field[x][y]);
            if (!(y == HEIGHT-1 && x == WIDTH-1)) {
                fprintf(f, ",");
            }
        }
    }
    // Bester Zug
    fprintf(f, ",%d\n", best_move);
}

int main(int argc, char *argv[]) {
    // Standardwerte
    const char *eval_program = "minmax_alpha_beta.exe";
    int num_positions = 1000;
    int max_depth = 8;
    const char *output_file = "data/training_data.csv";
    
    // Optionale Argumente überschreiben Standardwerte
    if (argc > 1) eval_program = argv[1];
    if (argc > 2) num_positions = atoi(argv[2]);
    if (argc > 3) max_depth = atoi(argv[3]);
    if (argc > 4) output_file = argv[4];
    
    srand(time(NULL));
    
    // data-Ordner erstellen, falls nicht vorhanden
    #ifdef _WIN32
        system("if not exist data mkdir data");
    #else
        system("mkdir -p data");
    #endif
    
    // Prüfen ob Bewertungsprogramm existiert
    FILE *test = fopen(eval_program, "r");
    if (!test) {
        printf("Error: Cannot find evaluation program: %s\n", eval_program);
        printf("Please make sure the file exists in the current directory.\n");
        return 1;
    }
    fclose(test);
    
    FILE *fout = fopen(output_file, "w");
    if (!fout) {
        perror("fopen output file");
        return 1;
    }
    
    // CSV-Header schreiben
    for (int i = 0; i < WIDTH * HEIGHT; i++) {
        fprintf(fout, "pos%d,", i);
    }
    fprintf(fout, "best_move\n");
    
    printf("Generating %d training positions...\n", num_positions);
    printf("Using evaluation program: %s\n", eval_program);
    printf("Max depth: %d\n", max_depth);
    printf("Output file: %s\n\n", output_file);
    
    int valid_positions = 0;
    int attempts = 0;
    
    while (valid_positions < num_positions && attempts < num_positions * 3) {
        attempts++;
        
        int field[WIDTH][HEIGHT];
        int current_player;
        
        // Zufälliges Spielfeld generieren
        generate_random_field(field, &current_player);
        
        // Validierung
        if (!is_valid_field(field)) continue;
        if (check_win(field) != 0) continue; // Spiel bereits vorbei
        
        // Spielerzahl validieren
        int p1_count, p2_count;
        count_pieces(field, &p1_count, &p2_count);
        if (abs(p1_count - p2_count) > 1) continue;
        
        // Besten Zug berechnen
        int best_move = get_best_move(field, current_player, eval_program, max_depth);
        
        if (best_move >= 0 && best_move < WIDTH) {
            write_csv_line(fout, field, best_move);
            valid_positions++;
            
            if (valid_positions % 100 == 0) {
                printf("Progress: %d/%d positions generated (%.1f%%)\n", 
                       valid_positions, num_positions, 
                       100.0 * valid_positions / num_positions);
                fflush(stdout);
            }
        }
    }
    
    fclose(fout);
    
    printf("\nDone! Generated %d positions in %d attempts.\n", valid_positions, attempts);
    printf("Data saved to: %s\n", output_file);
    
    return 0;
}