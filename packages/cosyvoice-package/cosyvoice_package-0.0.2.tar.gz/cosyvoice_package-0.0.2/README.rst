!!!!! Warning: Provided unofficially and for author use only !!!!!   

conda install -y -c conda-forge pynini==2.1.5
conda install pytorch torchvision torchaudio pytorch-cuda=12.4 -c pytorch -c nvidia

mkdir pretrained_models
git clone https://www.modelscope.cn/iic/CosyVoice-300M.git pretrained_models/CosyVoice-300M
git clone https://www.modelscope.cn/iic/CosyVoice-300M-SFT.git pretrained_models/CosyVoice-300M-SFT