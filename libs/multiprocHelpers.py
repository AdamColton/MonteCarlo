import multiprocessing

def calculateCores(cores):
  if cores > 0 :
    return cores
  if cores == 0 :
    return multiprocessing.cpu_count()
  if cores < 0 :
    cores += multiprocessing.cpu_count()
    if cores < 0 : cores = 1
    return cores