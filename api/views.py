from django.http import JsonResponse
import json
import os
import uuid
from django.conf import settings
from django.middleware.csrf import get_token  # get_token 用于登录时设置cookie
from django.views.decorators.csrf import ensure_csrf_cookie


@ensure_csrf_cookie
def get_csrf_token(request):
    """
    这个视图用于确保客户端有一个CSRF cookie。
    @ensure_csrf_cookie 装饰器会处理所有事情。
    """
    return JsonResponse({'detail': 'CSRF cookie set'})


def handle_signin(request):
    if request.method == 'POST':
        try:
            # 首次访问或登录成功时，确保CSRF cookie被设置
            get_token(request)

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


def create_music(request):
    '''
    创建音乐视图，接收前端传的歌曲描述和音频文件
    需要调用模型生成音乐，并将生成的音乐文件路径(类似http://localhost:8000/media/xxxx-xxxx.mp3)返回给前端
    '''
    if request.method == 'POST':
        try:
            # 接收到的歌曲描述
            description = request.POST.get('description', '')
            # 接收到的音频文件
            audio_file = request.FILES.get('audio_file')

            if audio_file:
                # 使用 uuid 确保文件名唯一，避免覆盖
                file_extension = os.path.splitext(audio_file.name)[1]
                file_name = f"{uuid.uuid4()}{file_extension}"
                file_path = os.path.join(settings.MEDIA_ROOT, file_name)

                # 将音频文件写入uploads目录
                with open(file_path, 'wb+') as dst_file:
                    for chunk in audio_file.chunks():
                        dst_file.write(chunk)

                print(f"Received Description: {description}")

                # 给模型传歌曲描述和用户上传的音频文件，获得模型生成的音频文件(期待完善～)

                # 返回上传的音频文件 URL
                # 构建文件的完整可访问 URL 例如: http://localhost:8000/media/xxxx-xxxx.mp3
                # 这边的settings.MEDIA_URL暂时指向uploads目录，uploads目录保存了前端上传的音频.mp3文件，后续需要改成模型生成的音乐URL
                # response_data里的name暂时返回上传的原始文件名，后续需要返回模型生成的音乐名称
                file_url = request.build_absolute_uri(os.path.join(settings.MEDIA_URL, file_name))
                print("File URL: ", file_url)
                response_data = {
                    'id': str(uuid.uuid4()),
                    'name': audio_file.name,  # 后续需要改成模型生成的音乐文件名称
                    'uri': file_url  # 返回真实的，模型生成的，可播放的文件URL
                }
            else:
                # 如果只有文本，暂时返回一个错误，后续需要像上面一样，返回一个模型生成的音乐URL
                return JsonResponse({'status': 'error', 'message': 'Error to create a song.'}, status=400)

            return JsonResponse(response_data, status=201)
        except Exception as e:
            print(f"Error in create_view: {e}")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)
