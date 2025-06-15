import multiprocessing as mp
from multiprocessing import shared_memory
import struct
import os

class GameState:
    """Classe para gerenciar o estado compartilhado do jogo"""

    def __init__(self, name="batalha_robos", create=False):
        self.name = name
        self.grid_size = 40 * 20  # 800 bytes para o grid
        self.robot_count = 4
        self.robot_data_size = 28  # ID, força, energia, velocidade, posição x,y, status, padding
        self.battery_count = 10
        self.battery_data_size = 12  # posição x,y, ativa/inativa
        self.flags_size = 20  # init_done, game_over, winner_id, etc.

        self.total_size = (
            self.grid_size +
            (self.robot_count * self.robot_data_size) +
            (self.battery_count * self.battery_data_size) +
            self.flags_size
        )

        try:
            if create:
                # Tenta criar nova memória compartilhada
                try:
                    # Limpa memória existente se houver
                    existing = shared_memory.SharedMemory(name=name)
                    existing.close()
                    existing.unlink()
                except FileNotFoundError:
                    pass

                self.shm = shared_memory.SharedMemory(
                    name=name,
                    create=True,
                    size=self.total_size
                )
                self._initialize_memory()
            else:
                # Conecta à memória existente
                self.shm = shared_memory.SharedMemory(name=name)

        except Exception as e:
            print(f"Erro ao criar/acessar memória compartilhada: {e}")
            raise

    def _initialize_memory(self):
        """Inicializa a memória compartilhada com valores padrão"""
        # Inicializa grid com espaços vazios
        for i in range(self.grid_size):
            self.shm.buf[i] = ord(' ')

        # Inicializa dados dos robôs
        robot_offset = self.grid_size
        for i in range(self.robot_count):
            offset = robot_offset + (i * self.robot_data_size)
            # ID do robô
            struct.pack_into('i', self.shm.buf, offset, i)
            # Força (1-10)
            struct.pack_into('i', self.shm.buf, offset + 4, 5)
            # Energia (10-100)
            struct.pack_into('i', self.shm.buf, offset + 8, 50)
            # Velocidade (1-5)
            struct.pack_into('i', self.shm.buf, offset + 12, 3)
            # Posição X
            struct.pack_into('i', self.shm.buf, offset + 16, -1)
            # Posição Y
            struct.pack_into('i', self.shm.buf, offset + 20, -1)
            # Status (0=morto, 1=vivo)
            struct.pack_into('i', self.shm.buf, offset + 24, 1)

        # Inicializa flags
        flags_offset = self.grid_size + (self.robot_count * self.robot_data_size) + (self.battery_count * self.battery_data_size)
        struct.pack_into('i', self.shm.buf, flags_offset, 0)  # init_done
        struct.pack_into('i', self.shm.buf, flags_offset + 4, 0)  # game_over
        struct.pack_into('i', self.shm.buf, flags_offset + 8, -1)  # winner_id

    def get_grid_cell(self, x, y):
        """Obtém o valor de uma célula do grid"""
        if 0 <= x < 40 and 0 <= y < 20:
            index = y * 40 + x
            return chr(self.shm.buf[index])
        return None

    def set_grid_cell(self, x, y, value):
        """Define o valor de uma célula do grid"""
        if 0 <= x < 40 and 0 <= y < 20:
            index = y * 40 + x
            self.shm.buf[index] = ord(str(value))

    def get_robot_data(self, robot_id):
        """Obtém os dados de um robô"""
        if 0 <= robot_id < self.robot_count:
            offset = self.grid_size + (robot_id * self.robot_data_size)
            return {
                'id': struct.unpack_from('i', self.shm.buf, offset)[0],
                'forca': struct.unpack_from('i', self.shm.buf, offset + 4)[0],
                'energia': struct.unpack_from('i', self.shm.buf, offset + 8)[0],
                'velocidade': struct.unpack_from('i', self.shm.buf, offset + 12)[0],
                'pos_x': struct.unpack_from('i', self.shm.buf, offset + 16)[0],
                'pos_y': struct.unpack_from('i', self.shm.buf, offset + 20)[0],
                'status': struct.unpack_from('i', self.shm.buf, offset + 24)[0]
            }
        return None

    def set_robot_data(self, robot_id, **kwargs):
        """Atualiza os dados de um robô"""
        if 0 <= robot_id < self.robot_count:
            offset = self.grid_size + (robot_id * self.robot_data_size)

            if 'forca' in kwargs:
                struct.pack_into('i', self.shm.buf, offset + 4, kwargs['forca'])
            if 'energia' in kwargs:
                struct.pack_into('i', self.shm.buf, offset + 8, kwargs['energia'])
            if 'velocidade' in kwargs:
                struct.pack_into('i', self.shm.buf, offset + 12, kwargs['velocidade'])
            if 'pos_x' in kwargs:
                struct.pack_into('i', self.shm.buf, offset + 16, kwargs['pos_x'])
            if 'pos_y' in kwargs:
                struct.pack_into('i', self.shm.buf, offset + 20, kwargs['pos_y'])
            if 'status' in kwargs:
                struct.pack_into('i', self.shm.buf, offset + 24, kwargs['status'])

    def get_flag(self, flag_name):
        """Obtém uma flag do sistema"""
        flags_offset = self.grid_size + (self.robot_count * self.robot_data_size) + (self.battery_count * self.battery_data_size)

        if not self.shm or not self.shm.buf:
            return 0

        try:
            if flag_name == 'init_done':
                return struct.unpack_from('i', self.shm.buf, flags_offset)[0]
            elif flag_name == 'game_over':
                return struct.unpack_from('i', self.shm.buf, flags_offset + 4)[0]
            elif flag_name == 'winner_id':
                return struct.unpack_from('i', self.shm.buf, flags_offset + 8)[0]
            else:
                return 0
        except (struct.error, IndexError):
            return 0

    def set_flag(self, flag_name, value):
        """Define uma flag do sistema"""
        flags_offset = self.grid_size + (self.robot_count * self.robot_data_size) + (self.battery_count * self.battery_data_size)

        if not self.shm or not self.shm.buf:
            return

        try:
            if flag_name == 'init_done':
                struct.pack_into('i', self.shm.buf, flags_offset, value)
            elif flag_name == 'game_over':
                struct.pack_into('i', self.shm.buf, flags_offset + 4, value)
            elif flag_name == 'winner_id':
                struct.pack_into('i', self.shm.buf, flags_offset + 8, value)
        except (struct.error, IndexError):
            pass

    def cleanup(self):
        """Limpa a memória compartilhada"""
        try:
            if hasattr(self, 'shm') and self.shm:
                self.shm.close()
                self.shm.unlink()
        except:
            pass
