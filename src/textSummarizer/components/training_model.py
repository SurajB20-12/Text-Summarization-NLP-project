from transformers import TrainingArguments
from transformers import DataCollatorForSeq2Seq,AutoModelForSeq2SeqLM,AutoTokenizer
from datasets import load_dataset, load_from_disk
import torch
from transformers.trainer import Trainer
from textSummarizer.entity import ModelTrainerConfig
import os 
class ModelTrainer:
  def __init__(self,config:ModelTrainerConfig):
    self.config=config 

  def train_the_model(self):
    device= "cuda" if torch.cuda.is_available() else "cpu"
    tokenizer = AutoTokenizer.from_pretrained(self.config.model_ckpt)
    model_t5 = AutoModelForSeq2SeqLM.from_pretrained(self.config.model_ckpt).to(device)
    seq2seq_data_collator = DataCollatorForSeq2Seq(tokenizer, model=model_t5)

    #loading data 
    dataset_samsum_pt = load_from_disk(self.config.data_path)

    #use yaml file to load parameters or hardcode it in TrainingArg function 
    # trainer_args = TrainingArguments(
        #     output_dir=self.config.root_dir, num_train_epochs=self.config.num_train_epochs, warmup_steps=self.config.warmup_steps,
        #     per_device_train_batch_size=self.config.per_device_train_batch_size, per_device_eval_batch_size=self.config.per_device_train_batch_size,
        #     weight_decay=self.config.weight_decay, logging_steps=self.config.logging_steps,
        #     evaluation_strategy=self.config.evaluation_strategy, eval_steps=self.config.eval_steps, save_steps=1e6,
        #     gradient_accumulation_steps=self.config.gradient_accumulation_steps
        # )

    #hardcode it in this function
    trainer_args = TrainingArguments(
            output_dir=self.config.root_dir, num_train_epochs=1, warmup_steps=0,
            per_device_train_batch_size=4, per_device_eval_batch_size=4,
            weight_decay=0.01, logging_steps=50,
            evaluation_strategy='epoch', save_strategy='no',disable_tqdm=True,
            gradient_accumulation_steps=1,report_to=[],overwrite_output_dir=True
        ) 
    trainer=Trainer(model=model_t5,args=trainer_args,tokenizer=tokenizer,
                    data_collator=seq2seq_data_collator,
                    train_dataset=dataset_samsum_pt['train'].select(range(1000)),
                    eval_dataset=dataset_samsum_pt['validation'])
    
    trainer.train()

    ##save model
    model_t5.save_pretrained(os.path.join(self.config.root_dir,"t5-samsum-model"))

    ##save tokenizer
    tokenizer.save_pretrained(os.path.join(self.config.root_dir,"tokenizer"))




