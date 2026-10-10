# Paste into the SECOND code cell under Lesson 6, replacing that cell.
async def gemini_mcp_demo():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            discovered = await session.list_tools()
            allowed = {tool.name for tool in discovered.tools}
            declarations = [types.FunctionDeclaration(
                name=tool.name, description=tool.description or "",
                parameters_json_schema=tool.inputSchema) for tool in discovered.tools]
            history = [types.Content(role="user", parts=[types.Part.from_text(
                text="Using the available tools, what fictional event is on Friday and when does the fictional library close?")])]
            config = types.GenerateContentConfig(
                tools=[types.Tool(function_declarations=declarations)],
                automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True))
            for _ in range(3):
                result = await client.aio.models.generate_content(
                    model=MODEL, contents=history, config=config)
                if not result.function_calls:
                    if not result.text:
                        raise RuntimeError("No final explanation returned.")
                    print(result.text)
                    return
                history.append(result.candidates[0].content)
                replies = []
                for call in result.function_calls:
                    if call.name not in allowed:
                        raise ValueError("Unknown MCP tool requested: " + str(call.name))
                    print("MCP TOOL:", call.name, call.args)
                    tool_result = await session.call_tool(call.name, dict(call.args or {}))
                    payload = tool_result.model_dump(mode="json", exclude_none=True)
                    print("MCP RESULT:", payload)
                    replies.append(types.Part.from_function_response(
                        name=call.name, response={"result": payload}))
                history.append(types.Content(role="tool", parts=replies))
            raise RuntimeError("Model turn limit reached; simplify the question.")

await gemini_mcp_demo()
