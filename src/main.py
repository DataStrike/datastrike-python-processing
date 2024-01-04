import signal
import time
import sys
from kafka_lib import ProducerThread, ConsumerThread


class DatastrikePythonProcessing:
    def __init__(self):

        self.running = True
        
        
        self.producer_thread = ProducerThread("localhost:29093")
        
        self.consumer_thread = ConsumerThread("localhost:29093")
        self.consumer_thread.add_topics("test", self.on_callback_test)
        
        self.consumer_thread.start()
        self.producer_thread.start()
        
        
    def on_callback_test(self, topic, data):
        print("message receive : ", topic, data)
        print("a")

    def run(self):

        while self.running:
            print("Service en cours d'exécution...")
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