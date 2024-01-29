import signal
import time
import sys
from kafka_lib import ProducerThread, ConsumerThread
from log_analyser.log_analyser import LogAnalyser
import configparser
import os


class DatastrikePythonProcessing:
    def __init__(self):

        self.running = True

        self.config = configparser.ConfigParser()
        self.config.read("datastrike_python_processing.cfg")


        self.kafka_url = self.config["kafka"]["url"]

        print(self.kafka_url)
        self.producer_thread = ProducerThread(self.kafka_url)
        
        self.consumer_thread = ConsumerThread(self.kafka_url)
        self.consumer_thread.add_topics("analyse", self.on_callback_test)
        
        self.consumer_thread.start()
        self.producer_thread.start()
        
        
    def on_callback_test(self, topic, data):
        print("message receive : ", topic, data)

        filePath = data["filePath"]
        fileName = data["fileName"]
        teamId = data["teamId"]

        if self.check_txt_extension(fileName):

            try:
                la = LogAnalyser(filePath, fileName, teamId)
                la.run()
                if la.map != None:
                    self.producer_thread.send("analyse.report", la.map.export_json())
                else:
                    self.producer_thread.send("analyse.report", {"error": "File txt not correct"})
            except Exception as e:
                self.producer_thread.send("analyse.report", {"error": "{}".format(e)})
        else:
            self.producer_thread.send("analyse.report", {"error": "File extension not correct"})
        try:
            os.remove("{}/{}".format(filePath, fileName))
        except Exception as e:
            print("Error remove file : {}".format(e))

    def check_txt_extension(self, filename):
        return filename.lower().endswith('.txt')
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