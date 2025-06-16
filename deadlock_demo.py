import threading
import time
import random
import logging
import multiprocessing as mp
from processo.game_state import GameState
from processo.lock_manager import LockManager
import os


class DeadlockDemoRobot:
    """
    Robô que deliberadamente causa deadlock para demonstração.
    Viola a ordem hierárquica de locks.
    """

    def __init__(self, robot_id, game_state, lock_manager):
        self.robot_id = robot_id
        self.game_state = game_state
        self.lock_manager = lock_manager
        self.running = True
        self.logger = None

    def run(self):
        """Executa o robô que causará deadlock."""
        logging.basicConfig(
            level=logging.INFO,
            format=f'[DEADLOCK-{self.robot_id}] %(asctime)s - %(message)s',
            filename=f'deadlock_demo_{self.robot_id}.log',
            filemode='w'  # 'w' para sobrescrever o log a cada execução
        )
        self.logger = logging.getLogger(f'deadlock_{self.robot_id}')

        self.logger.info(f"Robô {self.robot_id} iniciado - MODO DEADLOCK")

        # Criar threads com comportamento de deadlock
        sense_thread = threading.Thread(target=self.deadlock_sense_act, daemon=True)
        house_thread = threading.Thread(target=self.deadlock_housekeeping, daemon=True)

        sense_thread.start()
        house_thread.start()

        sense_thread.join()
        house_thread.join()

    def deadlock_sense_act(self):
        """Thread que causa deadlock intencionalmente."""
        time.sleep(1)  # Aguardar outros robôs iniciarem

        # Loop para garantir que o deadlock ocorra
        for _ in range(5):  # Tenta provocar o deadlock algumas vezes
            if not self.running: break
            try:
                self.logger.info("Iniciando sequência de deadlock...")

                if self.robot_id % 2 == 0:
                    # Robôs pares: battery_mutex -> grid_mutex (ORDEM ERRADA!)
                    self.logger.info("Tentando adquirir battery_mutex[0]...")
                    if self.lock_manager.battery_mutexes[0].acquire(timeout=5):
                        self.logger.info("battery_mutex[0] adquirido.")
                        time.sleep(0.5)  # Aumentar chance de deadlock

                        self.logger.info("Tentando adquirir grid_mutex...")
                        if self.lock_manager.grid_mutex.acquire(timeout=5):
                            self.logger.info("grid_mutex adquirido.")
                            self.lock_manager.grid_mutex.release()
                            self.logger.info("grid_mutex liberado.")
                        else:
                            self.logger.warning("TIMEOUT em grid_mutex - POSSÍVEL DEADLOCK!")

                        self.lock_manager.battery_mutexes[0].release()
                        self.logger.info("battery_mutex[0] liberado.")
                    else:
                        self.logger.warning("TIMEOUT em battery_mutex[0]")

                else:
                    # Robôs ímpares: grid_mutex -> battery_mutex (ORDEM ERRADA!)
                    self.logger.info("Tentando adquirir grid_mutex...")
                    if self.lock_manager.grid_mutex.acquire(timeout=5):
                        self.logger.info("grid_mutex adquirido.")
                        time.sleep(0.5)  # Aumentar chance de deadlock

                        self.logger.info("Tentando adquirir battery_mutex[0]...")
                        if self.lock_manager.battery_mutexes[0].acquire(timeout=5):
                            self.logger.info("battery_mutex[0] adquirido.")
                            self.lock_manager.battery_mutexes[0].release()
                            self.logger.info("battery_mutex[0] liberado.")
                        else:
                            self.logger.warning("TIMEOUT em battery_mutex[0] - POSSÍVEL DEADLOCK!")

                        self.lock_manager.grid_mutex.release()
                        self.logger.info("grid_mutex liberado.")
                    else:
                        self.logger.warning("TIMEOUT em grid_mutex")

                time.sleep(1)

            except Exception as e:
                self.logger.error(f"Erro em deadlock_sense_act: {e}")

        self.running = False

    def deadlock_housekeeping(self):
        """Thread de manutenção simples para a demonstração."""
        while self.running:
            time.sleep(3)
            self.logger.info("Housekeeping em execução.")


class DeadlockDetector:
    """Detector de deadlock simplificado para a demonstração."""

    def __init__(self, lock_manager):
        self.lock_manager = lock_manager
        self.running = True
        self.logger = None

    def run(self):
        """Executa o detector de deadlock."""
        # CONFIGURAÇÃO DO LOG DENTRO DO PROCESSO FILHO
        logging.basicConfig(
            level=logging.INFO,
            format='[DETECTOR] %(asctime)s - %(message)s',
            filename='deadlock_detector.log',
            filemode='w'
        )
        self.logger = logging.getLogger('deadlock_detector')

        self.logger.info("Detector de deadlock iniciado.")

        detector_thread = threading.Thread(target=self._detect_loop, daemon=True)
        detector_thread.start()
        detector_thread.join()

    def _detect_loop(self):
        """Loop principal de detecção."""
        # Dê tempo para os robôs começarem a competir pelos locks
        time.sleep(2)

        self.logger.info("Verificando estado dos locks para detecção de deadlock...")

        # Tenta adquirir os locks com timeout curto. Se falhar, é um forte indício de deadlock.
        locked_by_others = []

        if not self.lock_manager.grid_mutex.acquire(timeout=0.1):
            locked_by_others.append("grid_mutex")
        else:
            self.lock_manager.grid_mutex.release()

        if not self.lock_manager.battery_mutexes[0].acquire(timeout=0.1):
            locked_by_others.append("battery_mutexes[0]")
        else:
            self.lock_manager.battery_mutexes[0].release()

        if len(locked_by_others) > 1:
            self.logger.error(f"DEADLOCK DETECTADO! Locks indisponíveis: {locked_by_others}")
        else:
            self.logger.info("Nenhum deadlock detectado nesta verificação.")

        self.running = False


def demonstrate_deadlock():
    """Função principal para demonstrar deadlock."""
    print("INICIANDO DEMONSTRAÇÃO DE DEADLOCK")
    # Limpar logs antigos
    for i in range(2):
        if os.path.exists(f'deadlock_demo_{i}.log'): os.remove(f'deadlock_demo_{i}.log')
    if os.path.exists('deadlock_detector.log'): os.remove('deadlock_detector.log')

    game_state = GameState("deadlock_demo", create=True)
    lock_manager = LockManager()

    robots = [DeadlockDemoRobot(i, game_state, lock_manager) for i in range(2)]
    detector = DeadlockDetector(lock_manager)

    processes = []
    for robot in robots:
        p = mp.Process(target=robot.run)
        processes.append(p)

    detector_process = mp.Process(target=detector.run)
    processes.append(detector_process)

    for p in processes:
        p.start()

    print("Demonstração em andamento... Verifique os logs em ~15 segundos:")
    print("tail -f deadlock_demo_0.log deadlock_demo_1.log deadlock_detector.log")

    try:
        # Aguardar processos terminarem
        for p in processes:
            p.join(timeout=20)
    except KeyboardInterrupt:
        print("\nDemonstração interrompida.")
    finally:
        for p in processes:
            if p.is_alive():
                p.terminate()
        game_state.cleanup()
        print("\nDemonstração concluída.")


if __name__ == "__main__":
    # Garante compatibilidade entre sistemas operacionais
    mp.set_start_method('spawn', force=True)
    demonstrate_deadlock()