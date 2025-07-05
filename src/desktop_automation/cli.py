
import argparse
import sys
import json
import os

# 处理相对导入问题
try:
    from . import core as da
except ImportError:
    # 如果相对导入失败，使用绝对导入
    sys.path.insert(0, os.path.dirname(__file__))
    import core as da

# --- Constants ---
# 使用相对于当前模块的路径
import os.path
MODULE_DIR = os.path.dirname(__file__)
WORKFLOWS_DIR = os.path.join(MODULE_DIR, "successful_workflows")
MANIFEST_FILE = os.path.join(MODULE_DIR, "workflows_manifest.json")

def _execute_actions(actions, log_file_path, workflow_params=None):
    """Helper function to execute a list of action dictionaries."""
    if workflow_params is None:
        workflow_params = {}

    for action_item in actions:
        action_name = action_item.get("action")
        params = action_item.get("params", {})

        # Parameter substitution (e.g., replace "{{contact_name}}" with actual value)
        for key, value in params.items():
            if isinstance(value, str) and value.startswith("{{") and value.endswith("}}"):
                param_name = value[2:-2]
                if param_name in workflow_params:
                    param_value = workflow_params[param_name]
                    params[key] = param_value

        func_to_call = getattr(da, action_name, None)
        
        if func_to_call:
            # Pass the log_file_path to every action that accepts it
            if 'log_file_path' in func_to_call.__code__.co_varnames:
                params['log_file_path'] = log_file_path
            
            if action_name == 'press_hotkey':
                result = func_to_call(*params.pop('keys'), **params)
            else:
                result = func_to_call(**params)
            
            # Check for smart_click_text failures in workflows
            if action_name == 'smart_click_text' and result:
                print(f"Workflow step [{action_name}]: {result}")
                if "not found" in result.lower() or "failed" in result.lower() or "error" in result.lower():
                    print(f"Workflow failed at step: {action_name}", file=sys.stderr)
                    raise ValueError(f"Smart click action failed: {result}")
            elif result:
                print(f"Workflow step [{action_name}]: {result}")
        else:
            raise ValueError(f"Action '{action_name}' not found in desktop_automation module.")

def main():
    """
    A universal action runner that can execute single actions or a named workflow
    from the official workflows directory.
    """
    parser = argparse.ArgumentParser(
        description="A command-line runner for desktop_automation functions."
    )
    parser.add_argument('--log_file_path', default=None, help='Path to the log file for the action(s).')

    subparsers = parser.add_subparsers(dest='action', required=True, help='The action or mode to perform')

    # --- Mode 1: Single Action Parsers ---
    parser_start = subparsers.add_parser('start_task_log')
    parser_wait = subparsers.add_parser('wait')
    parser_wait.add_argument('--seconds', type=float, required=True)
    parser_sleep = subparsers.add_parser('sleep')
    parser_sleep.add_argument('--seconds', type=float, required=True)
    parser_end = subparsers.add_parser('end_task_with_verdict')
    parser_end.add_argument('--status', required=True, choices=['success', 'failure'])
    parser_end.add_argument('user_feedback', nargs='*', default="")
    parser_screenshot = subparsers.add_parser('take_screenshot')
    parser_screenshot.add_argument('--file_path', default='screenshot.png')
    parser_type = subparsers.add_parser('type_text')
    parser_type.add_argument('--text', required=True)
    parser_paste = subparsers.add_parser('paste_text')
    parser_paste.add_argument('--text', required=True)
    parser_hotkey = subparsers.add_parser('press_hotkey')
    parser_hotkey.add_argument('keys', nargs='+')
    
    # --- New Smart Action Parsers ---
    parser_analyze = subparsers.add_parser('analyze_screen_state', help='Analyze current screen content using OCR')
    
    parser_find_text = subparsers.add_parser('find_text_on_screen', help='Find text on screen and return its location')
    parser_find_text.add_argument('--target_text', required=True, help='Text to search for')
    
    parser_smart_click = subparsers.add_parser('smart_click_text', help='Intelligently find and click on text')
    parser_smart_click.add_argument('--target_text', required=True, help='Text to click on')
    parser_smart_click.add_argument('--button', default='left', choices=['left', 'right', 'middle'], help='Mouse button to click')
    parser_smart_click.add_argument('--max_retries', type=int, default=3, help='Maximum retry attempts')
    
    parser_wait_text = subparsers.add_parser('wait_for_text_appear', help='Wait for specific text to appear on screen')
    parser_wait_text.add_argument('--target_text', required=True, help='Text to wait for')
    parser_wait_text.add_argument('--timeout', type=int, default=10, help='Timeout in seconds')
    parser_wait_text.add_argument('--check_interval', type=float, default=1, help='Check interval in seconds')
    
    parser_verify = subparsers.add_parser('verify_operation_result', help='Verify operation success by checking for expected text')
    parser_verify.add_argument('--expected_text', required=True, help='Text that should appear if operation was successful')
    parser_verify.add_argument('--timeout', type=int, default=5, help='Timeout in seconds')

    # --- Mode 2: Workflow Executor ---
    parser_workflow = subparsers.add_parser('execute_workflow', help='Executes a named workflow from the library.')
    parser_workflow.add_argument('--name', required=True, help='The name of the workflow to execute.')
    # Change how params are handled to be more robust
    parser_workflow.add_argument('--params', type=str, default='{}', help='JSON string of parameters for the workflow.')

    args, unknown = parser.parse_known_args()

    # --- Main Logic ---

    if args.action == 'execute_workflow':
        try:
            with open(MANIFEST_FILE, 'r', encoding='utf-8') as f:
                manifest = json.load(f)
            workflow_meta = next((w for w in manifest['workflows'] if w['name'] == args.name), None)
            if not workflow_meta:
                raise FileNotFoundError(f"Workflow '{args.name}' not found in manifest.")
            
            workflow_file_path = os.path.join(WORKFLOWS_DIR, workflow_meta['file'])
            with open(workflow_file_path, 'r', encoding='utf-8') as f:
                action_sequence = json.load(f)

            # Manually parse the params JSON string
            workflow_params = json.loads(args.params)

            print(f"Executing workflow '{args.name}'...")
            _execute_actions(action_sequence, args.log_file_path, workflow_params)
            print(f"Workflow '{args.name}' finished.")

        except Exception as e:
            print(f"Error executing workflow '{args.name}': {e}", file=sys.stderr)
            sys.exit(1)

    else: # Handle single actions
        func_to_call = getattr(da, args.action, None)
        if func_to_call:
            params = vars(args).copy()
            del params['action']
            
            if args.action == 'end_task_with_verdict' and isinstance(params.get('user_feedback'), list):
                params['user_feedback'] = ' '.join(params['user_feedback'])

            if args.action == 'press_hotkey':
                func_to_call(*params.pop('keys'), **params)
            elif args.action == 'start_task_log':
                print(func_to_call())
            elif args.action == 'analyze_screen_state':
                result = func_to_call(**params)
                # Encode to UTF-8 and write bytes to stdout buffer to avoid console encoding issues
                output_json = json.dumps(result, indent=2, ensure_ascii=False)
                sys.stdout.buffer.write(output_json.encode('utf-8'))
            elif args.action == 'find_text_on_screen':
                result = func_to_call(**params)
                if result:
                    print(f"Found text at coordinates: {result}")
                else:
                    print("Text not found")
            elif args.action == 'wait_for_text_appear':
                result = func_to_call(**params)
                print(f"Wait result: {result}")
            elif args.action == 'verify_operation_result':
                result = func_to_call(**params)
                print(f"Verification result: {result}")
            else:
                # Ensure log_file_path is passed correctly for single actions too
                if 'log_file_path' in func_to_call.__code__.co_varnames:
                    func_to_call(**params)
                else:
                    params.pop('log_file_path', None) # Remove if not a valid arg
                    func_to_call(**params)
        else:
            print(f"Single action '{args.action}' not implemented or invalid.", file=sys.stderr)
            sys.exit(1)

if __name__ == '__main__':
    main()
