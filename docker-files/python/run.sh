#!/bin/bash

cp /home/runner/src/test_input.py .

paste /home/runner/testcases/inputs.txt /home/runner/testcases/expected_outputs.txt | while IFS=$'\t' read -r input expected; do
    args=$(echo "$input" | tr ' ' ,)

	output=$(python3 -c "
try:
    from test_input import solution
    import inspect

    args = [$args]
    sig = inspect.signature(solution)

    bound = sig.bind(*args)
    bound.apply_defaults()

    # Type enforcement
    for i, (name, value) in enumerate(bound.arguments.items()):
        expected_type = sig.parameters[name].annotation
        if expected_type is not inspect._empty:
            try:
                bound.arguments[name] = expected_type(value)
            except Exception as e:
                raise TypeError(f'Argument \"{name}\" must be {expected_type.__name__}, got {type(value).__name__}')

    result = solution(*bound.args)
    print('__PASS__:' + str(result))
except TypeError as e:
    print('__TYPE_ERROR__:' + str(e))
except Exception as e:
    print('__ERROR__:' + str(e))
")

    if [[ $output == __PASS__:* ]]; then
        result="${output#__PASS__:}"
        if [ "$result" = "$expected" ]; then
            echo "Test [$input]: PASS"
            pass_count=$((pass_count + 1))
        else
            echo "Test [$input]: FAIL\nExpected: $expected\nGot:      $result"
        fi
    elif [[ $output == __ERROR__:* ]]; then
        error="${output#__ERROR__:}"
        echo "Test [$input]: ERROR\nException: $error"
    elif [[ $output == __TYPE_ERROR__:* ]]; then
        error="${output#__TYPE_ERROR__:}"
        echo "Test [$input]: TYPE ERROR\nException: $error"
	else
        echo "Test [$input]: UNKNOWN ERROR\nRaw output: $output"
    fi
done
