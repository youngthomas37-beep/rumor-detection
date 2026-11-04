# 中文谣言检测（Chinese Rumor Detection）

一个基于 **BERT** 的中文谣言/假新闻**辅助检测**工具。模型在浏览器本地运行，输入文字不会上传服务器。

> ⚠️ 本工具基于「文本风格」做疑似谣言初筛，**不会查证事实**，结果仅供参考，非权威判定。

## ✨ 功能

- **网页版（PWA）**：粘贴一段文字，快速判断是否疑似谣言；手机可「添加到主屏幕」当 App 用。
- **浏览器插件**：网页选中文字 → 右键「检测是否谣言」，或点插件图标粘贴检测。
- **训练代码**：附带完整微调脚本，可换数据重新训练。

## 🚀 快速使用

- **在线体验**：https://youngthomas37-beep.github.io/rumor.html
- **模型**：https://huggingface.co/ThomasYoung101/bert-rumor-onnx （ONNX int8，约 103MB，浏览器自动下载）

## 📁 目录结构

```
web/       网页版 PWA（rumor.html + manifest + sw + icon）
extension/ 浏览器插件（Chrome/Edge，manifest + background + popup）
train/     训练代码（train_rumor.py）
```

## 🧠 模型与数据

- 模型：`bert-base-chinese`（约 1.1 亿参数）微调，导出为 ONNX 并 int8 量化。
- 数据：清华 [Chinese_Rumor_Dataset](https://github.com/thunlp/Chinese_Rumor_Dataset)（微博谣言数据集），共 4340 条（2500 谣言 + 1840 非谣言）。
- 验证集准确率：约 96%。

## 🔧 安装浏览器插件

1. 打开 `chrome://extensions`
2. 开启「开发者模式」
3. 点「加载已解压的扩展程序」→ 选择本仓库的 `extension/` 目录
4. 之后在网页选中文字 → 右键 →「检测是否谣言」

## 🔧 训练自己的版本

```bash
cd train
python train_rumor.py --data 你的数据.csv --epochs 3
```

数据格式：TSV，两列 `text`（文本）和 `label`（0=非谣言，1=谣言）。依赖：`transformers`、`torch`、`datasets`。

## 📄 说明

- 数据集来源：[thunlp/Chinese_Rumor_Dataset](https://github.com/thunlp/Chinese_Rumor_Dataset)（请遵循其许可）。
- 本仓库代码可自由使用；模型仅供学习参考，勿用于需要事实核查的场景。
