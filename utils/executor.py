from concurrent.futures import ProcessPoolExecutor
from multiprocessing import Manager

class Executor:
    def __init__(self, max_workers=None):
        self._futures = {}
        self._statuses = {}
        self._manager = Manager()
        self._pool = ProcessPoolExecutor(max_workers=max_workers)
    
    def submit(self, name, fn, *args, **kwargs):
        if name in self._futures:
            return self._futures[name]
        else:
            status = self._manager.dict()
            future = self._pool.submit(fn, *args, status=status, **kwargs)
            self._futures[name] = future
            self._statuses[name] = status
            return future
    
    def result(self, name, value=None):
        if name not in self._futures:
            raise KeyError("No such task!")
        
        future = self._futures[name]
        if future.done():
            del self._future[name]
            return future.result()
        
        return value
    
    def clear(self, name):
        if name not in self._futures:
            raise KeyError("No such task!")
        
        future = self._futures[name]
        cancelled = future.cancel()
        del self._futures[name]
        
        return cancelled
        
    def exists(name):
        return name in self._futures
        
    def future(self, name, value=None):
        return self._futures.get(name, value)
    
    def job_status(self, name, value=None):
        return self._statuses.get(name, value)

    @property
    def status(self):
        return {
            name: {
                "done": future.done(),
                "status": self._statuses[name].copy()
            }
            for name, future in self._futures.items()
        }
    
