
import argparse
import desktop_automation as da
import sys
import json
import os

# --- Constants ---
WORKFLOWS_DIR = "successful_workflows"
MANIFEST_FILE = "workflows_manifest.json"

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
                    params[key] = workflow_params[param_name]

        func_to_call = getattr(da, action_name, None)
        
        if func_to_call:
            # Pass the log_file_path to every action that accepts it
            if 'log_file_path' in func_to_call.__code__.co_varnames:
                params['log_file_path'] = log_file_path
            
            if action_name == 'press_hotkey':
                func_to_call(*params.pop('keys'), **params)
            else:
                func_to_call(**params)
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
    parser_end = subparsers.add_parser('end_task_with_verdict')
    parser_end.add_argument('--status', required=True, choices=['success', 'failure'])
    parser_end.add_argument('user_feedback', nargs='*', default="")
    parser_type = subparsers.add_parser('type_text')
    parser_type.add_argument('--text', required=True)
    parser_hotkey = subparsers.add_parser('press_hotkey')
    parser_hotkey.add_argument('keys', nargs='+')

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
