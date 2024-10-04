import ast
import os
import argparse


def get_type_hints(function_node):
    """Extract type hints from the function node."""
    if function_node.returns:
        return_type = ast.unparse(function_node.returns)
    else:
        return_type = "None"

    arg_types = {}
    for arg in function_node.args.args:
        if arg.annotation:
            arg_types[arg.arg] = ast.unparse(arg.annotation)
        else:
            arg_types[arg.arg] = 'Any'

    return arg_types, return_type


def parse_python_file(file_path: str):
    """Parse given Python file and extract functions with typehints and docstrings."""

    with open(file_path, 'r') as file:
        file_content = file.read()

    tree = ast.parse(file_content)
    functions = []
    classes = []

    class_functions = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            func_name = node.name
            if func_name in class_functions:
                continue
            docstring = ast.get_docstring(node)
            arg_types, return_type = get_type_hints(node)
            functions.append({'name': func_name, 'args': arg_types, 'return': return_type, 'docstring': docstring})
        elif isinstance(node, ast.ClassDef):
            class_name = node.name
            methods = []
            for class_node in node.body:
                if isinstance(class_node, ast.FunctionDef):
                    method_name = class_node.name
                    class_functions.append(method_name)
                    docstring = ast.get_docstring(class_node)
                    arg_types, return_type = get_type_hints(class_node)

                    methods.append(
                        {'name': method_name, 'args': arg_types, 'return': return_type, 'docstring': docstring})
            classes.append({'name': class_name, 'methods': methods, 'docstring': ast.get_docstring(node)})

    return functions, classes


def generate_markdown(file_path: str, functions: list, classes: list, delim: str):
    """Generate a Markdown document from the extracted data."""
    # Create path to final md file
    final_path_build = file_path.split(delim)
    file_name = final_path_build.pop()
    final_path_build = ["QuickMDBuild"] + final_path_build
    final_path_build = "/".join(final_path_build)
    os.makedirs(final_path_build, exist_ok=True)
    doc_name = os.path.splitext(file_name)[0] + '.md'

    final_path = final_path_build + "/" + doc_name

    with open(final_path, 'w') as md_file:
        md_file.write(f'# {file_name} \n\n')
        if functions:
            md_file.write('## Functions <br>\n')
            for func in functions:
                md_file.write(f'### {func["name"]}() <br>\n')
                if func['docstring']:
                    md_file.write('**Docstring:** ')
                    md_file.write(f'{func["docstring"]}() <br>\n')
                else:
                    md_file.write('**Docstring:** None. <br>\n')
                md_file.write(f'**Type Hints:** <br>\n')
                for arg, type_hint in func['args'].items():
                    md_file.write(f'- {arg}: {type_hint} <br>\n')
                md_file.write(f'- return: {func["return"]} <br>\n')

        if classes:
            md_file.write('## Classes <br> \n')
            for cls in classes:
                md_file.write(f'### {cls["name"]} <br>\n')
                if cls['docstring']:
                    md_file.write(f'**Docstring:** {cls["docstring"]} <br>\n')
                else:
                    md_file.write('**Docstring:** None <br>\n')

                if cls['methods']:
                    md_file.write(f'**Methods:** <br>\n')
                    for method in cls['methods']:
                        md_file.write(f'### {method["name"]}() <br>\n')
                        if method['docstring']:
                            md_file.write('**Docstring:** ')
                            md_file.write(f'{method["docstring"]}() <br>\n')
                        else:
                            md_file.write('**Docstring:** None. <br>\n')
                        md_file.write(f'**Type Hints:** <br>\n')
                        for arg, type_hint in method['args'].items():
                            md_file.write(f'- {arg}: {type_hint} <br>\n')
                        md_file.write(f'- return: {method["return"]} <br>\n')

                else:
                    md_file.write('No Methods Defined.<br>\n')

    print(f'Markdown Document Generated: {doc_name}')


def main():
    parser = argparse.ArgumentParser(
        description="Script that generates MD file for file path given in cmd"
    )
    parser.add_argument("action", choices=["md"],
                        help="Type of file to create (md)")  # Allows us to add other file formats easier
    parser.add_argument("--path", required=True, type=str,
                        help="path to file from current working directory (i.e. 'src/main.py')")
    parser.add_argument("--delim", required=False, type=str, help="deliminator in your file path (None='/')")
    args = parser.parse_args()

    delim = args.delim if args.delim else "/"
    path = args.path
    functions, classes = parse_python_file(path)
    generate_markdown(path, functions, classes, delim)
    print(f"Fin..")


if __name__ == '__main__':
    main()
