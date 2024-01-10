import signal
import time
import sys
from kafka_lib import ProducerThread, ConsumerThread
from log_analyser.log_analyser import LogAnalyser


class DatastrikePythonProcessing:
    def __init__(self):

        self.running = True

        self.producer_thread = ProducerThread("localhost:29092")
        
        self.consumer_thread = ConsumerThread("localhost:29092")
        self.consumer_thread.add_topics("analyse", self.on_callback_test)
        
        self.consumer_thread.start()
        self.producer_thread.start()
        
        
    def on_callback_test(self, topic, data):
        print("message receive : ", topic, data)

        la = LogAnalyser('logs/Log-2023-12-22-21-12-32.txt', "Log-2023-12-22-21-12-32.txt")
        la.run()
        self.producer_thread.send("analyse.report", la.map.export_json())

    def run(self):

        while self.running:
            # print("Service en cours d'exécution...")
            time.sleep(1)

        print("Service stop.")
    
    def stop(self):
        
        self.consumer_thread.stop()
        self.producer_thread.stop()
        self.running = False
        
    
    def stop_service(self, signum, frame):

        print(f"Signal reçu : {signum}. Arrêt du service...")
        
        self.consumer_thread.stop()
        self.producer_thread.stop()
        self.running = False

def signal_handler(signum, frame):
    datastrike_python_processing.stop_service(signum, frame)

if __name__ == "__main__":
    
    datastrike_python_processing = DatastrikePythonProcessing()

    # Associer le signal SIGTERM à la fonction handler
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        # Démarrer le service
        datastrike_python_processing.run()
    except KeyboardInterrupt:
        print("Arrêt forcé du service...")
    finally:
        datastrike_python_processing.stop()
        sys.exit(0)