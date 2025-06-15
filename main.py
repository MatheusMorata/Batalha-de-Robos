import multiprocessing as mp
import time
import random
import signal
import sys
import os

# Imports da estrutura existente (adaptados)
from processo.Robo import Robo
from view.Tabuleiro import VisualizadorTabuleiro  # Visualizador existente

# Novos imports para compliance
from processo.game_state import GameState
from processo.lock_manager import LockManager

class ArenaManager:
    """Gerenciador principal da arena - integra com código existente"""

    def __init__(self):
        self.game_state = None
        self.lock_manager = None
        self.robot_processes = []
        self.viewer_process = None

    def initialize_game(self):
        """Inicializa o ambiente do jogo"""
        print("🚀 Iniciando Arena dos Processos...")

        # Criar memória compartilhada
        print("📝 Criando memória compartilhada...")
        self.game_state = GameState("batalha_robos", create=True)

        # Criar sistema de locks
        print("🔒 Criando sistema de locks...")
        self.lock_manager = LockManager()

        # Inicializar ambiente (barreiras, baterias, etc.)
        self._setup_environment()

        print("✅ Inicialização concluída!")

    def _setup_environment(self):
        """Configura o ambiente inicial do jogo"""
        print("🏗️  Inicializando ambiente...")

        # Criar barreiras nas bordas
        for x in range(40):
            self.game_state.set_grid_cell(x, 0, '#')  # Borda superior
            self.game_state.set_grid_cell(x, 19, '#')  # Borda inferior

        for y in range(20):
            self.game_state.set_grid_cell(0, y, '#')  # Borda esquerda
            self.game_state.set_grid_cell(39, y, '#')  # Borda direita

        # Adicionar barreiras internas aleatórias
        barriers_count = 0
        while barriers_count < 6:
            x = random.randint(1, 38)
            y = random.randint(1, 18)
            if self.game_state.get_grid_cell(x, y) == ' ':
                self.game_state.set_grid_cell(x, y, '#')
                barriers_count += 1

        # Posicionar baterias
        batteries_count = 0
        while batteries_count < 10:
            x = random.randint(1, 38)
            y = random.randint(1, 18)
            if self.game_state.get_grid_cell(x, y) == ' ':
                self.game_state.set_grid_cell(x, y, 'S')
                batteries_count += 1

        # Posicionar robôs iniciais
        robot_positions = [(5, 5), (35, 5), (5, 15), (35, 15)]
        for i, (x, y) in enumerate(robot_positions):
            self.game_state.set_grid_cell(x, y, str(i))
            self.game_state.set_robot_data(
                i,
                forca=random.randint(1, 10),
                energia=random.randint(40, 100),
                velocidade=random.randint(1, 5),
                pos_x=x,
                pos_y=y,
                status=1
            )

        # Marcar inicialização como concluída
        self.game_state.set_flag('init_done', 1)

        print(f"✅ Ambiente inicializado: 6 barreiras internas, 10 baterias")

    def create_robots(self):
        """Cria e inicia os processos dos robôs"""
        print("🤖 Criando robôs...")
        for robot_id in range(4):
            robot_attrs = {
                'id': robot_id,
                'forca': random.randint(1, 10),
                'energia': random.randint(10, 100),
                'velocidade': random.randint(1, 5),
                'pos_x': random.randint(1, 38),
                'pos_y': random.randint(1, 18),
                'status': 1  # 1 para vivo
            }
            # Usar a classe existente Robo
            robot_process = mp.Process(
                target=run_robot_process,
                args=(
                    self.game_state.name,
                    self.lock_manager,
                    robot_id,
                    robot_attrs
                )
            )
            robot_process.start()
            self.robot_processes.append(robot_process)

            robot_data = self.game_state.get_robot_data(robot_id)
            print(f"✅ Robô {robot_id} iniciado (Força:{robot_attrs['forca']}, Energia:{robot_attrs['energia']}, Velocidade:{robot_attrs['velocidade']})")


    def _robot_main(self, robot_id, shm_name):
        """Função principal de cada processo robô"""
        try:
            # Conectar à memória compartilhada
            game_state = GameState(shm_name, create=False)
            lock_manager = LockManager()

            # Criar e iniciar o robô usando a estrutura existente
            # Mas com as modificações necessárias
            robot = Robo(robot_id, game_state, lock_manager)
            robot.run()

        except Exception as e:
            print(f"❌ Erro no robô {robot_id}: {e}")

    def start_viewer(self):
        """Inicia o visualizador usando o código existente modificado"""
        print("🖥️  Iniciando visualizador...")

        self.viewer_process = VisualizadorTabuleiro(
            self.game_state.name,
            self.lock_manager
        )

        self.viewer_process.start()

    def _viewer_main(self, shm_name):
        """Processo visualizador modificado"""
        try:
            # Usar a classe existente VisualizadorTabuleiro com modificações
            game_state = GameState(shm_name, create=False)
            viewer = VisualizadorTabuleiro(game_state)
            viewer.run()

        except Exception as e:
            print(f"❌ Erro no visualizador: {e}")

    def wait_for_game_end(self):
        """Aguarda o fim do jogo"""
        try:
            while not self.game_state.get_flag('game_over'):
                time.sleep(0.5)

                # Verificar se ainda há robôs vivos
                robots_alive = 0
                for i in range(4):
                    robot_data = self.game_state.get_robot_data(i)
                    if robot_data and robot_data['status'] == 1:
                        robots_alive += 1

                if robots_alive <= 1:
                    self.game_state.set_flag('game_over', 1)
                    if robots_alive == 1:
                        # Encontrar o vencedor
                        for i in range(4):
                            robot_data = self.game_state.get_robot_data(i)
                            if robot_data and robot_data['status'] == 1:
                                self.game_state.set_flag('winner_id', i)
                                break

        except KeyboardInterrupt:
            print("\n⏹️  Jogo interrompido pelo usuário")

    def cleanup(self):
        """Limpa todos os recursos"""
        print("🧹 Limpando recursos...")

        # Terminar processos
        for process in self.robot_processes:
            if process.is_alive():
                process.terminate()
                process.join(timeout=2)

        if self.viewer_process and self.viewer_process.is_alive():
            self.viewer_process.terminate()
            self.viewer_process.join(timeout=2)

        # Limpar memória compartilhada
        if self.game_state:
            self.game_state.cleanup()

        print("✅ Limpeza concluída!")

    def print_game_summary(self):
        """Imprime o resumo do jogo (com tratamento de erro)"""
        print("\n" + "="*50)
        print("RESUMO DO JOGO")
        print("="*50)

        try:
            if self.game_state and self.game_state.shm:
                winner_id = self.game_state.get_flag('winner_id')
                if winner_id >= 0:
                    print(f"🏆 Vencedor: Robô {winner_id}")
                else:
                    print("🏆 Nenhum vencedor (empate ou erro)")
            else:
                print("⚠️ Estado do jogo não disponível")

        except Exception as e:
            print(f"❌ Erro ao gerar resumo: {str(e)}")

def signal_handler(signum, frame):
    """Handler para sinais do sistema"""
    print("\n⏹️  Recebido sinal de interrupção...")
    sys.exit(0)

def run_robot_process(shm_name, lock_manager, robo_id, robot_attrs):
    # 1. Conecta ao estado de jogo compartilhado existente
    game_state = GameState(name=shm_name, create=False)

    # 2. Atualiza os dados do robô na memória compartilhada
    game_state.set_robot_data(robo_id, **robot_attrs)

    # 3. Cria a instância do Robô
    robo = Robo(robo_id, game_state, lock_manager)

    # 4. Inicia a execução do robô
    robo.run()

def main():
    """Função principal - integrada com estrutura existente"""

    # Configurar handler de sinais
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Banner do jogo
    print("🤖 ARENA DOS PROCESSOS - BATALHA DOS ROBÔS AUTÔNOMOS 🤖")
    print()

    arena = ArenaManager()

    try:
        # Inicializar jogo
        arena.initialize_game()

        # Criar robôs
        arena.create_robots()

        # Aguardar estabilização
        print("⏳ Aguardando estabilização do sistema...")
        time.sleep(2)

        # Iniciar visualizador
        arena.start_viewer()

        print("="*60)
        print("ARENA DOS PROCESSOS - BATALHA DOS ROBÔS AUTÔNOMOS")
        print("="*60)
        print("Pressione 'q' no visualizador para sair")
        print("Ctrl+C para interromper o programa")
        print("="*60)
        print()

        # Aguardar fim do jogo
        arena.wait_for_game_end()

        # Imprimir resumo
        arena.print_game_summary()

    except Exception as e:
        print(f"❌ Erro durante execução: {e}")
        import traceback
        traceback.print_exc()

    finally:
        arena.cleanup()
        print("\n👋 Obrigado por jogar Arena dos Processos!")

if __name__ == "__main__":
    mp.set_start_method('spawn', force=True)  # Compatibilidade multiplataforma
    main()