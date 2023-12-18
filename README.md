# Fine-Tuning Latest LLM for Video Response Prediction
![image](https://github.com/krjeo/UOS_2023_NLP/assets/138076274/94c484ca-5ba1-4d7d-b6be-5465a327f1f6)


## Contributors
**Jiwhan Lee, Jeonghyun Kim, Jiyoung Seo**<br/>
If there occurs any copyright issues on our dataset, we'll delete it immediately so please let us know. <br/>
Thank you.
<br/><br/>

## Task
![image](https://github.com/krjeo/UOS_2023_NLP/assets/138076274/1b3ed629-5b62-4709-9890-121a2063fedc) <br> 
Our task is to generate a YouTube comment based on the video content by extracting its subtitles and processing them through a fine-tuned Large Language Model (LLM).<br/><br/><br/>


## Model
We use the latest open-source LLM, LLaMA 2 by Meta.
There exists 3 versions of LLaMA 2 depeding on their size; 7B, 13B, and 70B and we employ 7B model for learning efficiency and embedded systems. <br/><br/>
<img src="https://github.com/krjeo/UOS_2023_NLP/assets/138076274/c0f56673-2ee5-4c6a-a737-d7a6cd6d2eb3" align="center" width="300"/> <br/><br/>


### Fine-Tuning
For fine-tuning we exploit the Parameter Efficient Fine Tuning (PEFT) method.
There are two ways to implement the PEFT methods. 
- First, unfreeze some parts of the classifier in the latter half of the frozen model and training it to suit the task.
- Second is adding small Linear Layers to the bottom of the frozen model and training it. 
Since we are dealing with text-to-text problem, we adopt the original schema of LLaMA2 therefore proceed with using the first fine-tuning method. <br/><br/><br/>

## Results
We generated comments of 8 videos from different categories in 5 different ways to compare:
- 1. Beam Search with Base LLaMA2 
- 2. Greedy Search with 1-Epoch Fine-Tuned Model 
- 3. Greedy Search with 3-Epoch Fine-Tuned Model 
- 4. Beam Search with Temperture with 2-Epoch Fine-Tuned Model 
- 5. Beam Search with Do-Sample with 2-Epoch Fine Tuned Model
<br/><br/>

<img src="https://github.com/krjeo/UOS_2023_NLP/assets/138076274/7691fb3f-6928-406a-ba2a-df315a4a7062" width="700"/>
<img src="https://github.com/krjeo/UOS_2023_NLP/assets/138076274/afa723a4-97e3-4558-a30a-08b5aa6c0b2d" " width="700"/> 
<br/><br/>

<img src="https://github.com/krjeo/UOS_2023_NLP/assets/138076274/a964dd45-ae47-4d62-8b37-8ba8c0b8efad"  width="700"/>
<img src="https://github.com/krjeo/UOS_2023_NLP/assets/138076274/41615be7-2879-4e41-a2d4-6550848200e3"  width="700"/>

<br/><br/>
<img src="https://github.com/krjeo/UOS_2023_NLP/assets/138076274/a968c3a6-e008-451d-8370-90667d2c92a3" width="700"/>
<img src="https://github.com/krjeo/UOS_2023_NLP/assets/138076274/6a9d814f-48e0-43bb-af52-79ce7721d37f" width="700"/> 

<br/><br/>
<img src="https://github.com/krjeo/UOS_2023_NLP/assets/138076274/d1303783-7fd5-4464-8fef-18d5ea532280" width="700"/>
<img src="https://github.com/krjeo/UOS_2023_NLP/assets/138076274/9ce658d5-eaab-4d7e-a6b8-f0b6980ef0e9"  width="700"/>
<br/><br/>


## Conclusion
- To summarize the contribution of our project : <br/>
(1) We created a dataset of 2400 video subtitle-comment pairs from YouTube videos. <br/>
(2) We fine-tuned the latest open-source LLM, LLaMA 2, with our new dataset to successfully predict and generate meaningful comments.<br/><br/>

- To enhance the model's performance, the following improvements can be made : <br/>
(1) Increase the number of comment samples per video for dataset that reduces bias and help the model to generate varied comments in real-word scenarios.<br/>
(2) Add visual information such as thumbnail images and video scenes for multi-modal learning could lead to better performance and more realistic comment generation.<br/><br/><br/>


## References
- Hugo Touvron, Thibaut Lavril, Gautier Izacard, Edouard Grave ,Guillaume Lample, et al. LLaMA: Open and Efficient Foundation Language Models. arXiv:2302.13971, 2023.
- Haokun Liu, Derek Tam, Mohammed Muqeeth, et al. Few-Shot Parameter-Efficient Fine-Tuning is Better and Cheaper than In-Context Learning. arXiv:2205.05638, 2022. 
- Yanli Zhao, Andrew Gu, Rohan Varma, et al. PyTorch FSDP: Experiences on Scaling Fully Sharded Data Parallel. arXiv:2304.11277, 2023.
<br/><br/><br/>

## Implementation
- datasets
- results
- Youtube_crawling.jpynb
- Youtube_crawling.py
- fine_tuning.py
- finetuned_beam.py
- finetuned_dosample.py
- finetuned_greedy.py
- manual_test.py
- original_greedy.py
  









