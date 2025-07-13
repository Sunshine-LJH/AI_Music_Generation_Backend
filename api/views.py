from django.http import JsonResponse
from django.conf import settings
from django.middleware.csrf import get_token  # get_token 用于登录时设置cookie
from django.views.decorators.csrf import csrf_exempt
from .utils import create_music, convert_wav_to_mp3
import json
import os
import uuid
import asyncio

@csrf_exempt
def handle_signin(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')

            # 打印接收到的数据
            print(f"--- Sign In Request ---")
            print(f"Email: {email}")
            print(f"Password: {password}")

            # 验证用户并将用户信息存入数据库(暂未完成，期待补充～)

            # 这里我们直接返回成功
            return JsonResponse({'status': 'ok', 'message': 'Signed in successfully'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

@csrf_exempt
async def upload_and_fetch_music(request):
    if request.method == 'POST':
        try:
            creation_mode = None
            model = None
            description = None
            audio_file = None
            midi_file = None
            sequential = None
            duration = None
            song_name = None
            style = None
            audio_file_path = None
            midi_file_path = None

            if request.POST.get('creation_mode'):
                creation_mode = request.POST.get('creation_mode')

            if request.POST.get('model'):
                model = request.POST.get('model')

            if request.POST.get('description', ''):
                description = request.POST.get('description', '')

            if request.FILES.get('audio_file'):
                audio_file = request.FILES.get('audio_file')
                audio_file_path = os.path.join(settings.UPLOAD_ROOT, audio_file.name)
                with open(audio_file_path, 'wb+') as dst_file:
                    for chunk in audio_file.chunks():
                        dst_file.write(chunk)

            if request.FILES.get('midi_file'):
                midi_file = request.FILES.get('midi_file')
                midi_file_path = os.path.join(settings.MIDI_ROOT, midi_file.name)
                # 将midi文件写入midi目录
                with open(midi_file_path, 'wb+') as dst_file:
                    for chunk in audio_file.chunks():
                        dst_file.write(chunk)

            if request.POST.get('sequential'):
                sequential = request.POST.get('sequential')

            if request.POST.get('duration'):
                duration = request.POST.get('duration')

            if request.POST.get('song_name'):
                song_name = request.POST.get('song_name')

            if request.POST.get('style'):
                style = request.POST.get('style')

            print("creation_mode",creation_mode)
            print("model",model)
            print("description: ", description)
            print("audio_file: ", audio_file)
            print("midi_file: ", midi_file)
            print("sequential: ", sequential)
            print("duration: ", duration)
            print("song_name: ", song_name)
            print("style: ", style)
            print("audio_file_path: ", audio_file_path)
            print("midi_file_path: ", midi_file_path)

            loop_create_music = asyncio.get_event_loop()
            # 模型创建音乐 "final.wav"
            created_music_file_name = await loop_create_music.run_in_executor(
                None,  # 使用默认线程池执行器
                create_music,  # 要运行的同步函数
                creation_mode,
                model,
                style,
                description,  # 同步函数的一个参数
                audio_file_path,
                midi_file_path,
                sequential,
                duration,
                song_name
            )

            # final
            prefix_music_file = created_music_file_name[:created_music_file_name.rfind('.')]
            # final.mp3
            converted_music_file_name = prefix_music_file + ".mp3"
            input_wav_path = os.path.join(settings.MEDIA_ROOT, created_music_file_name)
            # output_mp3_path = BASE_DIR / media / final.mp3
            output_mp3_path = os.path.join(settings.MEDIA_ROOT, converted_music_file_name)

            loop_convert_wav_to_mp3 = asyncio.get_event_loop()
            is_convert_success = await loop_convert_wav_to_mp3.run_in_executor(
                None,
                convert_wav_to_mp3,
                input_wav_path,
                output_mp3_path
            )

            if is_convert_success:
                # created_music_file_url为请求的url，类似http://localhost:8000/media/final.mp3
                convert_music_url = os.path.join(settings.MEDIA_URL, converted_music_file_name)

                convert_absolute_music_url = request.build_absolute_uri(convert_music_url)
                print("Created music URL: ", convert_absolute_music_url)
                response_data = {
                    'id': str(uuid.uuid4()),
                    'name': converted_music_file_name, # 返回给前端展示的音乐名称
                    'uri': convert_absolute_music_url  # 返回真实的，模型生成的，可播放的文件URL
                }
                return JsonResponse(response_data, status=201)
            else:
                return JsonResponse({'status': 'error', 'message': 'Failed to convert WAV to MP3.'}, status=500)

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)
