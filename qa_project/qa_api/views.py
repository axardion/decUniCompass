from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .qa_chain import ask_question
from django.http import HttpResponse
import os
from django.conf import settings


@csrf_exempt
@require_http_methods(["POST"])
def qa_view(request):
    try:
        data = json.loads(request.body)
        question = data.get('question')
        
        if not question:
            return JsonResponse({"error": "No question provided"}, status=400)
        
        answer = ask_question(question)
        return JsonResponse({"answer": answer})
    
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
def debug_file_view(request):
    data_file_path = os.path.join(settings.BASE_DIR, 'qa_api', 'data', 'data.txt')
    try:
        with open(data_file_path, 'r', encoding='windows-1251') as file:
            content = file.read()
        return HttpResponse(f"File content:<br><pre>{content[:500]}</pre>")
    except Exception as e:
        return HttpResponse(f"Error reading file: {str(e)}")