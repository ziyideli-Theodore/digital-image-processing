# AgenticFlow: Multi-Agent Cartoonization System

基于多智能体协作网络的可控人物卡通化生成系统

## 项目简介

AgenticFlow 是一个基于 LangGraph 的多智能体协作系统，用于实现可控的人物图像卡通化。系统通过多个专业化的 Agent 协作完成图像分析、风格生成和质量评估的完整流程。

## 系统架构

本系统采用多智能体协作架构，包含以下核心 Agent：

- **Project Manager**: 项目管理者，负责协调整体流程
- **Image Analyzer**: 图像分析师，负责分析输入图像的特征
- **Art Director**: 艺术总监，负责生成卡通化图像
- **QA Critic**: 质量评审员，负责评估生成结果并提供反馈

## 技术栈

- **LangGraph**: 多智能体协作框架
- **LangChain**: LLM 应用开发框架
- **Diffusers**: Stable Diffusion 模型库
- **ControlNet**: 姿态控制模型
- **IP-Adapter**: 风格迁移模型
- **Ollama**: 本地 LLM 推理

## 安装

```bash
# 克隆仓库
git clone https://github.com/Theodore-PKU/digital-image-processing.git
cd digital-image-processing

# 安装依赖
pip install -r requirements.txt
```

## 模型下载

由于模型文件过大，未包含在仓库中。请从以下链接下载所需模型：

- **ControlNet OpenPose**: [lllyasviel/control_v11p_sd15_openpose](https://huggingface.co/lllyasviel/control_v11p_sd15_openpose)
- **Classic Animation Diffusion**: [ItsJayQz/Classic_Anim_Diffusion](https://huggingface.co/ItsJayQz/Classic_Anim_Diffusion)
- **IP-Adapter**: [h94/IP-Adapter](https://huggingface.co/h94/IP-Adapter)

下载后将模型文件放置在 `models/` 目录下对应的子目录中。

## 使用方法

```python
python main.py
```

## 项目结构

```
.
├── agents/                 # Agent 模块
│   ├── project_manager.py  # 项目管理者
│   ├── image_analyzer.py   # 图像分析师
│   ├── art_director.py     # 艺术总监
│   └── qa_critic.py        # 质量评审员
├── models/                 # 模型文件目录
│   ├── ControlNet/
│   ├── control_v11p_sd15_openpose/
│   ├── classic-anim-diffusion/
│   └── IP-Adapter/
├── main.py                 # 主程序入口
├── requirements.txt        # 依赖列表
└── README.md              # 项目说明

```

## 工作流程

1. **图像分析**: Image Analyzer 分析输入图像的姿态、风格特征
2. **卡通化生成**: Art Director 基于分析结果生成卡通化图像
3. **质量评估**: QA Critic 评估生成质量并提供反馈
4. **迭代优化**: 根据反馈决定是否重新生成

## 相关论文

本项目是数字图像处理课程的期末项目，相关技术细节请参考：
- AgenticFlow 中文终期汇报.pdf
- 数字图像处理中期汇报.pdf

## 作者

Theodore (李梓屹得) - 中国传媒大学

## 致谢

感谢 Gemini 在项目开发过程中提供的技术支持。

## License

MIT License
