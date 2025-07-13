from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError
from django.conf import settings
import os
# from structure_gen.musicgen_api_extendservice import generate_melody_api
# from structure_gen.musicgen_api import generate_music_api

def create_music(
            creation_mode,
            model,
            style,
            description=None,
            audio_file_path=None,
            midi_file_path=None,
            sequential=False,
            duration=None,
            song_name=None
        ):
    created_music_file_name = song_name + '.wav'
    audio_model_id = 'facebook/musicgen-melody' if creation_mode == 'Melody' else 'facebook/musicgen-small'
    use_local_llm = True if model == 'local' else False
    sampling_mode = 'sequential' if sequential else 'random'
    
    style_name = None
    if style == 'ambient':
        style_name = 'ambient'
    if style == 'hip-hop':
        style_name = 'lofi hip hop'
    if style == 'classical':
        style_name = 'classical'
    
    params = {
        # 'audio_model_id': 'facebook/musicgen-melody',  # or 'facebook/musicgen-melody'
        'audio_model_id': audio_model_id,
        'api_endpoint': 'https://www.dmxapi.com/v1/chat/completions',
        'api_key': 'sk-vWyNj5NxixWjJcjknaxNivrtIkHIjXDBVlk1b6wRW2pZc0hz',
        'model': 'o3-mini-high',
        'use_local_llm': use_local_llm,
        # 'seed_path': './data/melody_seed_wave/6.wav',  // audio_file_path
        'seed_path': audio_file_path,
        'style': style_name,
        # description
        'user_prompt': description,
        'total_sec': int(duration),
        'window_sec': 30,
        'overlap_sec': 5,
        'prompt_sec': 5,
        # 'safety_tail': 3,
        'safety_tail': 2,
        'n_tracks': 1,
        'clap_candidates': 1,
        # 'clap_candidates': 1,
        'sim_thresh': 0.46,
        'sil_thresh': -40,
        'use_fp16': True,
        # 'out_path': './result/final.wav',
        'out_path': os.path.join(settings.MEDIA_ROOT,created_music_file_name),
        'checkpoint_path': '/root/autodl-tmp/structure_gen/models/best_epoch100.pt',
        # 用户上传的midi文件的路径
        'prompt_pool_dir': '/root/autodl-tmp/structure_gen/data/melody_prompt_pool',
        'fade_out': 5.0,
        'finetuned_lm_path': '/root/autodl-tmp/structure_gen/models/ckpt_epoch24.089.pt',
        'strict_load': False,
        # 加选项框，逻辑推断模式，随机
        # 'sampling_mode': 'sequential',  # 可选 "random" 或 "sequential"
        'sampling_mode': sampling_mode
    }

    # 调用structure_gen 下的音乐生成模型API
    # if 'melody' in params['audio_model_id']:
    #     result = generate_melody_api(params)
    #     print("result",result)
    # else:
    #     result = generate_music_api(params)
        
    return created_music_file_name



def convert_wav_to_mp3(input_wav_path, output_mp3_path) -> bool:
    """
    将.wav格式的音频文件转换为.mp3格式。
    Args:
        input_wav_path (str): 输入WAV文件的完整路径。
        output_mp3_path (str): 输出MP3文件的完整路径。
    Returns:
        bool: 如果转换成功返回True，否则返回False。
    """
    print(f"尝试将 '{input_wav_path}' 转换为 '{output_mp3_path}'...")
    try:
        # 加载WAV文件
        audio = AudioSegment.from_wav(input_wav_path)
        # 导出为MP3格式
        # bitrate 参数可以控制输出MP3的质量，例如 "192k", "256k", "320k"
        audio.export(output_mp3_path, format="mp3", bitrate="256k")
        print(f"成功将 '{input_wav_path}' 转换为 '{output_mp3_path}'。")
        return True
    except CouldntDecodeError:
        print(f"错误: 无法解码输入文件 '{input_wav_path}'。请确保它是有效的WAV文件。")
        return False
    except FileNotFoundError:
        # 这种情况通常是由于FFmpeg或FFprobe未正确安装或不在系统PATH中导致的。
        print(f"错误: 转换失败。可能是FFmpeg或FFprobe未正确安装或不在系统PATH中。")
        return False
    except Exception as e:
        print(f"转换过程中发生未知错误: {e}")
        return False