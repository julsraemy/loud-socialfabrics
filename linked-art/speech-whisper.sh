for f in *.wav ; do whisper $f --model small --fp16 False ; done