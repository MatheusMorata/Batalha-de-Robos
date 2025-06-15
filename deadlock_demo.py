import threading
import time
import random
import logging
from processo.game_state import GameState
from processo.lock_manager import LockManager

class DeadlockDemoRobot:
    """
    Robô que deliberadamente causa deadlock para demonstração
    Viola a ordem hierárquica de locks
    """

    def __init__(self, robot_id, game_state, lock_manager):
        self.robot_id = robot_id
        self.game_state = game_state
        self.lock_manager = lock_manager
        self.running = True

        # Logger específico para deadlock
        logging.basicConfig(
            level=logging.INFO,
            format=f'[DEADLOCK-{robot_id}] %(asctime)s - %(message)s',
            filename=f'deadlock_demo_{robot_id}.log'
        )
        self.logger = logging.getLogger(f'deadlock_{robot_id}')

    def run(self):
        """Executa o robô que causará deadlock"""
        print(f"Robô {self.robot_id} iniciado - MODO DEADLOCK")

        # Criar threads com comportamento de deadlock
        sense_thread = threading.Thread(target=self.deadlock_sense_act, daemon=True)
        house_thread = threading.Thread(target=self.deadlock_housekeeping, daemon=True)

        sense_thread.start()
        house_thread.start()

        # Aguardar deadlock ou finalização
        try:
            while self.running:
                time.sleep(0.1)
        except KeyboardInterrupt:
            self.running = False

    def deadlock_sense_act(self):
        """Thread que causa deadlock intencionalmente"""
        time.sleep(1)  # Aguardar outros robôs iniciarem

        while self.running:
            try:
                self.logger.info("Iniciando sequência de deadlock...")

                if self.robot_id % 2 == 0:
                    # Robôs pares: battery_mutex -> grid_mutex (ORDEM ERRADA!)
                    self.logger.info("Tentando adquirir battery_mutex...")
                    if self.lock_manager.battery_mutexes[0].acquire(timeout=2):
                        self.logger.info("battery_mutex adquirido")

                        time.sleep(1)  # Aumentar chance de deadlock

                        self.logger.info("Tentando adquirir grid_mutex...")
                        if self.lock_manager.grid_mutex.acquire(timeout=2):
                            self.logger.info("grid_mutex adquirido")

                            # Simular trabalho
                            time.sleep(0.5)

                            self.lock_manager.grid_mutex.release()
                            self.logger.info("grid_mutex liberado")
                        else:
                            self.logger.warning("TIMEOUT em grid_mutex - possível deadlock!")

                        self.lock_manager.battery_mutexes[0].release()
                        self.logger.info("battery_mutex liberado")
                    else:
                        self.logger.warning("TIMEOUT em battery_mutex")

                else:
                    # Robôs ímpares: grid_mutex -> battery_mutex (ORDEM ERRADA!)
                    self.logger.info("Tentando adquirir grid_mutex...")
                    if self.lock_manager.grid_mutex.acquire(timeout=2):
                        self.logger.info("grid_mutex adquirido")

                        time.sleep(1)  # Aumentar chance de deadlock

                        self.logger.info("Tentando adquirir battery_mutex...")
                        if self.lock_manager.battery_mutexes[0].acquire(timeout=2):
                            self.logger.info("battery_mutex adquirido")

                            # Simular trabalho
                            time.sleep(0.5)

                            self.lock_manager.battery_mutexes[0].release()
                            self.logger.info("battery_mutex liberado")
                        else:
                            self.logger.warning("TIMEOUT em battery_mutex - possível deadlock!")

                        self.lock_manager.grid_mutex.release()
                        self.logger.info("grid_mutex liberado")
                    else:
                        self.logger.warning("TIMEOUT em grid_mutex")

                time.sleep(random.uniform(0.5, 2.0))  # Intervalo aleatório

            except Exception as e:
                self.logger.error(f"Erro em deadlock_sense_act: {e}")
                time.sleep(1)

    def deadlock_housekeeping(self):
        """Thread de manutenção que também participa do deadlock"""
        time.sleep(2)  # Aguardar início

        while self.running:
            try:
                self.logger.info("Housekeeping - tentando acessar recursos...")

                # Tentar acessar recursos de forma conflitante
                if self.robot_id % 2 == 1:
                    # Robôs ímpares também tentam battery -> grid
                    if self.lock_manager.battery_mutexes[1].acquire(timeout=1):
                        time.sleep(0.5)
                        if self.lock_manager.grid_mutex.acquire(timeout=1):
                            self.logger.info("Housekeeping: recursos adquiridos")
                            time.sleep(0.2)
                            self.lock_manager.grid_mutex.release()
                        else:
                            self.logger.warning("Housekeeping: TIMEOUT em grid_mutex")
                        self.lock_manager.battery_mutexes[1].release()
                    else:
                        self.logger.warning("Housekeeping: TIMEOUT em battery_mutex")

                time.sleep(3)  # Intervalo de housekeeping

            except Exception as e:
                self.logger.error(f"Erro em deadlock_housekeeping: {e}")
                time.sleep(2)

class DeadlockDetector:
    """
    Detector de deadlock usando timeouts e análise de estado
    """

    def __init__(self, lock_manager):
        self.lock_manager = lock_manager
        self.running = True
        self.detected_deadlocks = 0

        logging.basicConfig(
            level=logging.INFO,
            format='[DETECTOR] %(asctime)s - %(message)s',
            filename='deadlock_detector.log'
        )
        self.logger = logging.getLogger('deadlock_detector')

    def run(self):
        """Executa o detector de deadlock"""
        print("Detector de deadlock iniciado")

        detector_thread = threading.Thread(target=self._detect_loop, daemon=True)
        detector_thread.start()

        try:
            while self.running:
                time.sleep(0.1)
        except KeyboardInterrupt:
            self.running = False

    def _detect_loop(self):
        """Loop principal de detecção"""
        while self.running:
            try:
                time.sleep(5)  # Verificar a cada 5 segundos

                # Tentar adquirir todos os locks com timeout muito baixo
                deadlock_detected = False

                # Teste de detecção por timeout
                if not self.lock_manager.grid_mutex.acquire(timeout=0.1):
                    self.logger.warning("grid_mutex indisponível por muito tempo")
                    deadlock_detected = True
                else:
                    self.lock_manager.grid_mutex.release()

                # Verificar battery mutexes
                for i, battery_mutex in enumerate(self.lock_manager.battery_mutexes[:2]):
                    if not battery_mutex.acquire(timeout=0.1):
                        self.logger.warning(f"battery_mutex[{i}] indisponível por muito tempo")
                        deadlock_detected = True
                    else:
                        battery_mutex.release()

                if deadlock_detected:
                    self.detected_deadlocks += 1
                    self.logger.error(f"DEADLOCK DETECTADO #{self.detected_deadlocks}")
                    print(f"DEADLOCK DETECTADO #{self.detected_deadlocks}")

                    # Estratégia de recuperação (opcional)
                    # self._recover_from_deadlock()

            except Exception as e:
                self.logger.error(f"Erro no detector: {e}")
                time.sleep(2)

    def _recover_from_deadlock(self):
        """Estratégia simples de recuperação de deadlock"""
        self.logger.info("Tentando recuperação de deadlock...")

        # Forçar liberação de recursos (estratégia drástica)
        # Em um sistema real, seria mais sofisticado
        try:
            # Aguardar um pouco e tentar novamente
            time.sleep(2)
            self.logger.info("Recuperação tentada")
        except Exception as e:
            self.logger.error(f"Erro na recuperação: {e}")

def demonstrate_deadlock():
    """Função principal para demonstrar deadlock"""
    print("INICIANDO DEMONSTRAÇÃO DE DEADLOCK")
    print("="*50)

    # Criar sistema
    game_state = GameState("deadlock_demo", create=True)
    lock_manager = LockManager()

    # Criar robôs que causarão deadlock
    robots = []
    for i in range(2):  # Apenas 2 robôs para simplificar
        robot = DeadlockDemoRobot(i, game_state, lock_manager)
        robots.append(robot)

    # Criar detector
    detector = DeadlockDetector(lock_manager)

    # Iniciar tudo
    import multiprocessing as mp

    processes = []

    # Processos dos robôs
    for i, robot in enumerate(robots):
        p = mp.Process(target=robot.run)
        p.start()
        processes.append(p)

    # Processo do detector
    detector_process = mp.Process(target=detector.run)
    detector_process.start()
    processes.append(detector_process)

    try:
        print("Aguardando deadlock ocorrer...")
        print("Verifique os logs: deadlock_demo_0.log, deadlock_demo_1.log, deadlock_detector.log")

        # Aguardar por um tempo para observar o deadlock
        time.sleep(30)

    except KeyboardInterrupt:
        print("\nDemonstração interrompida")

    finally:
        # Terminar processos
        for p in processes:
            if p.is_alive():
                p.terminate()
                p.join(timeout=2)

        # Limpar recursos
        game_state.cleanup()
        print("- Verifique os arquivos de log para detalhes")

if __name__ == "__main__":
    demonstrate_deadlock()
