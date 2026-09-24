#  Running MCP Server in copilot-cli

## 1 - Install copilot cl
Requires a GitHub subscription, can sign up here https://github.com

Open a new powershell terminal and run the command:
```powershell
npm install -g @github/copilot
```

Check it installed successfully:
```powershell
copilot --version
```

## 2 - Register MCP server
Run below command to register the MCP server:
```powershell
copilot mcp add business-insights -- python "{root}\mcp-server\server.py"

Once registered it does not to be executed again
```

## 3 - Start Copilot CLI
 
 run command:
```powershell
copilot
```
 
## 4 - Check the server is connected
 
Inside the copilot session session:
 
```
/mcp
```
 
`business-insights` should be listed as connected.
 
To see the tools it provides:
 
```
/mcp show business-insights
```

 `get_top_items`, `get_item_sales` and `get_item_forecast` should be listed
 
![MCP server listed](image.png)
![Tools listed](image-1.png)
 
## 5 - Ask a question
 
The server is now configured. Ask the agent a question and it will invoke a tool call:
 
```
For TestBusinessAcc, forecast Piping Tip 352 for the next 3 weeks.
```

**Note:** the data ingestion must be complete first
 