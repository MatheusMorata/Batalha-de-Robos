import curses
import time
import multiprocessing
import threading
from processo.game_state import GameState

class VisualizadorTabuleiro(multiprocessing.Process):

    def __init__(self, shm_name, lock_manager):
        super().__init__(daemon=True)
        self.shm_name = shm_name          # Armazena o nome da memória
        self.lock_manager = lock_manager  # Armazena o gerenciador de locks
        self.game_state = None

    def run(self):
        """Este método é executado no novo processo do visualizador."""
        # Conecta à memória compartilhada existente
        self.game_state = GameState(name=self.shm_name, create=False)

        try:
            while not self.game_state.get_flag('game_over'):
                self.draw_board()
                time.sleep(0.1) # Taxa de atualização de 100ms
        except KeyboardInterrupt:
            pass # Permite que o visualizador saia silenciosamente
        finally:
            # Limpa o cursor ao sair
            print("\x1b[?25h", end="")

    def draw_board(self):
        """Renderiza o estado atual do tabuleiro no terminal."""
        acquired_locks = []
        try:
            acquired_locks = self.lock_manager.acquire_multiple(['grid'], timeout=0.5)

            grid_snapshot = [self.game_state.get_grid_cell(x, y) for y in range(20) for x in range(40)]

        except TimeoutError:
            # Se o lock estiver ocupado, pula este frame de renderização
            return
        finally:
            self.lock_manager.release_multiple(acquired_locks)
        # Limpa a tela e posiciona o cursor
        output = "\x1b[H\x1b[J"
        output += "--- ARENA DOS PROCESSOS ---\n"

        for y in range(20):
            for x in range(40):
                # Pega o caractere do snapshot local
                char = grid_snapshot[y * 40 + x]
                output += char if isinstance(char, str) else chr(char)
            output += "\n"
        print(output, end="", flush=True)

    def _main_loop(self, stdscr):
        """Loop principal do visualizador"""
        self.stdscr = stdscr

        # Configurar curses
        curses.curs_set(0)  # Esconder cursor
        stdscr.nodelay(True)  # Não bloquear getch()
        stdscr.timeout(100)  # Timeout de 100ms

        # Inicializar cores se o terminal suportar
        if curses.has_colors():
            curses.start_color()
            curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)     # Robôs
            curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)   # Baterias
            curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)    # Barreiras
            curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Espaços
            curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_BLACK)   # Texto
            self.colors_initialized = True

        # Loop principal de renderização
        while self.running and not self.game_state.get_flag('game_over'):
            try:
                # Verificar entrada do usuário
                key = stdscr.getch()
                if key == ord('q') or key == ord('Q'):
                    break

                # Renderizar tela
                self._render_screen()

                # Aguardar 100ms (conforme especificação 50-200ms)
                time.sleep(0.1)

            except KeyboardInterrupt:
                break
            except Exception as e:
                # Em caso de erro, mostrar informação básica
                stdscr.clear()
                stdscr.addstr(0, 0, f"Erro na renderização: {e}")
                stdscr.refresh()
                time.sleep(1)

    def _render_screen(self):
        """Renderiza a tela completa"""
        if not self.stdscr:
            return

        try:
            self.stdscr.clear()

            # Renderizar cabeçalho
            self._render_header()

            # Renderizar tabuleiro
            self._render_grid()

            # Renderizar informações dos robôs
            self._render_robot_info()

            # Renderizar rodapé
            self._render_footer()

            self.stdscr.refresh()

        except curses.error:
            # Terminal muito pequeno ou outro erro do curses
            pass

    def _render_header(self):
        """Renderiza o cabeçalho"""
        try:
            header = "=== ARENA DOS PROCESSOS - BATALHA DOS ROBÔS AUTÔNOMOS ==="
            if self.colors_initialized:
                self.stdscr.attron(curses.color_pair(5) | curses.A_BOLD)
                self.stdscr.addstr(0, 0, header)
                self.stdscr.attroff(curses.color_pair(5) | curses.A_BOLD)
            else:
                self.stdscr.addstr(0, 0, header)
        except curses.error:
            pass

    def _render_grid(self):
        """Renderiza o tabuleiro 40x20"""
        try:
            start_row = 2

            for y in range(20):
                line = ""
                for x in range(40):
                    cell = self.game_state.get_grid_cell(x, y)
                    if cell:
                        line += cell
                    else:
                        line += " "

                # Adicionar linha com cores apropriadas
                if self.colors_initialized:
                    self._render_colored_line(start_row + y, 0, line)
                else:
                    self.stdscr.addstr(start_row + y, 0, line)

        except curses.error:
            pass

    def _render_colored_line(self, row, col, line):
        """Renderiza uma linha com cores"""
        try:
            current_col = col
            for char in line:
                color_pair = 5  # Padrão branco

                if char == '#':
                    color_pair = 3  # Azul para barreiras
                elif char == '⚡':
                    color_pair = 2  # Verde para baterias
                elif char.isdigit():
                    color_pair = 1  # Vermelho para robôs
                elif char == ' ':
                    color_pair = 4  # Amarelo para espaços

                self.stdscr.attron(curses.color_pair(color_pair))
                self.stdscr.addch(row, current_col, char)
                self.stdscr.attroff(curses.color_pair(color_pair))
                current_col += 1

        except curses.error:
            pass

    def _render_robot_info(self):
        """Renderiza informações dos robôs"""
        try:
            info_row = 23

            if self.colors_initialized:
                self.stdscr.attron(curses.color_pair(5) | curses.A_BOLD)
                self.stdscr.addstr(info_row, 0, "=== INFORMAÇÕES DOS ROBÔS ===")
                self.stdscr.attroff(curses.color_pair(5) | curses.A_BOLD)
            else:
                self.stdscr.addstr(info_row, 0, "=== INFORMAÇÕES DOS ROBÔS ===")

            for i in range(4):
                robot_data = self.game_state.get_robot_data(i)
                if robot_data:
                    status = "VIVO" if robot_data['status'] == 1 else "MORTO"
                    info = (f"Robô {i}: "
                           f"Força={robot_data['forca']} "
                           f"Energia={robot_data['energia']} "
                           f"Velocidade={robot_data['velocidade']} "
                           f"Pos=({robot_data['pos_x']},{robot_data['pos_y']}) "
                           f"Status={status}")

                    color_pair = 1 if robot_data['status'] == 1 else 5
                    if self.colors_initialized:
                        self.stdscr.attron(curses.color_pair(color_pair))
                        self.stdscr.addstr(info_row + 1 + i, 0, info)
                        self.stdscr.attroff(curses.color_pair(color_pair))
                    else:
                        self.stdscr.addstr(info_row + 1 + i, 0, info)

        except curses.error:
            pass

    def _render_footer(self):
        """Renderiza o rodapé com instruções"""
        try:
            footer_row = 28

            instructions = [
                "LEGENDA: # = Barreira, B = Bateria, 0-3 = Robôs",
                "CONTROLES: Pressione 'q' para sair",
                "STATUS: " + ("JOGO ATIVO" if not self.game_state.get_flag('game_over') else "JOGO TERMINADO")
            ]

            for i, instruction in enumerate(instructions):
                if self.colors_initialized:
                    self.stdscr.attron(curses.color_pair(5))
                    self.stdscr.addstr(footer_row + i, 0, instruction)
                    self.stdscr.attroff(curses.color_pair(5))
                else:
                    self.stdscr.addstr(footer_row + i, 0, instruction)

        except curses.error:
            pass