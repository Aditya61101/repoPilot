def find_symbol_node(root, code_bytes, symbol):

    stack = [root]

    while stack:
        node = stack.pop()

        # function foo() {}
        if node.type == "function_declaration":

            name_node = node.child_by_field_name("name")

            if name_node:
                name = code_bytes[name_node.start_byte:name_node.end_byte].decode()

                if name == symbol:
                    return node

        # class Foo {}
        if node.type == "class_declaration":

            name_node = node.child_by_field_name("name")

            if name_node:
                name = code_bytes[name_node.start_byte:name_node.end_byte].decode()

                if name == symbol:
                    return node

        # const foo = () => {}
        if node.type == "variable_declarator":

            name_node = node.child_by_field_name("name")

            if name_node:
                name = code_bytes[name_node.start_byte:name_node.end_byte].decode()

                if name == symbol:
                    return node

        stack.extend(node.children)

    return None