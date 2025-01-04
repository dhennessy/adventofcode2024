import time
from ui import draw_screen

PROGRESS = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

test_results = []
draw_screen(PROGRESS, test_results)
    
modules = {}
for day in range(25):
    try:
        modules[day] = __import__(f"0{day+1}")
    except ImportError:
        print(f"Day {day+1} not implemented")

# Run all tests
for day in range(1):
    try:
        module = modules[day]
        sample_answer = modules[day].sample_answer()
        actual_answer = modules[day].solve()
        correct = 0
        if actual_answer[0] == sample_answer[0]:
            correct += 1
        if actual_answer[1] == sample_answer[1]:
            correct += 1
        test_results.append(correct)
        draw_screen(PROGRESS, test_results)

        # If answer to sample is incorrect, then run with actual input
        if correct < 2:
            print(f"Day {day+1} sample: {actual_answer}, expected {sample_answer}")
            print(f"Running with actual input for day {day+1}")
            answer = module.solve()
            print(f"Day {day+1}: {answer}")
    except KeyError:
        pass
