import threading
import random
from typing import List


class PopulaLista(threading.Thread):
    
    def __init__(self, lista: List[int], tamanho: int, min_val: int, max_val: int):
        super().__init__()
        self.lista = lista
        self.tamanho = tamanho
        self.min_val = min_val
        self.max_val = max_val
    
    def run(self):
        thread_name = threading.current_thread().name
        print(f"Thread {thread_name} iniciada para popular a lista com tamanho: {self.tamanho}")
        
        for i in range(self.tamanho): #adiciona numeros aleatorios entre min e max
            self.lista.append(random.randint(self.min_val, self.max_val))
        
        print(f"Thread finalizada {thread_name}")


class CalculaMedia(threading.Thread):
    
    def __init__(self, lista: List[int]):
        super().__init__()
        self.lista = lista
        self.media = 0.0
    
    def run(self):
        thread_name = threading.current_thread().name
        print(f"Thread {thread_name} iniciada para calcular a media da lista com tamanho: {len(self.lista)}")
        
        if not self.lista: # se  a lista estiver vazia
            self.media = 0.0
            print(f"Thread finalizada {thread_name} - Media: 0.0")
            return
        
        # calcula media dos numeros na lista
        soma = sum(self.lista)  # soma todos os nnmeros da lista
        self.media = soma / len(self.lista)  # faz a media
        print(f"Thread de Media finalizada {thread_name} - Media: {self.media}")
    
    def get_media(self):  # !!get para pegar!! a media calculada e fazer o calculo final
        return self.media


def main():
    n = 100000  # total de numeros a serem gerados
    m = 10      # numero de listas
    
    listas_de_listas = []
    populadores = []  # lista para armazenar os threads que vai popular as listas
    
    tamanho_por_lista = n // m  # tamanho de cada lista
    min_val = 1000
    max_val = 100000
    
    # distribui os numeros e cria as threads de populacap
    for i in range(m):
        lista = []
        listas_de_listas.append(lista)  # adiciona a nova lista na lista de listas
        
        popula_lista = PopulaLista(lista, tamanho_por_lista, min_val, max_val)  # cria a tarefa de popular a lista
        populadores.append(popula_lista)  # adiciona a thread na lista de threads
        
        popula_lista.start()
    
    #e!!spera todas as threads de população terminarem!!
    for thread in populadores:
        thread.join()
    
    print("\nTodas as listas foram populadas. Iniciando calculo das medias...")
    
    calculadores = []  # nova lista com as threads que vao calcular as medias
    tarefas_listas = []  # lista para armazenar as tarefas de calculo de media
    
    # cria e inicia as threads para calcular a media de cada lista
    for i in range(m):
        tarefa = CalculaMedia(listas_de_listas[i])  # !!cria a tarefa de calcular a media da lista!!
        tarefa.name = f"CalculaMedia-{i + 1}"  #define o nome da thread
        tarefas_listas.append(tarefa)
        calculadores.append(tarefa)  
        tarefa.start()
    
    # !!Espera todas as threads de calculo terminarem!!
    for thread in calculadores:
        thread.join()
    
    # Calcula a media geral
    soma_das_medias = sum(tarefa.get_media() for tarefa in tarefas_listas)
    media_geral = soma_das_medias / m
    print(f"\nCalculo finalizado. A media geral das {m} listas eh: {media_geral}")


if __name__ == "__main__":
    main()

