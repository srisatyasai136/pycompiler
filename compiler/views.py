import json
import subprocess
import uuid
import os

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


def home(request):
    return render(request, 'index1.html')


@csrf_exempt  # required because you're using fetch()
def run_code(request):
    if request.method != 'POST':
        return JsonResponse({'output': 'Invalid request method'}, status=405)

    try:
        data = json.loads(request.body)
        code = data.get('code', '')
        user_input = data.get('input', '')

        filename = f"temp_{uuid.uuid4().hex}.py"

        with open(filename, 'w') as f:
            f.write(code)

        result = subprocess.run(
            ['python', filename],
            input=user_input.encode('utf-8'),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=15
        )

        output = result.stdout.decode() + result.stderr.decode()

    except subprocess.TimeoutExpired:
        output = "❌ Error: Execution timed out. Possible infinite loop?"
    except Exception as e:
        output = f"❌ Internal error: {str(e)}"
    finally:
        if 'filename' in locals() and os.path.exists(filename):
            os.remove(filename)

    return JsonResponse({'output': output})
