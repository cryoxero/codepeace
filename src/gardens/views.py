from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Garden
import os
import subprocess
from shutil import rmtree

class TestSample():
    def __init__(self, input, output):
        self.input = input
        self.output = output
        self.result = list()
        self.status = '#34d399'

@login_required
def meditate(request, slug):
    garden = get_object_or_404(Garden, slug=slug)
    context = {
        'garden': garden,
        'initial_code': garden.initial_code,
        'tests': [],
        'ready_to_submit': False
    }

    input_path = f'{os.getcwd()}/{garden.test_input}'
    output_path = f'{os.getcwd()}/{garden.test_output}'

    with open(input_path, 'r') as input_file, open(output_path, 'r') as output_file:
        inputs = [line.strip() for line in input_file.readlines()]
        outputs = [line.strip() for line in output_file.readlines()]

        for i, (input_line, output_line) in enumerate(zip(inputs, outputs)):
            if i >= 13:
                break
            context['tests'].append(TestSample(', '.join(input_line.split()), output_line))

    if request.method == 'POST':
        solution = request.POST.get('solution')
        context['initial_code'] = solution

        # Write solution to src/
        runner_base = os.path.abspath(f'user-code/{request.user.username}')
        src_path = os.path.join(runner_base, "src")
        testcases_path = os.path.join(runner_base, "testcases")

        os.makedirs(src_path, exist_ok=True)
        os.makedirs(testcases_path, exist_ok=True)

        with open(os.path.join(src_path, "test_input.py"), "w") as f:
            f.write(solution)

        with open(os.path.join(testcases_path, "inputs.txt"), "w") as f:
            f.write("\n".join(inputs))

        with open(os.path.join(testcases_path, "expected_outputs.txt"), "w") as f:
            f.write("\n".join(outputs))

        # Run the container
        try:
            result = subprocess.run(
                [
                    "docker", "run", "--rm",
                    "-v", f"{src_path}:/home/runner/src",
                    "-v", f"{testcases_path}:/home/runner/testcases",
                    f"{garden.runner}-test",
                ],
                capture_output=True,
                text=True,
                timeout=10
            )
            output_lines = result.stdout.strip().splitlines()

            ready_to_submit = True
            for i, line in enumerate(output_lines):
                if i < len(context['tests']) and line.startswith("Test"):
                    lines = line.split("\\n")
                    res = lines[0].split(":")[-1].strip()
                    if res != 'PASS':
                        context['tests'][i].status = 'red'
                        ready_to_submit = False
                    context['tests'][i].result.append(res)
                    for l in lines[1:]:
                            context['tests'][i].result.append(l)
            context['ready_to_submit'] = ready_to_submit

            context["run_output"] = result.stdout

        except subprocess.TimeoutExpired:
            context["run_output"] = "Execution timed out."
        
        finally:
            try:
                rmtree(runner_base)

            except Exception as cleanup_error:
                print('Clean up failed...', cleanup_error)
        
        if request.POST['action'] == 'submit' and context['ready_to_submit'] == True:
            request.user.gain_xp(garden.level)

    return render(request, 'gardens/meditate.html', context)

