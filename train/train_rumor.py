"""中文谣言/假新闻检测模型微调（bert-base-chinese + 清华微博谣言数据集）。"""
import argparse

import numpy as np
import torch
from datasets import Dataset
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    DataCollatorWithPadding,
    Trainer,
    TrainingArguments,
)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="google-bert/bert-base-chinese")
    ap.add_argument("--data", default=r"F:/Users/yangge/Documents/dive-into-llms/chinese-rumor/rumor_data.csv")
    ap.add_argument("--epochs", type=int, default=3)
    ap.add_argument("--batch-size", type=int, default=16)
    ap.add_argument("--lr", type=float, default=2e-5)
    ap.add_argument("--max-length", type=int, default=128)
    ap.add_argument("--output-dir", default="finetuned-bert-rumor")
    args = ap.parse_args()

    print("CUDA:", torch.cuda.is_available())
    if torch.cuda.is_available():
        print("GPU:", torch.cuda.get_device_name(0))

    tokenizer = AutoTokenizer.from_pretrained(args.model)
    model = AutoModelForSequenceClassification.from_pretrained(args.model, num_labels=2)
    model.config.id2label = {0: "非谣言", 1: "谣言"}
    model.config.label2id = {"非谣言": 0, "谣言": 1}

    texts, labels = [], []
    with open(args.data, encoding="utf-8-sig") as f:
        next(f)  # 跳过表头
        for line in f:
            line = line.rstrip("\n")
            if not line:
                continue
            parts = line.split("\t")
            if len(parts) == 2:
                texts.append(parts[0])
                labels.append(int(parts[1]))

    ds = Dataset.from_dict({"text": texts, "label": labels}).shuffle(seed=42)
    split = ds.train_test_split(test_size=0.2, seed=42)
    train_ds, eval_ds = split["train"], split["test"]

    def tokenize(examples):
        return tokenizer(examples["text"], truncation=True, max_length=args.max_length)

    train_ds = train_ds.map(tokenize, batched=True, remove_columns=["text"])
    eval_ds = eval_ds.map(tokenize, batched=True, remove_columns=["text"])
    train_ds = train_ds.rename_column("label", "labels")
    eval_ds = eval_ds.rename_column("label", "labels")
    train_ds.set_format("torch")
    eval_ds.set_format("torch")
    print("train=%d eval=%d" % (len(train_ds), len(eval_ds)))

    def compute_metrics(p):
        preds = np.argmax(p.predictions, axis=-1)
        return {"accuracy": float((preds == p.label_ids).mean())}

    training_args = TrainingArguments(
        output_dir=args.output_dir,
        eval_strategy="epoch",
        save_strategy="epoch",
        learning_rate=args.lr,
        per_device_train_batch_size=args.batch_size,
        per_device_eval_batch_size=args.batch_size,
        num_train_epochs=args.epochs,
        weight_decay=0.01,
        load_best_model_at_end=True,
        metric_for_best_model="accuracy",
        logging_steps=20,
        fp16=True,
        report_to="none",
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_ds,
        eval_dataset=eval_ds,
        data_collator=DataCollatorWithPadding(tokenizer),
        compute_metrics=compute_metrics,
    )

    trainer.train()
    metrics = trainer.evaluate()
    print("EVAL:", metrics)
    trainer.save_model(args.output_dir)
    tokenizer.save_pretrained(args.output_dir)
    print("saved ->", args.output_dir)


if __name__ == "__main__":
    main()
