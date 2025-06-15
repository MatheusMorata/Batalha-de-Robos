
import multiprocessing as mp

class LockManager:
    """Gerenciador de locks para prevenir deadlocks"""

    def __init__(self):
        self.grid_mutex = mp.Lock()
        self.robots_mutex = mp.Lock()
        self.battery_mutexes = [mp.Lock() for _ in range(10)]  # 10 baterias
        self.init_mutex = mp.Lock()

        # Ordem hierárquica de locks para prevenir deadlocks
        self.lock_hierarchy = {
            'init': 0,
            'grid': 1,
            'robots': 2,
            'battery': 3
        }

    def acquire_multiple(self, lock_types, timeout=5.0):
        """Adquire múltiplos locks seguindo a hierarquia"""
        # Ordena os locks pela hierarquia
        sorted_locks = sorted(lock_types, key=lambda x: self.lock_hierarchy.get(x.split('_')[0], 99))
        acquired_locks = []

        try:
            for lock_type in sorted_locks:
                if lock_type == 'grid':
                    if self.grid_mutex.acquire(timeout=timeout):
                        acquired_locks.append(('grid', self.grid_mutex))
                    else:
                        raise TimeoutError(f"Timeout ao adquirir {lock_type}")

                elif lock_type == 'robots':
                    if self.robots_mutex.acquire(timeout=timeout):
                        acquired_locks.append(('robots', self.robots_mutex))
                    else:
                        raise TimeoutError(f"Timeout ao adquirir {lock_type}")

                elif lock_type.startswith('battery_'):
                    battery_id = int(lock_type.split('_')[1])
                    if self.battery_mutexes[battery_id].acquire(timeout=timeout):
                        acquired_locks.append((lock_type, self.battery_mutexes[battery_id]))
                    else:
                        raise TimeoutError(f"Timeout ao adquirir {lock_type}")

            return acquired_locks

        except Exception as e:
            # Libera todos os locks já adquiridos em caso de erro
            for lock_name, lock_obj in reversed(acquired_locks):
                try:
                    lock_obj.release()
                except:
                    pass
            raise e

    def release_multiple(self, acquired_locks):
        """Libera múltiplos locks na ordem inversa"""
        for lock_name, lock_obj in reversed(acquired_locks):
            try:
                lock_obj.release()
            except:
                pass
