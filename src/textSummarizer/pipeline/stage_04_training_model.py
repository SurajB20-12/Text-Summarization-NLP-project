from textSummarizer.config.configuration import ConfigurationManager
from textSummarizer.components.training_model import ModelTrainer
from textSummarizer.logging import logger

class ModelTrainerTrainingPipeline:
  def __init__(self):
    pass

  def main(self):
    config=ConfigurationManager()
    model_trainer_config=config.get_model_trainer_config()
    model_trainer_config=ModelTrainer(config=model_trainer_config)
    model_trainer_config.train_the_model()