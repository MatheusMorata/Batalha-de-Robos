import threading
import time
import random
import logging

class Robo():
    def __init__(self, robo_id, game_state, lock_manager):
        self.robo_id = robo_id
        self.game_state = game_state
        self.lock_manager = lock_manager
        self.running = True

        # Configurar logging para o robô
        logging.basicConfig(
            level=logging.INFO,
            format=f'[Robô {robo_id}] %(asctime)s - %(message)s',
            filename=f'robot_{robo_id}.log'
        )
        self.logger = logging.getLogger(f'robo_{robo_id}')

        self.sense_act_thread = None
        self.housekeeping_thread = None
        self.simular_deadlock = False # Feature Flag para o deadlock

    # Inicia o processo, que contém duas threads
    def run(self):
        """Inicia e gerencia as threads do robô."""
        print(f"Robô {self.robo_id} ativado.")

        # Inicia a thread de percepção e ação
        self.sense_act_thread = threading.Thread(target=self.sense_act, daemon=True)
        self.sense_act_thread.start()
        print(f"Robô {self.robo_id}: thread sense_act iniciada.")

        # Inicia a thread de manutenção
        self.housekeeping_thread = threading.Thread(target=self.housekeeping, daemon=True)
        self.housekeeping_thread.start()
        print(f"Robô {self.robo_id}: thread housekeeping iniciada.")

        # Mantém o processo do robô vivo enquanto as threads estiverem ativas
        self.sense_act_thread.join()
        self.housekeeping_thread.join()
        print(f"Robô {self.robo_id} encerrando.")

    def _provocar_deadlock(self):
        """Simula deadlock real entre robôs 0 e 1."""
        if self.robo_id == 0:
            self.logger.info("Tentando pegar battery_mutex")
            self.lock_manager.battery_mutexes[0].acquire()
            self.logger.info("Pegou battery_mutex")
            time.sleep(1)
            self.logger.info("Tentando pegar grid_mutex")
            self.lock_manager.grid_mutex.acquire()
            self.logger.info("Pegou grid_mutex")
            self.lock_manager.grid_mutex.release()
            self.lock_manager.battery_mutexes[0].release()
            self.logger.info("Liberou locks")

        elif self.robo_id == 1:
            self.logger.info("Tentando pegar grid_mutex")
            self.lock_manager.grid_mutex.acquire()
            self.logger.info("Pegou grid_mutex")
            time.sleep(1)
            self.logger.info("Tentando pegar battery_mutex")
            self.lock_manager.battery_mutexes[0].acquire()
            self.logger.info("Pegou battery_mutex")
            self.lock_manager.battery_mutexes[0].release()
            self.lock_manager.grid_mutex.release()
            self.logger.info("Liberou locks")

    def _prevenir_deadlock(self):
        """Previne deadlock adquirindo locks sempre na mesma ordem."""
        self.logger.info("Prevenção: adquirindo grid_mutex")
        self.lock_manager.grid_mutex.acquire()
        self.logger.info("Prevenção: adquirindo battery_mutex")
        self.lock_manager.battery_mutexes[0].acquire()
        self.logger.info("Locks adquiridos com sucesso (prevenção)")

        time.sleep(1)  # Simula alguma operação segura

        self.lock_manager.battery_mutexes[0].release()
        self.lock_manager.grid_mutex.release()
        self.logger.info("Locks liberados com sucesso (prevenção)")

    def sense_act(self):
        """
        Thread sense_act - Ciclo principal conforme especificação:
        1. Tira snapshot local do grid (sem lock)
        2. Decide a ação
        3. Adquire locks necessários na ordem documentada
        4. Executa ação
        5. Libera locks
        """
        
        # Lógica da Feature Flag caso deadlock esteja como True ou False
        if self.robo_id in [0, 1] and self.simular_deadlock:
            self._provocar_deadlock()
        elif self.robo_id in [0, 1] and not self.simular_deadlock:
            self._prevenir_deadlock()

        while self.running and not self.game_state.get_flag('game_over'):
            try:
                robot_data = self.game_state.get_robot_data(self.robo_id)
                if not robot_data or robot_data['status'] == 0:
                    break  # Robô morto

                # 1. Snapshot local do grid (sem lock)
                local_snapshot = self._take_grid_snapshot()

                # 2. Decidir ação baseada no snapshot
                action = self._decide_action(local_snapshot, robot_data)

                # 3-5. Executar ação com locks apropriados
                self._execute_action(action, robot_data)

                # Aguardar baseado na velocidade
                sleep_time = robot_data['velocidade'] * 0.2  # 200ms por unidade de velocidade
                time.sleep(sleep_time)

            except Exception as e:
                self.logger.error(f"Erro em sense_act: {e}")
                time.sleep(0.5)

    def housekeeping(self):
        """
        Thread housekeeping - Manutenção conforme especificação:
        - Reduz energia de tempos em tempos
        - Grava log
        - Checa condição de vitória (robôs vivos == 1)
        """
        while self.running and not self.game_state.get_flag('game_over'):
            try:
                time.sleep(2)  # Executa a cada 2 segundos

                robot_data = self.game_state.get_robot_data(self.robo_id)
                if not robot_data or robot_data['status'] == 0:
                    break

                # Reduzir energia (metabolismo)
                new_energy = max(0, robot_data['energia'] - 1)
                self.game_state.set_robot_data(self.robo_id, energia=new_energy)

                # Log da situação atual
                self.logger.info(f"Energia: {new_energy}, Posição: ({robot_data['pos_x']}, {robot_data['pos_y']})")

                # Verificar morte por falta de energia
                if new_energy <= 0:
                    self._die("falta de energia")
                    break

                # Verificar condição de vitória
                alive_count = self._count_alive_robots()
                if alive_count <= 1:
                    self.game_state.set_flag('game_over', 1)
                    if alive_count == 1 and robot_data['status'] == 1:
                        self.game_state.set_flag('winner_id', self.robo_id)
                        self.logger.info("VITÓRIA! Sou o último robô vivo!")

            except Exception as e:
                self.logger.error(f"Erro em housekeeping: {e}")

    def _take_grid_snapshot(self):
        """Tira snapshot local do grid sem usar locks"""
        snapshot = {}
        robot_data = self.game_state.get_robot_data(self.robo_id)

        if not robot_data:
            return snapshot

        x, y = robot_data['pos_x'], robot_data['pos_y']

        # Examinar células adjacentes
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # W, E, N, S
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 40 and 0 <= ny < 20:
                cell = self.game_state.get_grid_cell(nx, ny)
                snapshot[(nx, ny)] = cell

        return snapshot

    def _decide_action(self, snapshot, robot_data):
        """Decide a próxima ação baseada no snapshot"""
        x, y = robot_data['pos_x'], robot_data['pos_y']

        # Verificar robôs adjacentes para duelo
        for (nx, ny), cell in snapshot.items():
            if cell.isdigit() and int(cell) != self.robo_id:
                return {'type': 'duel', 'target': int(cell), 'pos': (nx, ny)}

        # Procurar baterias próximas
        for (nx, ny), cell in snapshot.items():
            if cell == '⚡':
                return {'type': 'move', 'target': (nx, ny)}

        # Movimento aleatório
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        dx, dy = random.choice(directions)
        target = (x + dx, y + dy)

        if target in snapshot and snapshot[target] == ' ':
            return {'type': 'move', 'target': target}

        return {'type': 'wait'}

    def _execute_action(self, action, robot_data):
        """Executa a ação com locks apropriados"""
        if action['type'] == 'wait':
            return

        try:
            if action['type'] == 'move':
                self._execute_move(action['target'], robot_data)
            elif action['type'] == 'duel':
                self._execute_duel(action['target'], action['pos'], robot_data)

        except Exception as e:
            self.logger.error(f"Erro ao executar ação {action['type']}: {e}")

    def _execute_move(self, target, robot_data):
        """Executa movimento com locks adequados"""
        # Ordem de locks: grid -> robots
        acquired_locks = self.lock_manager.acquire_multiple(['grid', 'robots'])

        try:
            x, y = robot_data['pos_x'], robot_data['pos_y']
            tx, ty = target

            # Verificar se o destino ainda está livre
            cell = self.game_state.get_grid_cell(tx, ty)

            if cell == ' ':
                # Movimento normal
                self.game_state.set_grid_cell(x, y, ' ')
                self.game_state.set_grid_cell(tx, ty, str(self.robo_id))
                self.game_state.set_robot_data(self.robo_id, pos_x=tx, pos_y=ty)

                # Consumir energia
                new_energy = max(0, robot_data['energia'] - 1)
                self.game_state.set_robot_data(self.robo_id, energia=new_energy)

            elif cell == '⚡':
                # Coletar bateria
                self.game_state.set_grid_cell(x, y, ' ')
                self.game_state.set_grid_cell(tx, ty, str(self.robo_id))
                self.game_state.set_robot_data(self.robo_id, pos_x=tx, pos_y=ty)

                # Restaurar energia
                new_energy = min(100, robot_data['energia'] + 20)
                self.game_state.set_robot_data(self.robo_id, energia=new_energy)

                self.logger.info(f"Bateria coletada! Energia: {new_energy}")

        finally:
            self.lock_manager.release_multiple(acquired_locks)

    def _execute_duel(self, enemy_id, enemy_pos, robot_data):
        """Executa duelo com locks adequados"""
        # Ordem de locks: grid -> robots
        acquired_locks = self.lock_manager.acquire_multiple(['grid', 'robots'])

        try:
            enemy_data = self.game_state.get_robot_data(enemy_id)
            if not enemy_data or enemy_data['status'] == 0:
                return  # Inimigo já morto

            my_force = robot_data['forca']
            enemy_force = enemy_data['forca']

            self.logger.info(f"DUELO! Robô {self.robo_id} (F:{my_force}) vs Robô {enemy_id} (F:{enemy_force})")

            if my_force > enemy_force:
                # Eu venci
                self._kill_robot(enemy_id, enemy_pos)
                self.logger.info(f"VITÓRIA no duelo contra Robô {enemy_id}!")

            elif enemy_force > my_force:
                # Eu perdi
                self._die("derrotado em duelo")

            else:
                # Empate - ambos morrem
                self._kill_robot(enemy_id, enemy_pos)
                self._die("empate em duelo")
                self.logger.info(f"EMPATE no duelo contra Robô {enemy_id} - ambos mortos!")

        finally:
            self.lock_manager.release_multiple(acquired_locks)

    def _kill_robot(self, robo_id, pos):
        """Mata um robô e libera sua célula"""
        self.game_state.set_robot_data(robo_id, status=0)
        self.game_state.set_grid_cell(pos[0], pos[1], ' ')

    def _die(self, reason):
        """Marca este robô como morto"""
        robot_data = self.game_state.get_robot_data(self.robo_id)
        if robot_data:
            self.game_state.set_robot_data(self.robo_id, status=0)
            self.game_state.set_grid_cell(robot_data['pos_x'], robot_data['pos_y'], ' ')

        self.logger.info(f"MORTE por {reason}")
        self.running = False

    def _count_alive_robots(self):
        """Conta quantos robôs ainda estão vivos"""
        count = 0
        for i in range(4):
            robot_data = self.game_state.get_robot_data(i)
            if robot_data and robot_data['status'] == 1:
                count += 1
        return count

    def stop(self):
        """Para o robô"""
        self.running = False
        self.logger.info("Robô parado")
